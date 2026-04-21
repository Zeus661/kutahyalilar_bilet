import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime, timezone, timedelta

from app.models import Payment
from app.schemas import PaymentCreate

import sys
sys.path.insert(0, "/shared")
from shared.exceptions import not_found, bad_request


async def process_payment(db: AsyncSession, data: PaymentCreate) -> Payment:
    success = random.random() < 0.90
    status = "completed" if success else "failed"
    failure_reason = None if success else "Insufficient funds (mock)"

    payment = Payment(
        booking_id=data.booking_id,
        user_id=data.user_id,
        amount=data.amount,
        currency=data.currency,
        method=data.method,
        status=status,
        mock_card_last4=data.mock_card_last4,
        failure_reason=failure_reason,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)

    from shared.kafka_client import get_producer
    topic = "payment.completed" if success else "payment.failed"
    producer = await get_producer()
    try:
        await producer.send_and_wait(topic, {
            "payment_id": str(payment.id),
            "booking_id": str(payment.booking_id),
            "amount": float(payment.amount),
            "status": payment.status,
            "failure_reason": failure_reason,
        })
    finally:
        await producer.stop()

    return payment


async def get_payment(db: AsyncSession, payment_id: UUID) -> Payment:
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        not_found("Payment")
    return payment


async def refund_payment(db: AsyncSession, payment_id: UUID) -> Payment:
    payment = await get_payment(db, payment_id)
    if payment.status != "completed":
        bad_request("Only completed payments can be refunded")

    created_at = payment.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    if now - created_at > timedelta(hours=2):
        bad_request("Refund only allowed within 2 hours of payment")

    payment.status = "refunded"
    await db.commit()
    await db.refresh(payment)
    return payment
