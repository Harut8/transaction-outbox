import asyncio
from sqlalchemy import select

from db import DbHelper
from models import OutboxMessage, OutboxStatus
from outbox import OutBoxService
from schedule import celery_app


async def publish_messages_function():
    async with DbHelper.scoped_session() as session:
        stmt = select(OutboxMessage).where(OutboxMessage.status == OutboxStatus.PENDING)
        messages = await session.execute(stmt)
        messages = messages.scalars().all()
        for msg in messages:
            await OutBoxService.publish_messages(msg.payload, msg.routing_key)
            msg.status = OutboxStatus.PROCESSED
            await session.commit()


@celery_app.task(bind=True, name="outbox.publish_messages")
def publish_messages_task(self):
    asyncio.run(publish_messages_function())
