import os
import random
from datetime import datetime, timedelta
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "ride_share_v1")



client = MongoClient(MONGO_URI)
db = client["ride_share_v1"]


STATUSES = ["active", "inactive", "suspended", "banned"]
STATUS_WEIGHTS = [0.80, 0.10, 0.07, 0.03]
SUSPENDED_REASONS = ["documents_expired", "complaint", "fraud_suspected", "policy_violation"]
BANNED_REASONS = ["fraud_confirmed", "multiple_violations", "legal_issue", "permanent_decision"]

now = datetime.utcnow()

bulk_ops = []
for driver in db.drivers.find({}, {"_id": 1}):
    status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
    update = {"status": status}
    if status == "inactive":
        days = random.randint(1, 90)
        update["inactive_since"] = now - timedelta(days=days)
    elif status == "suspended":
        days = random.randint(1, 60)
        update["suspended_since"] = now - timedelta(days=days)
        update["suspended_reason"] = random.choice(SUSPENDED_REASONS)
    elif status == "banned":
        days = random.randint(1, 365)
        update["banned_since"] = now - timedelta(days=days)
        update["banned_reason"] = random.choice(BANNED_REASONS)
    bulk_ops.append(
        UpdateOne(
            {"_id": driver["_id"]},
            {"$set": update}
        )
    )

if bulk_ops:
    result = db.drivers.bulk_write(bulk_ops)
    print(f"{result.modified_count} drivers mis à jour.")
else:
    print("Aucun driver trouvé.")