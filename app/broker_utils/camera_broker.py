from typing import Literal

from app.cameras.schemas import CameraScheme
from app.config import broker, settings


async def camera_broker_sender(camera_data: CameraScheme, action: Literal["add", "remove", "update"]):
    async with broker:
        await broker.publish(
            camera_data,
            exchange=settings.CAMERA_EXCHANGE_NAME,
            routing_key=f"camera.{action}.{camera_data.id}"
        )