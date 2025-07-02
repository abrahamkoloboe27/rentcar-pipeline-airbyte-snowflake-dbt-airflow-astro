# create_indexes.py

import os
import logging
#from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING, GEOSPHERE

# -------------- LOAD ENV --------------
#load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/ride_share")
DB_NAME = os.getenv("DB_NAME", None)  # si tu veux un nom explicite, sinon on prend la DB dans URI

# -------------- LOGGING SETUP --------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



def generate_index() : 
    # -------------- CONNECT --------------
    client = MongoClient(MONGO_URI)
    db = client.get_default_database() if DB_NAME is None else client[DB_NAME]
    logger.info(f"Connected to DB: {db.name}")

    # -------------- INDEX CREATION --------------

    # countries: ISO code unique
    db.countries.create_index(
        [("isoCode", ASCENDING)],
        unique=True,
        name="idx_countries_isoCode"
    )
    logger.info("Created index idx_countries_isoCode on countries(isoCode)")

    # users: email unique, phoneNumber unique, countryId
    db.users.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="idx_users_email"
    )
    logger.info("Created index idx_users_email on users(email)")

    db.users.create_index(
        [("phoneNumber", ASCENDING)],
        unique=True,
        name="idx_users_phoneNumber"
    )
    logger.info("Created index idx_users_phoneNumber on users(phoneNumber)")

    db.users.create_index(
        [("countryId", ASCENDING)],
        name="idx_users_countryId"
    )
    logger.info("Created index idx_users_countryId on users(countryId)")

    # drivers: userId unique, licenseNumber unique, status
    db.drivers.create_index(
        [("userId", ASCENDING)],
        unique=True,
        name="idx_drivers_userId"
    )
    logger.info("Created index idx_drivers_userId on drivers(userId)")

    db.drivers.create_index(
        [("licenseNumber", ASCENDING)],
        unique=True,
        name="idx_drivers_licenseNumber"
    )
    logger.info("Created index idx_drivers_licenseNumber on drivers(licenseNumber)")

    db.drivers.create_index(
        [("status", ASCENDING)],
        name="idx_drivers_status"
    )
    logger.info("Created index idx_drivers_status on drivers(status)")

    # vehicles: licensePlate unique, driverId, status
    db.vehicles.create_index(
        [("licensePlate", ASCENDING)],
        unique=True,
        name="idx_vehicles_licensePlate"
    )
    logger.info("Created index idx_vehicles_licensePlate on vehicles(licensePlate)")

    db.vehicles.create_index(
        [("driverId", ASCENDING)],
        name="idx_vehicles_driverId"
    )
    logger.info("Created index idx_vehicles_driverId on vehicles(driverId)")

    db.vehicles.create_index(
        [("status", ASCENDING)],
        name="idx_vehicles_status"
    )
    logger.info("Created index idx_vehicles_status on vehicles(status)")

    # trips: geo indexes + foreign keys + status/serviceType
    db.trips.create_index(
        [("origin", GEOSPHERE)],
        name="idx_trips_origin_geo"
    )
    logger.info("Created geospatial index idx_trips_origin_geo on trips(origin)")

    db.trips.create_index(
        [("destination", GEOSPHERE)],
        name="idx_trips_destination_geo"
    )
    logger.info("Created geospatial index idx_trips_destination_geo on trips(destination)")

    db.trips.create_index(
        [("userId", ASCENDING)],
        name="idx_trips_userId"
    )
    logger.info("Created index idx_trips_userId on trips(userId)")

    db.trips.create_index(
        [("driverId", ASCENDING)],
        name="idx_trips_driverId"
    )
    logger.info("Created index idx_trips_driverId on trips(driverId)")

    db.trips.create_index(
        [("vehicleId", ASCENDING)],
        name="idx_trips_vehicleId"
    )
    logger.info("Created index idx_trips_vehicleId on trips(vehicleId)")

    db.trips.create_index(
        [("serviceType", ASCENDING), ("status", ASCENDING)],
        name="idx_trips_service_status"
    )
    logger.info("Created compound index idx_trips_service_status on trips(serviceType, status)")

    # ratings: tripId, raterId, rateeId, stars descending
    db.ratings.create_index(
        [("tripId", ASCENDING)],
        name="idx_ratings_tripId"
    )
    logger.info("Created index idx_ratings_tripId on ratings(tripId)")

    db.ratings.create_index(
        [("raterId", ASCENDING)],
        name="idx_ratings_raterId"
    )
    logger.info("Created index idx_ratings_raterId on ratings(raterId)")

    db.ratings.create_index(
        [("rateeId", ASCENDING)],
        name="idx_ratings_rateeId"
    )
    logger.info("Created index idx_ratings_rateeId on ratings(rateeId)")

    db.ratings.create_index(
        [("stars", DESCENDING)],
        name="idx_ratings_stars_desc"
    )
    logger.info("Created index idx_ratings_stars_desc on ratings(stars)")

    # maintenance: vehicleId, reportedAt, status
    db.maintenance.create_index(
        [("vehicleId", ASCENDING)],
        name="idx_maintenance_vehicleId"
    )
    logger.info("Created index idx_maintenance_vehicleId on maintenance(vehicleId)")

    db.maintenance.create_index(
        [("reportedAt", DESCENDING)],
        name="idx_maintenance_reportedAt_desc"
    )
    logger.info("Created index idx_maintenance_reportedAt_desc on maintenance(reportedAt)")

    db.maintenance.create_index(
        [("status", ASCENDING)],
        name="idx_maintenance_status"
    )
    logger.info("Created index idx_maintenance_status on maintenance(status)")

    logger.info("All indexes created successfully.")
