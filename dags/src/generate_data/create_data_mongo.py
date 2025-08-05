import os
import logging
import random
from datetime import datetime, timedelta, timezone
from typing import List

#from dotenv import load_dotenv
import os 
import sys
import logging
logging.basicConfig(level=logging.INFO)

logging.info(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "generate_data"))
logger = logging.getLogger(__name__)


from faker import Faker
from pydantic import BaseModel
from pymongo import MongoClient
from models_mongo import *

# -------------------- LOAD ENV --------------------
#load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/ride_share")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000))
NB_COUNTRIES = int(os.getenv("NB_COUNTRIES", 5))
NB_CITIES = int(os.getenv("NB_CITIES", NB_COUNTRIES*10))
NB_USERS = int(os.getenv("NB_USERS", 100000))
NB_DRIVERS = int(os.getenv("NB_DRIVERS", 15000))
NB_VEHICLES = int(os.getenv("NB_VEHICLES", 30000))
NB_TRIPS = int(os.getenv("NB_TRIPS", 605000))
NB_MAINTENANCE = int(os.getenv("NB_MAINTENANCE", 10000))

# -------------------- LOGGING SETUP --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------- Pydantic MODELS --------------------


# -------------------- INIT --------------------
fake = Faker()
Faker.seed(42)
client = MongoClient(MONGO_URI)
db = client["ride_share_v1"]

# -------------------- HELPERS --------------------
def random_datetime(start: datetime, end: datetime) -> datetime:
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def batch_insert(collection: str, docs: List[BaseModel]):
    for i in range(0, len(docs), BATCH_SIZE):
        batch = docs[i : i + BATCH_SIZE]
        payload = [d.model_dump(by_alias=True, exclude_none=True) for d in batch]
        result = db[collection].insert_many(payload)
        logger.info(f"Inserted {len(result.inserted_ids)} into {collection}")

# -------------------- GENERATION --------------------
def generate_countries() -> List[Country]:
    template = [
        {"name": "Bénin", "isoCode": "BJ", "currency": "XOF", "locale": "fr-BJ"},
        {"name": "Nigeria", "isoCode": "NG", "currency": "NGN", "locale": "en-NG"},
        {"name": "Ghana", "isoCode": "GH", "currency": "GHS", "locale": "en-GH"},
        {"name": "Kenya", "isoCode": "KE", "currency": "KES", "locale": "en-KE"},
        {"name": "Côte d'Ivoire", "isoCode": "CI", "currency": "XOF", "locale": "fr-CI"},
        {"name": "Congo (DRC)", "isoCode": "CD", "currency": "CDF", "locale": "fr-CD"},
        {"name": "Congo (Republic)", "isoCode": "CG", "currency": "XAF", "locale": "fr-CG"},
        {"name": "Cameroon", "isoCode": "CM", "currency": "XAF", "locale": "fr-CM"},
        {"name": "Tchad", "isoCode": "TD", "currency": "XAF", "locale": "fr-TD"},
        {"name": "Central African Republic", "isoCode": "CF", "currency": "XAF", "locale": "fr-CF"},
        {"name": "Equatorial Guinea", "isoCode": "GQ", "currency": "XAF", "locale": "fr-GQ"},
        {"name": "Gabon", "isoCode": "GA", "currency": "XAF", "locale": "fr-GA"},
        {"name": "Guinea", "isoCode": "GN", "currency": "XOF", "locale": "fr-GN"},
        {"name": "Guinea-Bissau", "isoCode": "GW", "currency": "XOF", "locale": "fr-GW"},
        {"name": "Mali", "isoCode": "ML", "currency": "XOF", "locale": "fr-ML"},
        {"name": "Mauritania", "isoCode": "MR", "currency": "XOF", "locale": "fr-MR"},
        {"name": "Senegal", "isoCode": "SN", "currency": "XOF", "locale": "fr-SN"},
        {"name": "Sierra Leone", "isoCode": "SL", "currency": "SLL", "locale": "en-SL"},
        {"name": "Togo", "isoCode": "TG", "currency": "XOF", "locale": "fr-TG"},
    ]
    return [Country(**c) for c in template]

# -------------------- MAIN SEED --------------------
def generate_data_all():
    # Drop existing
    for col in ["countries","users","drivers","vehicles","trips","ratings","maintenance"]:
        db.drop_collection(col)
        logger.debug(f"Dropped {col}")

    # Countries
    countries = generate_countries()
    batch_insert("countries", countries)
    iso_map = {c.isoCode: cid["_id"] for c, cid in zip(countries, db.countries.find({}, {"_id": 1, "isoCode": 1}))}

    # Cities (from cities_data.json)
    import json
    with open(os.path.join(os.path.dirname(__file__), "cities_data.json"), "r", encoding="utf-8") as f:
        cities_data = json.load(f)

    city_map = {}  # isoCode -> list of city ObjectIds
    for country in db.countries.find({}, {"_id": 1, "isoCode": 1}):
        iso = country["isoCode"]
        country_id = country["_id"]
        cities = []
        n_cities = random.randint(8, min(20, len(cities_data.get(iso, []))))
        for city_info in random.sample(cities_data.get(iso, []), n_cities):
            city = City(
                name=city_info["name"],
                countryId=country_id,
                longitude=city_info["lng"],
                latitude=city_info["lat"]
            )
            cities.append(city)
        batch_insert("cities", cities)
        city_ids = [c["_id"] for c in db.cities.find({"countryId": country_id}, {"_id": 1})]
        city_map[iso] = city_ids

    # Users
    users = []
    user_ids = []
    now = datetime.utcnow() + timedelta(days=90)
    start = now - timedelta(days=4*365)
    for _ in range(NB_USERS):
        iso = random.choice(list(iso_map.keys()))
        country_id = iso_map[iso]
        city_id = random.choice(city_map[iso])
        u = User(
            fullName=fake.name(),
            email=fake.unique.email(),
            phoneNumber=fake.phone_number(),
            registrationDate=random_datetime(start, now),
            countryId=country_id,
            cityId=city_id
        )
        users.append(u)
    batch_insert("users", users)
    user_ids = [doc["_id"] for doc in db.users.find({}, {"_id": 1})]

    # Drivers
    # Générer les drivers à partir des users existants, en copiant tous les champs obligatoires
    drivers = []
    driver_user_docs = list(db.users.find(
        {}, 
                            {"_id":1, 
                                "fullName":1, "email":1, "phoneNumber":1,
                                "registrationDate":1, "countryId":1, "cityId":1
                            }
                            )
                    )
    random.shuffle(driver_user_docs)
    # Limite au nombre demandé
    for user_doc in driver_user_docs[:NB_DRIVERS]:
        d = Driver(
            fullName=user_doc["fullName"],
            email=user_doc["email"],
            phoneNumber=user_doc["phoneNumber"],
            registrationDate=user_doc["registrationDate"],
            countryId=user_doc["countryId"],
            cityId=user_doc["cityId"],
            userId=user_doc["_id"],
            status = random.choice(["active","inactive","suspended","banned"]),
            licenseNumber=fake.bothify("??-########")
        )
        drivers.append(d)
    batch_insert("drivers", drivers)
    driver_ids = [doc["_id"] for doc in db.drivers.find({}, {"_id":1})]

    # Vehicles
    vehicles = []
    for _ in range(NB_VEHICLES):
        driver_id = random.choice(driver_ids)
        v = Vehicle(
            licensePlate=fake.bothify("??-###-??"),
            brand=fake.company(),
            model=fake.word().title(),
            year=random.randint(2015,2025),
            mileageKm=random.randint(0,100000),
            type=random.choice(["car", "bike", "tricycle", "van"]),
            status=random.choice(["active","maintenance","decommissioned","sold"]),
            driverId=driver_id,
            acquisitionDate=random_datetime(start, now)
        )
        vehicles.append(v)
    batch_insert("vehicles", vehicles)
    vehicle_ids = [doc["_id"] for doc in db.vehicles.find({}, {"_id":1})]


    # 1. user_id -> registrationDate
    user_reg = {
        doc["_id"]: doc["registrationDate"]
        for doc in db.users.find({}, {"_id":1, "registrationDate":1})
    }

    # 2. driver_id -> registrationDate
    driver_reg = {
        doc["_id"]: doc["registrationDate"]
        for doc in db.drivers.find({}, {"_id":1, "registrationDate":1})
    }

    # 3. vehicle_id -> acquisitionDate
    vehicle_reg = {
        doc["_id"]: doc["acquisitionDate"]
        for doc in db.vehicles.find({}, {"_id":1, "acquisitionDate":1})
    }


    # Trips
    trips = []
    now = datetime.utcnow() + timedelta(days=60)
    start = now - timedelta(days=2*365)
    global_start = now - timedelta(days=2*365)

    for _ in range(NB_TRIPS):
        u_id = random.choice(user_ids)
        d_id = random.choice(driver_ids)
        v_id = random.choice(vehicle_ids)

        # date minimale = max(start global, user, driver, véhicule)
        earliest = max(
            global_start,
            user_reg[u_id],
            driver_reg[d_id],
            vehicle_reg[v_id]
        )

        # on génère requestedAt après earliest
        req = random_datetime(earliest, now + timedelta(days=60))
        acc = req + timedelta(seconds=random.randint(60,600))
        st  = acc + timedelta(seconds=random.randint(60,300))
        en  = st + timedelta(seconds=random.randint(600,3600))
        
        amount = random.triangular(500,5000,2000)
        currency = random.choice(["XOF","NGN","KES","GHS","XAF","CDF","SLL"])
        serviceType = random.choice(["ride","delivery","rental"])
        t = Trip(
            serviceType=serviceType,
            userId=u_id,
            driverId=d_id,
            vehicleId=v_id,
            origin={"type":"Point","coordinates":[float(fake.longitude()),float(fake.latitude())]},
            destination={"type":"Point","coordinates":[float(fake.longitude()),float(fake.latitude())]},
            requestedAt=req,
            acceptedAt=acc,
            startedAt=st,
            endedAt=en,
            status="completed",
            currency=currency, 
            amount=amount,
            fare={
                "amount":amount,
                "currency":currency,
                "breakdown":{"base":random.triangular(50,amount//4,amount//2),
                "distance":random.triangular(500,amount*3//4,amount*3//2),
                "time":random.triangular(50,amount//4,amount//2)}
                },
            serviceDetails={
                "rentalDurationMins": None,
                "packageWeightKg": None if serviceType != "delivery" else random.triangular(1,50,10)
            }
        )
        trips.append(t)
    batch_insert("trips", trips)
    trip_docs = list(db.trips.find({}, {"_id":1, "userId":1, "driverId":1}))

    # Ratings
    ratings = []
    for trip_doc in trip_docs:
        # Pour chaque trip, on génère une note user->driver et driver->user
        ratings.append(Rating(
            tripId=trip_doc["_id"],
            givenBy="user",
            toType="driver",
            toId=trip_doc["driverId"],
            givenById=trip_doc["userId"],
            stars=random.randint(1,5),
            comment=fake.sentence(nb_words=10),
            createdAt=fake.date_time_between(start_date="-5y", end_date="+2M", tzinfo=timezone.utc)
        ))
        ratings.append(Rating(
            tripId=trip_doc["_id"],
            givenBy="driver",
            givenById=trip_doc["driverId"],
            toType="user",
            toId=trip_doc["userId"],
            stars=random.randint(1,5),
            comment=fake.sentence(nb_words=10),
            createdAt=fake.date_time_between(start_date="-5y", end_date="+2M", tzinfo=timezone.utc)
        ))
    batch_insert("ratings", ratings)

    # Maintenance
    maints = []
    for _ in range(NB_MAINTENANCE):
        vid = random.choice(vehicle_ids)
        st = random_datetime(start, now)
        en = st + timedelta(hours=random.randint(1,72))
        m = MaintenanceRecord(
            vehicleId=vid,
            type=random.choice(["repair","routine_check","replacement"]),
            cost=random.randint(5000,50000),
            reportedAt= st - timedelta(hours=random.randint(1,72)),
            startDate= st,
            endDate= en,
            description=fake.sentence(nb_words=6)
        )
        maints.append(m)
    batch_insert("maintenance", maints)

    logger.info("Database seeding complete.")

if __name__ == "__main__":
    main()