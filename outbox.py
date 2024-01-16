from models import OutboxMessage, OutboxStatus
from publisher import OutBoxPublisher


class OutBoxService:

    @staticmethod
    async def save(msg: dict, routing_key: str, session):
        outbox = OutboxMessage(payload=msg, routing_key=routing_key, status=OutboxStatus.PENDING)
        session.add(outbox)
        await session.commit()

    @staticmethod
    async def update(msg: OutboxMessage, session):
        msg.status = OutboxStatus.PROCESSED
        await session.commit()

    @staticmethod
    async def publish_messages(msg_payload, routing_key):
        await OutBoxPublisher.publish(msg_payload, routing_key)
