import os
import time
import uuid
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class CassandraDB:

    def __init__(self):
        self.cassandra_host = os.getenv("CASSANDRA_HOST", "cassandra")
        self.cassandra_port = int(os.getenv("CASSANDRA_PORT", "9042"))
        self.keyspace = os.getenv("CASSANDRA_KEYSPACE", "fraud_detection")
        self.username = os.getenv("CASSANDRA_USERNAME", "")
        self.password = os.getenv("CASSANDRA_PASSWORD", "")

        self.cluster = None
        self.session = None

        self._connect()

    ############################################################
    # Connect
    ############################################################

    def _connect(self):

        retries = 20

        while retries > 0:
            try:
                print("=" * 60)
                print("Connecting to Cassandra...")
                print(f"Host : {self.cassandra_host}")
                print(f"Port : {self.cassandra_port}")
                print("=" * 60)

                if self.username and self.password:
                    auth = PlainTextAuthProvider(
                        username=self.username,
                        password=self.password
                    )

                    self.cluster = Cluster(
                        [self.cassandra_host],
                        port=self.cassandra_port,
                        auth_provider=auth
                    )
                else:
                    self.cluster = Cluster(
                        [self.cassandra_host],
                        port=self.cassandra_port
                    )

                self.session = self.cluster.connect(self.keyspace)

                print("Connected to Cassandra Successfully.")

                return

            except Exception as e:

                print("Connection Failed")
                print(e)

                retries -= 1
                time.sleep(5)

        raise Exception("Unable to connect to Cassandra")

    ############################################################

    def close(self):
        if self.cluster:
            self.cluster.shutdown()

    ############################################################
    # Dashboard Statistics
    ############################################################

    def get_dashboard_stats(self):

        try:

            total_transactions = self.session.execute(
                "SELECT COUNT(*) FROM transactions"
            ).one()[0]

            total_alerts = self.session.execute(
                "SELECT COUNT(*) FROM fraud_alerts"
            ).one()[0]

            fraud_transactions = self.session.execute(
                """
                SELECT COUNT(*)
                FROM transactions
                WHERE is_fraud=true
                ALLOW FILTERING
                """
            ).one()[0]

            fraud_rate = 0

            if total_transactions > 0:
                fraud_rate = round(
                    fraud_transactions * 100 / total_transactions,
                    2
                )

            return {

                "total_transactions": total_transactions,

                "total_fraud": fraud_transactions,

                "total_alerts": total_alerts,

                "fraud_rate": fraud_rate

            }

        except Exception as e:

            print("Dashboard Error:", e)

            return {
                "total_transactions": 0,
                "total_fraud": 0,
                "total_alerts": 0,
                "fraud_rate": 0
            }

    ############################################################
    # Recent Transactions
    ############################################################

    def get_recent_transactions(self, limit=20):

        try:

            query = f"""
            SELECT *
            FROM transactions
            WHERE bucket=0
            ORDER BY timestamp DESC
            LIMIT {limit}
            """

            rows = self.session.execute(query)

            transactions = []

            for row in rows:

                transactions.append({

                    "transaction_id": str(row.transaction_id),

                    "card_number": row.card_number,

                    "amount": float(row.amount),

                    "merchant": row.merchant,

                    "category": row.category,

                    "latitude": float(row.latitude),

                    "longitude": float(row.longitude),

                    "is_fraud": row.is_fraud,

                    "timestamp": row.timestamp

                })

            return transactions

        except Exception as e:

            print("Transaction Error:", e)

            return []

    ############################################################
    # Recent Alerts
    ############################################################

    def get_recent_alerts(self, limit=20):

        try:

            query = f"""
            SELECT *
            FROM fraud_alerts
            WHERE bucket=0
            ORDER BY timestamp DESC
            LIMIT {limit}
            """

            rows = self.session.execute(query)

            alerts = []

            for row in rows:

                alerts.append({

                    "alert_id": str(row.alert_id),

                    "transaction_id": str(row.transaction_id),

                    "card_number": row.card_number,

                    "amount": float(row.amount),

                    "merchant": row.merchant,

                    "reason": row.reason,

                    "timestamp": row.timestamp

                })

            return alerts

        except Exception as e:

            print("Alert Error:", e)

            return []

    ############################################################
    # Card Transactions
    ############################################################

    def get_card_transactions(self, card_number):

        try:

            rows = self.session.execute(
                """
                SELECT *
                FROM transactions_by_card
                WHERE card_number=%s
                """,
                (card_number,)
            )

            return [row._asdict() for row in rows]

        except Exception as e:

            print(e)

            return []

    ############################################################
    # Transaction Search
    ############################################################

    def get_transaction(self, transaction_id):

        try:

            rows = self.session.execute(
                """
                SELECT *
                FROM transactions
                WHERE transaction_id=%s
                ALLOW FILTERING
                """,
                (uuid.UUID(transaction_id),)
            )

            row = rows.one()

            if row:
                return row._asdict()

            return None

        except Exception as e:

            print(e)

            return None