from sqlalchemy import Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid

import sys
sys.path.insert(0, "/shared")
from shared.models import Base, TimestampMixin


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="TRY")
    method = Column(String(20))
    status = Column(String(20), default="pending")
    mock_card_last4 = Column(String(4))
    failure_reason = Column(String(255), nullable=True)
