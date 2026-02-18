import aio_pika
from faststream.rabbit import RabbitQueue, RabbitExchange, ExchangeType
from app.config import settings, broker


async def declare_exchange_and_queue():
    queue = RabbitQueue(settings.QUEUE_NAME, auto_delete=True)
    exchange = RabbitExchange(settings.EXCHANGE_NAME, ExchangeType.FANOUT)

    async with broker:
        tg_queue: aio_pika.RobustQueue = await broker.declare_queue(queue)
        tg_exchange: aio_pika.RobustExchange = await broker.declare_exchange(exchange)

        await tg_queue.bind(exchange=tg_exchange)
