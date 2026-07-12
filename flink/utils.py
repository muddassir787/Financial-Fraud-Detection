"""
utils.py

Common helper functions.
"""

import math
from datetime import datetime


def parse_timestamp(value):

    try:

        if value.endswith("Z"):

            value = value[:-1]

        return datetime.fromisoformat(value)

    except Exception:

        try:

            return datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S"
            )

        except Exception:

            return datetime.utcnow()


def haversine_distance(
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
        math.cos(
            math.radians(lat1)
        )
        *
        math.cos(
            math.radians(lat2)
        )
        *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return radius * c


def calculate_speed(
    distance_km,
    seconds
):

    if seconds <= 0:

        return 0

    return (
        distance_km /
        seconds
    ) * 3600


def safe_float(value):

    try:

        return float(value)

    except Exception:

        return 0.0


def safe_int(value):

    try:

        return int(value)

    except Exception:

        return 0


def print_banner(text):

    print("=" * 70)

    print(text)

    print("=" * 70)


def print_transaction(
    transaction_id,
    card,
    amount,
    fraud
):

    print("-" * 70)

    print(f"Transaction : {transaction_id}")

    print(f"Card        : {card}")

    print(f"Amount      : ${amount:.2f}")

    print(f"Fraud       : {fraud}")

    print("-" * 70)