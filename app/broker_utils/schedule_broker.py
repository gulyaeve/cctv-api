from app.config import broker, settings


async def send_ai_job(data):
    async with broker:
        await broker.publish(
            data,

            exchange=settings.EXCHANGE_NAME_AI,
            routing_key=settings.QUEUE_NAME_AI_TASK,

        )