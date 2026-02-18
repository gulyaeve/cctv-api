from datetime import datetime
import logging
from typing import Sequence, Annotated
from fastapi import APIRouter, Query, status, Depends

from app.broker_utils.incident_tg import message_to_tg
from app.cameras.dao import CamerasDAO
from app.incidents.models import IncidentModel
from app.incidents.schemas import IncidentAppendScheme, IncidentScheme, IncidentSearch
from app.incidents.dao import IncidentsDAO
from app.exceptions import ObjectMissingException
from app.users.dependencies import get_current_user
from app.users.models import UserModel
from app.camera_utils.streaming import Camera
# from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.get("/schedule/{id}")
async def get_active_monitoring(id: int, current_user: UserModel = Depends(get_current_user)):
    schedule_for_monitoring = await IncidentsDAO.get_incidents_info(visor_id=current_user.id, event_id=id)
    return schedule_for_monitoring


@router.get("", response_model=Sequence[IncidentScheme])
# @cache(expire=60)
async def get_all_incidents(filter_query: Annotated[IncidentSearch, Query()]):
    """
    Get all incidents
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await IncidentsDAO.find_all(**filter_model)


@router.get("/{id}", response_model=IncidentScheme)
async def get_incident(id: int):
    item = await IncidentsDAO.find_one_or_none(id=id)
    if item is None:
        raise ObjectMissingException
    else:
        return item


@router.post("", response_model=IncidentScheme, status_code=status.HTTP_201_CREATED)
async def add_incident(data: IncidentAppendScheme):
    """
    Add incident with cameras
    """
    screenshot_dir = "app/static/screenshots"
    data_to_save = data.model_dump()
    if data.cameras_ids:
        filenames = []
        for camera in data.cameras_ids:
            filename = f"{data.event}_{camera}_{datetime.now().strftime('%d.%m.%Y_%T')}.jpg"
            filenames.append(f"{filename}")
        data_to_save["cameras_screenshots"] = filenames

    new_object: IncidentModel = await IncidentsDAO.add(
        **data_to_save
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        if data.cameras_ids:
            for camera, filename in zip(data.cameras_ids, filenames):
                camera_data = await CamerasDAO.find_one_or_none(id=camera)
                if camera_data:
                    camera_rtsp = camera_data.rtsp_url
                    frame = Camera(camera_rtsp)
                    frame.save_screenshot(f"{screenshot_dir}/{filename}")
        data = await IncidentsDAO.get_incident_full_info(new_object.id)
        # logging.info(f"{data}")
        # await message_to_tg(data) # TODO: Fix broker
        return new_object


@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_add_incidents(items: Sequence[IncidentAppendScheme]):
    await IncidentsDAO.add_bulk([item.model_dump() for item in items])


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_incident(id: int):
    """
    Удалить incident
    """
    existing_object = await IncidentsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await IncidentsDAO.delete(id=id)


@router.put("/{id}", response_model=IncidentScheme)
async def update_incident(id: int, data: IncidentAppendScheme):
    """
    update group
    """
    existing_object = await IncidentsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await IncidentsDAO.update(id, **data.model_dump())
        return updated_object
    
