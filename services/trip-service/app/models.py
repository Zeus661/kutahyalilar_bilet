from sqlalchemy import Column, String, Integer, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

import sys
sys.path.insert(0, "/shared")
from shared.models import Base, TimestampMixin


class Route(Base, TimestampMixin):
    __tablename__ = "routes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    distance_km = Column(Integer)
    estimated_duration_min = Column(Integer)


class Bus(Base, TimestampMixin):
    __tablename__ = "buses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plate = Column(String(20), unique=True, nullable=False)
    total_seats = Column(Integer, nullable=False, default=45)
    bus_type = Column(String(50))


class Trip(Base, TimestampMixin):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    route_id = Column(UUID(as_uuid=True), ForeignKey("routes.id"), nullable=False)
    bus_id = Column(UUID(as_uuid=True), ForeignKey("buses.id"), nullable=False)
    departure_time = Column(DateTime(timezone=True), nullable=False)
    arrival_time = Column(DateTime(timezone=True), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    available_seats = Column(Integer, nullable=False)
    status = Column(String(20), default="scheduled")


class Seat(Base, TimestampMixin):
    __tablename__ = "seats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id"), nullable=False)
    seat_number = Column(Integer, nullable=False)
    is_reserved = Column(Boolean, default=False)
    gender_restriction = Column(String(10), nullable=True)
