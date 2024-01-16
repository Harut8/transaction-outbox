from models import OutboxMessage
from publisher import OutBoxPublisher


class OutBoxService:

    @staticmethod
    async def save(msg: dict, routing_key: str, session):
        outbox = OutboxMessage(payload=msg, routing_key=routing_key)
        session.add(outbox)
        await session.commit()

    @staticmethod
    async def publish_messages(msg_payload, routing_key):
        await OutBoxPublisher.publish(msg_payload, routing_key)
