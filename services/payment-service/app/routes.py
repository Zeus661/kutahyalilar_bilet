from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.dependencies import get_current_user, require_admin
from app.schemas import PaymentCreate, PaymentOut, RefundResponse
from app.service import process_payment, get_payment, refund_payment
from app.database import get_db

router = APIRouter(tags=["payments"])


@router.post("/payments/", response_model=PaymentOut, status_code=201)
async def create_payment(data: PaymentCreate, _user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await process_payment(db, data)


@router.get("/payments/{payment_id}", response_model=PaymentOut)
async def get_payment_detail(payment_id: UUID, _user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_payment(db, payment_id)


@router.post("/payments/{payment_id}/refund", response_model=RefundResponse)
async def refund(payment_id: UUID, _user=Depends(require_admin), db: AsyncSession = Depends(get_db)):
    payment = await refund_payment(db, payment_id)
    return RefundResponse(
        payment_id=payment.id,
        status=payment.status,
        message="Payment refunded successfully"
    )
