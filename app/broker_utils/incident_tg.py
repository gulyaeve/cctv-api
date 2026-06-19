from faststream.rabbit import RabbitBroker

from app.config import settings


async def message_to_tg(data, broker: RabbitBroker):
    async with broker:
        await broker.publish(
            data,

            exchange=settings.EXCHANGE_NAME_INPUT,
            routing_key=settings.QUEUE_NAME,

        )
