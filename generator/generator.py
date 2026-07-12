import json
import time
import random
import uuid
import os
from datetime import datetime
from kafka import KafkaProducer
from transaction_generator import TransactionGenerator


# -------------------------------------------------------------------
# Kafka Configuration
# -------------------------------------------------------------------
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:39092"
)

TOPIC = "transactions"


# -------------------------------------------------------------------
# Create Kafka Producer
# -------------------------------------------------------------------
def create_producer():

    retries = 20

    while retries > 0:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                retries=5,
                acks="all"
            )

            print("========================================")
            print("Connected to Kafka")
            print(f"Broker : {KAFKA_BOOTSTRAP_SERVERS}")
            print(f"Topic  : {TOPIC}")
            print("========================================")

            return producer

        except Exception as e:

            retries -= 1

            print(f"Kafka not ready : {e}")
            print(f"Retrying... ({retries} retries left)")

            time.sleep(5)

    raise RuntimeError("Unable to connect to Kafka.")


# -------------------------------------------------------------------
# Send Transaction
# -------------------------------------------------------------------
def send_transaction(producer, transaction):

    try:

        producer.send(TOPIC, value=transaction)

        producer.flush()

        print(
            f"[{transaction['ts_str']}] "
            f"{transaction['transaction_id']} | "
            f"{transaction['card_number']} | "
            f"${transaction['amount']} | "
            f"{transaction['merchant']}"
        )

    except Exception as e:

        print("Error sending transaction")

        print(e)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
def main():

    producer = create_producer()

    generator = TransactionGenerator()

    print("\nStarting Financial Transaction Generator...\n")

    total = 0

    while True:

        transaction = generator.generate_transaction()

        send_transaction(producer, transaction)

        total += 1

        if total % 20 == 0:

            print("------------------------------------------")
            print(f"Generated {total} Transactions")
            print("------------------------------------------")

        time.sleep(random.uniform(0.4, 1.2))


# -------------------------------------------------------------------
# Entry
# -------------------------------------------------------------------
if __name__ == "__main__":

    main()