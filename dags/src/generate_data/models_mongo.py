from typing import Optional, List, Literal, Union
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from decimal import Decimal


# Classe de base pour accepter ObjectId
class BaseDocument(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }


class Country(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name: str
    isoCode: str
    currency: str
    locale: str


class City(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name: str
    countryId: ObjectId
    longitude: float
    latitude: float


class User(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    fullName: str
    email: str
    phoneNumber: str
    registrationDate: datetime
    countryId: ObjectId
    cityId: ObjectId


class Driver(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    fullName: str
    email: str
    phoneNumber: str
    licenseNumber: str
    status: Literal["active", "inactive", "suspended", "banned"]
    registrationDate: datetime
    countryId: ObjectId
    cityId: ObjectId
    userId: Optional[ObjectId]  # Lien si un driver est aussi user


class Vehicle(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    licensePlate: str
    type : Literal["car", "bike", "tricycle", "van"]
    brand: str
    model: str
    year: int
    mileageKm: int
    status: Literal["active", "maintenance", "decommissioned", "sold"]
    driverId: ObjectId
    acquisitionDate: datetime


class MaintenanceRecord(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    vehicleId: ObjectId
    type: Literal["repair", "routine_check", "replacement"]
    cost: float
    startDate: datetime
    endDate: datetime
    reportedAt: datetime
    description: str


class Trip(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    serviceType: Literal["ride", "rental", "delivery"]
    userId: ObjectId
    driverId: ObjectId
    vehicleId: ObjectId
    origin: dict  # {"type": "Point", "coordinates": [lng, lat]}
    destination: dict
    requestedAt: datetime
    acceptedAt: Optional[datetime]
    startedAt: Optional[datetime]
    endedAt: Optional[datetime]
    status: Literal["requested", "ongoing", "completed", "cancelled"]
    currency: Literal["XOF", "NGN", "KES", "GHS"]
    amount: float
    fare: dict  # {"amount": float, "currency": str, "breakdown": {"base": float, "distance": float, "time": float}}
    serviceDetails: dict  # {"rentalDurationMins": int, "packageWeightKg": float}


class Rating(BaseDocument):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    tripId: ObjectId
    givenBy: Literal["user", "driver"]
    givenById: ObjectId
    toType: Literal["user", "driver", "vehicle"]
    toId: ObjectId
    stars: int = Field(ge=1, le=5)
    comment: Optional[str]
    createdAt: datetime = Field(default_factory=datetime.utcnow)
