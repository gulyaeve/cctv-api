import aio_pika
from faststream.rabbit import RabbitQueue, RabbitExchange, ExchangeType
from app.config import settings, broker


async def declare_exchange_and_queue():
    queue = RabbitQueue(settings.QUEUE_NAME, auto_delete=True)
    exchange = RabbitExchange(settings.EXCHANGE_NAME, ExchangeType.FANOUT)

    queue_add_camera = RabbitQueue("add_camera", auto_delete=False, routing_key="camera.add.*")
    queue_remove_camera = RabbitQueue("remove_camera", auto_delete=False, routing_key="camera.remove.*")
    queue_update_camera = RabbitQueue("update_camera", auto_delete=False, routing_key="camera.update.*")

    camera_exchange = RabbitExchange(settings.CAMERA_EXCHANGE_NAME, ExchangeType.TOPIC, auto_delete=False)

    async with broker:
        tg_queue: aio_pika.RobustQueue = await broker.declare_queue(queue)
        tg_exchange: aio_pika.RobustExchange = await broker.declare_exchange(exchange)

        await tg_queue.bind(exchange=tg_exchange)

        camera_add_queue: aio_pika.RobustQueue = await broker.declare_queue(queue_add_camera)
        camera_remove_queue: aio_pika.RobustQueue = await broker.declare_queue(queue_remove_camera)
        camera_update_queue: aio_pika.RobustQueue = await broker.declare_queue(queue_update_camera)

        camera_exchange: aio_pika.RobustExchange = await broker.declare_exchange(exchange)

        await camera_add_queue.bind(exchange=camera_exchange)
        await camera_remove_queue.bind(exchange=camera_exchange)
        await camera_update_queue.bind(exchange=camera_exchange)
