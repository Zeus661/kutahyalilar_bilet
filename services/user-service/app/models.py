from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid

import sys
sys.path.insert(0, "/shared")
from shared.models import Base, TimestampMixin


class UserProfile(Base, TimestampMixin):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    date_of_birth = Column(Date, nullable=True)
    tc_kimlik = Column(String(11), nullable=True)
    gender = Column(String(10), nullable=True)
