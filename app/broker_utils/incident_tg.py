import aio_pika
from faststream.rabbit import RabbitQueue, RabbitExchange, ExchangeType
from app.config import broker, settings


async def declare_exchange_and_queue():
    queue = RabbitQueue(settings.QUEUE_NAME, auto_delete=True)
    exchange = RabbitExchange(settings.EXCHANGE_NAME, ExchangeType.FANOUT)

    tg_queue: aio_pika.RobustQueue = await broker.declare_queue(queue)
    tg_exchange: aio_pika.RobustExchange = await broker.declare_exchange(exchange)

    await tg_queue.bind(exchange=tg_exchange)


async def message_to_tg(data):
    await declare_exchange_and_queue()

    await broker.publish(
        str(data),
        exchange=settings.EXCHANGE_NAME
    )