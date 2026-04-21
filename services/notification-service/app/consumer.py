import asyncio
import sys
sys.path.insert(0, "/shared")

from shared.kafka_client import get_consumer
from app.handlers import (
    handle_booking_created,
    handle_booking_cancelled,
    handle_payment_failed,
    handle_user_registered,
)

TOPIC_HANDLERS = {
    "booking.created": handle_booking_created,
    "booking.cancelled": handle_booking_cancelled,
    "payment.failed": handle_payment_failed,
    "user.registered": handle_user_registered,
}


async def consume_topic(topic: str, handler):
    consumer = await get_consumer(topic, f"notification-service-{topic}")
    try:
        async for msg in consumer:
            try:
                await handler(msg.value)
            except Exception as e:
                print(f"Error handling {topic}: {e}")
    finally:
        await consumer.stop()


def start_consumers():
    tasks = []
    for topic, handler in TOPIC_HANDLERS.items():
        tasks.append(asyncio.create_task(consume_topic(topic, handler)))
    return tasks
