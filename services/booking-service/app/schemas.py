from pydantic import BaseModel
from uuid import UUID
from datetime import date
from decimal import Decimal
from typing import Optional, List


class BookingCreate(BaseModel):
    trip_id: UUID
    seat_id: UUID
    passenger_name: str
    passenger_tc: str
    passenger_gender: str
    passenger_dob: date


class BookingOut(BaseModel):
    id: UUID
    user_id: UUID
    trip_id: UUID
    seat_id: UUID
    seat_number: int
    passenger_name: str
    passenger_tc: str
    passenger_gender: str
    passenger_dob: date
    total_price: Decimal
    status: str
    payment_id: Optional[UUID] = None
    ticket_code: str
    model_config = {"from_attributes": True}
