"""
fraud_rules.py

Contains reusable fraud detection rules.
"""

from datetime import datetime
from utils import haversine_distance


HIGH_AMOUNT_LIMIT = 5000
VELOCITY_WINDOW_SECONDS = 60
VELOCITY_TRANSACTION_LIMIT = 3

MAX_TRAVEL_SPEED = 800          # km/h
MIN_TRAVEL_DISTANCE = 100       # km


def high_amount_rule(amount):
    """
    Rule 1
    """

    if amount > HIGH_AMOUNT_LIMIT:

        return (
            True,
            f"High Amount (${amount:.2f})"
        )

    return (
        False,
        ""
    )


def velocity_rule(current_timestamp, history):

    count = 0

    for txn in history:

        try:

            diff = abs(
                (
                    current_timestamp -
                    txn.timestamp
                ).total_seconds()
            )

            if diff <= VELOCITY_WINDOW_SECONDS:

                count += 1

        except Exception:

            continue

    if count >= VELOCITY_TRANSACTION_LIMIT:

        return (
            True,
            f"Velocity Fraud ({count} transactions within {VELOCITY_WINDOW_SECONDS} sec)"
        )

    return (
        False,
        ""
    )


def impossible_travel_rule(
    current_timestamp,
    current_lat,
    current_lon,
    history
):

    if len(history) == 0:

        return (
            False,
            ""
        )

    previous = history[0]

    try:

        distance = haversine_distance(
            current_lat,
            current_lon,
            previous.latitude,
            previous.longitude
        )

        seconds = abs(
            (
                current_timestamp -
                previous.timestamp
            ).total_seconds()
        )

        if seconds <= 0:

            return (
                False,
                ""
            )

        speed = (distance / seconds) * 3600

        if (
            distance >= MIN_TRAVEL_DISTANCE and
            speed >= MAX_TRAVEL_SPEED
        ):

            return (
                True,
                f"Impossible Travel ({distance:.1f} km @ {speed:.1f} km/h)"
            )

    except Exception:

        pass

    return (
        False,
        ""
    )


def detect_fraud(
    amount,
    timestamp,
    latitude,
    longitude,
    history
):
    """
    Executes all fraud rules.
    """

    reasons = []

    fraud = False

    result, reason = high_amount_rule(amount)

    if result:

        fraud = True

        reasons.append(reason)

    result, reason = velocity_rule(
        timestamp,
        history
    )

    if result:

        fraud = True

        reasons.append(reason)

    result, reason = impossible_travel_rule(
        timestamp,
        latitude,
        longitude,
        history
    )

    if result:

        fraud = True

        reasons.append(reason)

    return fraud, reasons