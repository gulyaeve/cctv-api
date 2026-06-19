import aio_pika
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange, ExchangeType
from app.config import settings


async def declare_exchange_and_queue(broker: RabbitBroker):
    # queues for image and messages
    queue_max = RabbitQueue(settings.QUEUE_NAME_MAX, auto_delete=False)
    queue_tg = RabbitQueue(settings.QUEUE_NAME_TG, auto_delete=False)
    queue_img = RabbitQueue(settings.QUEUE_NAME, auto_delete=False)

    # exchanges for image and messages
    exchange_out = RabbitExchange(settings.EXCHANGE_NAME_OUTPUT, ExchangeType.FANOUT)
    exchange_in = RabbitExchange(settings.EXCHANGE_NAME_INPUT, ExchangeType.DIRECT)

    # queues for ai
    queue_ai_object = RabbitQueue(settings.QUEUE_NAME_AI_TASK, auto_delete=False)

    # exchanges for ai
    exchange_ai_object = RabbitExchange(settings.EXCHANGE_NAME_AI)


    async with broker:

        img_queue: aio_pika.RobustQueue = await broker.declare_queue(queue_img)
        img_exchange: aio_pika.RobustExchange = await broker.declare_exchange(exchange_in)
        await img_queue.bind(exchange=img_exchange)

        msg_exchange: aio_pika.RobustExchange = await broker.declare_exchange(exchange_out)
        max_queue: aio_pika.RobustQueue = await broker.declare_queue(queue_max)
        tg_queue: aio_pika.RobustQueue = await broker.declare_queue(queue_tg)

        await max_queue.bind(exchange=msg_exchange)
        await tg_queue.bind(exchange=msg_exchange)

        ai_rq_queue: aio_pika.RobustQueue = await broker.declare_queue(queue_ai_object)
        ai_re_exhange: aio_pika.RobustExchange = await broker.declare_exchange(exchange_ai_object)
        await ai_rq_queue.bind(exchange=ai_re_exhange)
        
