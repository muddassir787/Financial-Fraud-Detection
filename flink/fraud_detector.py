import os
import math
import time
import uuid
from datetime import datetime

from cassandra.cluster import Cluster

from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import MapFunction
from pyflink.table import StreamTableEnvironment


class FraudDetectorMap(MapFunction):

    def open(self, runtime_context):

        cassandra_host = os.getenv("CASSANDRA_HOST", "cassandra")

        print("=" * 60)
        print("Connecting to Cassandra...")
        print("Host:", cassandra_host)
        print("=" * 60)

        retries = 20

        while retries > 0:
            try:
                self.cluster = Cluster([cassandra_host])
                self.session = self.cluster.connect("fraud_detection")

                print("Connected to Cassandra")
                break

            except Exception as e:

                print("Waiting for Cassandra...")
                print(e)

                retries -= 1
                time.sleep(5)

        if retries == 0:
            raise RuntimeError("Cannot connect to Cassandra.")

        # ---------------------------------------------------
        # Prepared Statements
        # ---------------------------------------------------

        self.insert_transaction = self.session.prepare("""
            INSERT INTO transactions
            (
                bucket,
                timestamp,
                transaction_id,
                card_number,
                amount,
                merchant,
                category,
                latitude,
                longitude,
                is_fraud
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)

        self.insert_card = self.session.prepare("""
            INSERT INTO transactions_by_card
            (
                card_number,
                timestamp,
                transaction_id,
                amount,
                latitude,
                longitude
            )
            VALUES
            (?, ?, ?, ?, ?, ?)
        """)

        self.insert_alert = self.session.prepare("""
            INSERT INTO fraud_alerts
            (
                bucket,
                timestamp,
                alert_id,
                transaction_id,
                card_number,
                amount,
                merchant,
                reason
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
        """)

        self.select_recent = self.session.prepare("""
            SELECT
                timestamp,
                amount,
                latitude,
                longitude
            FROM transactions_by_card
            WHERE card_number = ?
            LIMIT 10
        """)

        print("Prepared statements created.")

    # -------------------------------------------------------
    # Utility Functions
    # -------------------------------------------------------

    def get_value(self, row, index, name):

        try:
            return row[name]
        except Exception:
            pass

        try:
            return getattr(row, name)
        except Exception:
            pass

        return row[index]

    def haversine_distance(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):

        radius = 6371.0

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2
            +
            math.cos(math.radians(lat1))
            *
            math.cos(math.radians(lat2))
            *
            math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return radius * c

    # -------------------------------------------------------
    # Main Processing Function
    # -------------------------------------------------------

    def map(self, value):

        transaction_id = self.get_value(
            value,
            0,
            "transaction_id"
        )

        card_number = self.get_value(
            value,
            1,
            "card_number"
        )

        amount = float(
            self.get_value(
                value,
                2,
                "amount"
            )
        )

        timestamp_string = self.get_value(
            value,
            3,
            "ts_str"
        )

        merchant = self.get_value(
            value,
            4,
            "merchant"
        )

        category = self.get_value(
            value,
            5,
            "category"
        )

        latitude = float(
            self.get_value(
                value,
                6,
                "latitude"
            )
        )

        longitude = float(
            self.get_value(
                value,
                7,
                "longitude"
            )
        )

        transaction_uuid = uuid.UUID(transaction_id)

        try:

            if timestamp_string.endswith("Z"):
                timestamp_string = timestamp_string[:-1]

            timestamp = datetime.fromisoformat(
                timestamp_string
            )

        except Exception:

            timestamp = datetime.utcnow()

        is_fraud = False

        reasons = []

        recent_transactions = []

        try:

            rows = self.session.execute(
                self.select_recent,
                [card_number]
            )

            for row in rows:
                recent_transactions.append(row)

        except Exception as e:

            print("History Lookup Error")

            print(e)
        # -------------------------------------------------------
        # Rule 1 : High Amount
        # -------------------------------------------------------

        if amount > 5000:

            is_fraud = True

            reasons.append(
                f"High Amount (${amount:.2f})"
            )

        # -------------------------------------------------------
        # Rule 2 : Velocity Fraud
        # More than 3 transactions within 60 seconds
        # -------------------------------------------------------

        recent_60_seconds = []

        for txn in recent_transactions:

            try:

                diff = abs(
                    (timestamp - txn.timestamp).total_seconds()
                )

                if diff <= 60:

                    recent_60_seconds.append(txn)

            except Exception:

                pass

        if len(recent_60_seconds) >= 3:

            is_fraud = True

            reasons.append(
                f"Velocity Fraud ({len(recent_60_seconds)} txns in 60 sec)"
            )

        # -------------------------------------------------------
        # Rule 3 : Impossible Travel
        # -------------------------------------------------------

        if len(recent_transactions) > 0:

            previous = recent_transactions[0]

            try:

                distance = self.haversine_distance(
                    latitude,
                    longitude,
                    previous.latitude,
                    previous.longitude
                )

                seconds = abs(
                    (timestamp - previous.timestamp).total_seconds()
                )

                if seconds > 0:

                    speed = (distance / seconds) * 3600

                    if distance > 100 and speed > 800:

                        is_fraud = True

                        reasons.append(
                            f"Impossible Travel ({distance:.1f} km @ {speed:.1f} km/h)"
                        )

            except Exception as e:

                print("Travel Rule Error")

                print(e)

        # -------------------------------------------------------
        # Save Transaction
        # -------------------------------------------------------

        bucket = 0

        try:

            self.session.execute(
                self.insert_transaction,
                [
                    bucket,
                    timestamp,
                    transaction_uuid,
                    card_number,
                    amount,
                    merchant,
                    category,
                    latitude,
                    longitude,
                    is_fraud
                ]
            )

        except Exception as e:

            print("Insert Transaction Error")

            print(e)

        # -------------------------------------------------------
        # Save Card History
        # -------------------------------------------------------

        try:

            self.session.execute(
                self.insert_card,
                [
                    card_number,
                    timestamp,
                    transaction_uuid,
                    amount,
                    latitude,
                    longitude
                ]
            )

        except Exception as e:

            print("Insert Card History Error")

            print(e)

        # -------------------------------------------------------
        # Fraud Alert
        # -------------------------------------------------------

        if is_fraud:

            alert_id = uuid.uuid4()

            reason_string = ", ".join(reasons)

            try:

                self.session.execute(
                    self.insert_alert,
                    [
                        bucket,
                        timestamp,
                        alert_id,
                        transaction_uuid,
                        card_number,
                        amount,
                        merchant,
                        reason_string
                    ]
                )

                print("=" * 60)
                print("FRAUD ALERT")
                print("=" * 60)
                print("Card      :", card_number)
                print("Amount    :", amount)
                print("Merchant  :", merchant)
                print("Reason    :", reason_string)
                print("=" * 60)

            except Exception as e:

                print("Insert Alert Error")

                print(e)

        # -------------------------------------------------------
        # Console Output
        # -------------------------------------------------------

        return (
            f"Transaction={transaction_id} | "
            f"Card={card_number} | "
            f"Amount={amount:.2f} | "
            f"Fraud={is_fraud}"
        )

    # -------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------

    def close(self):

        try:

            self.cluster.shutdown()

            print("Cassandra Connection Closed")

        except Exception:

            pass
def main():

    print("=" * 70)
    print("Starting PyFlink Financial Fraud Detection Job")
    print("=" * 70)

    # --------------------------------------------------
    # Execution Environment
    # --------------------------------------------------

    env = StreamExecutionEnvironment.get_execution_environment()

    env.set_parallelism(1)

    t_env = StreamTableEnvironment.create(env)

    # --------------------------------------------------
    # Kafka Source Table
    # --------------------------------------------------

    t_env.execute_sql("""

        CREATE TABLE kafka_transactions (

            transaction_id STRING,

            card_number STRING,

            amount DOUBLE,

            ts_str STRING,

            merchant STRING,

            category STRING,

            latitude DOUBLE,

            longitude DOUBLE

        ) WITH (

            'connector' = 'kafka',

            'topic' = 'transactions',

            'properties.bootstrap.servers' = 'kafka:9092',

            'properties.group.id' = 'fraud-detector-group',

            'scan.startup.mode' = 'latest-offset',

            'format' = 'json',

            'json.ignore-parse-errors' = 'true',

            'json.fail-on-missing-field' = 'false'

        )

    """)

    print("Kafka Table Created")

    # --------------------------------------------------
    # Convert Table -> DataStream
    # --------------------------------------------------

    table = t_env.from_path("kafka_transactions")

    stream = t_env.to_data_stream(table)

    # --------------------------------------------------
    # Fraud Detection
    # --------------------------------------------------

    processed_stream = stream.map(

        FraudDetectorMap(),

        output_type=Types.STRING()

    )

    # --------------------------------------------------
    # Print Output
    # --------------------------------------------------

    processed_stream.print()

    print("Fraud Detector Running...")

    # --------------------------------------------------
    # Execute Job
    # --------------------------------------------------

    env.execute("Real-Time Financial Fraud Detection")


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":

    main()