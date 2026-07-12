import random
import uuid
import json
import time
from datetime import datetime
from faker import Faker

fake = Faker()

# ==========================================================
# Merchant Categories
# ==========================================================

MERCHANTS = {
    "Groceries": [
        "Walmart",
        "Carrefour",
        "Tesco",
        "Metro",
        "Fresh Mart"
    ],

    "Electronics": [
        "Amazon",
        "Best Buy",
        "Apple Store",
        "Samsung Store",
        "AliExpress"
    ],

    "Restaurant": [
        "McDonalds",
        "KFC",
        "Pizza Hut",
        "Dominos",
        "Burger King"
    ],

    "Fuel": [
        "Shell",
        "Total",
        "PSO",
        "Caltex",
        "Exxon"
    ],

    "Fashion": [
        "Nike",
        "Adidas",
        "Zara",
        "H&M",
        "Uniqlo"
    ],

    "ATM": [
        "HBL ATM",
        "UBL ATM",
        "MCB ATM",
        "Bank Alfalah ATM"
    ],

    "Travel": [
        "Emirates",
        "PIA",
        "Booking.com",
        "Airbnb"
    ],

    "Medical": [
        "City Hospital",
        "Apollo Pharmacy",
        "Care Hospital"
    ]
}

# ==========================================================
# Customer Profiles
# ==========================================================

CUSTOMERS = []

for i in range(100):
    CUSTOMERS.append({
        "customer_id": i + 1,
        "card_number": str(random.randint(
            4000000000000000,
            4999999999999999
        )),
        "home_city": random.choice([
            "Lahore",
            "Karachi",
            "Islamabad",
            "Rawalpindi",
            "Faisalabad",
            "Multan",
            "Peshawar"
        ]),
        "avg_amount": random.randint(100, 1500)
    })

# ==========================================================
# GPS Coordinates
# ==========================================================

CITY_LOCATIONS = {
    "Lahore": (31.5204, 74.3587),
    "Karachi": (24.8607, 67.0011),
    "Islamabad": (33.6844, 73.0479),
    "Rawalpindi": (33.5651, 73.0169),
    "Multan": (30.1575, 71.5249),
    "Faisalabad": (31.4504, 73.1350),
    "Peshawar": (34.0151, 71.5249)
}

# ==========================================================
# Blacklisted Merchants
# ==========================================================

BLACKLISTED_MERCHANTS = [
    "Dark Electronics",
    "Unknown Shop",
    "Fake ATM",
    "Ghost Store"
]

# ==========================================================
# Fraud Probability
# ==========================================================

FRAUD_PROBABILITY = 0.10

# ==========================================================
# Transaction Amount Limits
# ==========================================================

MIN_AMOUNT = 10

MAX_AMOUNT = 15000

# ==========================================================
# Transaction Categories
# ==========================================================

CATEGORIES = list(MERCHANTS.keys())


class TransactionGenerator:
    
    def __init__(self):
        self.merchants = list(MERCHANTS.values())
        self.categories = CATEGORIES
        self.velocity_card = random.choice(CUSTOMERS)["card_number"]
        self.travel_card = random.choice(CUSTOMERS)["card_number"]
        self.travel_toggle = True
    
    def random_card(self):
        return random.choice(CUSTOMERS)["card_number"]
    
    def random_merchant(self):
        merchants_list = random.choice(self.merchants)
        return random.choice(merchants_list)
    
    def random_category(self):
        return random.choice(self.categories)
    
    def random_location(self):
        """Returns (latitude, longitude)"""
        return (
            round(random.uniform(24.8, 25.2), 6),
            round(random.uniform(66.9, 67.4), 6)
        )
    
    def generate_normal_transaction(self):
        """Generate a normal transaction."""
        lat, lon = self.random_location()
        
        txn = {
            "transaction_id": str(uuid.uuid4()),
            "card_number": self.random_card(),
            "amount": round(random.uniform(5, 1000), 2),
            "ts_str": datetime.utcnow().isoformat(),
            "merchant": self.random_merchant(),
            "category": self.random_category(),
            "latitude": lat,
            "longitude": lon
        }
        
        return txn
    
    def generate_high_amount_transaction(self):
        """Fraud Rule 1: High Amount"""
        txn = self.generate_normal_transaction()
        txn["amount"] = round(random.uniform(6000, 25000), 2)
        return txn
    
    def generate_velocity_transaction(self):
        """Fraud Rule 2: Velocity - card used repeatedly"""
        txn = self.generate_normal_transaction()
        txn["card_number"] = self.velocity_card
        return txn
    
    def generate_impossible_travel_transaction(self):
        """Fraud Rule 3: Impossible Travel - same card jumps between cities"""
        txn = self.generate_normal_transaction()
        txn["card_number"] = self.travel_card
        
        if self.travel_toggle:
            # Karachi
            txn["latitude"] = 24.8607
            txn["longitude"] = 67.0011
        else:
            # Lahore
            txn["latitude"] = 31.5204
            txn["longitude"] = 74.3587
        
        self.travel_toggle = not self.travel_toggle
        return txn
    
    def generate_transaction(self):
        r = random.random()
        
        # 70% Normal
        if r < 0.70:
            return self.generate_normal_transaction()
        # 10% High Amount
        elif r < 0.80:
            return self.generate_high_amount_transaction()
        # 10% Velocity Fraud
        elif r < 0.90:
            return self.generate_velocity_transaction()
        # 10% Impossible Travel
        else:
            return self.generate_impossible_travel_transaction()


if __name__ == "__main__":
    generator = TransactionGenerator()
    
    while True:
        tx = generator.generate_transaction()
        print(json.dumps(tx, indent=2))
        time.sleep(1)
