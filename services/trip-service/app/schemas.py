from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


# Route
class RouteCreate(BaseModel):
    origin: str
    destination: str
    distance_km: Optional[int] = None
    estimated_duration_min: Optional[int] = None


class RouteOut(BaseModel):
    id: UUID
    origin: str
    destination: str
    distance_km: Optional[int] = None
    estimated_duration_min: Optional[int] = None
    model_config = {"from_attributes": True}


# Bus
class BusCreate(BaseModel):
    plate: str
    total_seats: int = 45
    bus_type: Optional[str] = "standard"


class BusOut(BaseModel):
    id: UUID
    plate: str
    total_seats: int
    bus_type: Optional[str] = None
    model_config = {"from_attributes": True}


# Trip
class TripCreate(BaseModel):
    route_id: UUID
    bus_id: UUID
    departure_time: datetime
    arrival_time: datetime
    price: Decimal


class TripOut(BaseModel):
    id: UUID
    route_id: UUID
    bus_id: UUID
    departure_time: datetime
    arrival_time: datetime
    price: Decimal
    available_seats: int
    status: str
    model_config = {"from_attributes": True}


class TripDetail(TripOut):
    seats: List["SeatOut"] = []


# Seat
class SeatOut(BaseModel):
    id: UUID
    trip_id: UUID
    seat_number: int
    is_reserved: bool
    gender_restriction: Optional[str] = None
    model_config = {"from_attributes": True}


class SeatReserveResponse(BaseModel):
    seat_id: UUID
    trip_id: UUID
    seat_number: int
    reserved: bool = True


TripDetail.model_rebuild()
