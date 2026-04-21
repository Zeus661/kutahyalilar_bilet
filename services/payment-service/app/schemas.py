from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import Optional


class PaymentCreate(BaseModel):
    booking_id: UUID
    user_id: UUID
    amount: Decimal
    currency: str = "TRY"
    method: str = "credit_card"
    mock_card_last4: str = "4242"


class PaymentOut(BaseModel):
    id: UUID
    booking_id: UUID
    user_id: UUID
    amount: Decimal
    currency: str
    method: str
    status: str
    mock_card_last4: Optional[str] = None
    failure_reason: Optional[str] = None
    model_config = {"from_attributes": True}


class RefundResponse(BaseModel):
    payment_id: UUID
    status: str
    message: str
