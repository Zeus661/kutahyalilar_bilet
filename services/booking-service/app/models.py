from sqlalchemy import Column, String, Integer, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid

import sys
sys.path.insert(0, "/shared")
from shared.models import Base, TimestampMixin


class Booking(Base, TimestampMixin):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    trip_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    seat_id = Column(UUID(as_uuid=True), nullable=False)
    seat_number = Column(Integer, nullable=False)
    passenger_name = Column(String(200), nullable=False)
    passenger_tc = Column(String(11), nullable=False)
    passenger_gender = Column(String(10), nullable=False)
    passenger_dob = Column(Date, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending")
    payment_id = Column(UUID(as_uuid=True), nullable=True)
    ticket_code = Column(String(20), unique=True, nullable=False)
