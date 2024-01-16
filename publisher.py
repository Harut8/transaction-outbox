import asyncio
import json

from aio_pika import connect_robust, Message, Channel
from aio_pika.abc import AbstractRobustConnection, DeliveryMode
from aio_pika.pool import Pool


async def get_connection() -> AbstractRobustConnection:
    OutBoxPublisher.connection = await connect_robust(...)
    return OutBoxPublisher.connection


async def get_channel() -> Channel:
    async with OutBoxPublisher.connection_pool.acquire() as connection:
        return await connection.channel()


class OutBoxPublisher:
    connection: AbstractRobustConnection | None = None
    EXCHANGE_NAME = "outbox"

    connection_pool = Pool(
        get_connection,
        max_size=2,
        loop=asyncio.get_event_loop()
    )
    channel_pool = Pool(
        get_channel,
        max_size=2,
        loop=asyncio.get_event_loop()
    )

    @staticmethod
    async def publish(msg: dict, routing_key: str):
        async with OutBoxPublisher.channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(OutBoxPublisher.EXCHANGE_NAME, durable=True)

            ready_queue = await channel.declare_queue(
                routing_key, durable=True
            )
            await ready_queue.bind(exchange, routing_key)
            print(f"Publishing message to {routing_key} queue")
            await exchange.publish(
                Message(
                    body=json.dumps(msg).encode(),
                    delivery_mode=DeliveryMode.PERSISTENT
                ),
                routing_key
            )