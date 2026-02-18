from app.config import broker, settings


async def message_to_tg(data):
    async with broker:
        await broker.publish(
            str(data),
            exchange=settings.EXCHANGE_NAME
        )
