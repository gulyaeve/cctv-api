from datetime import datetime
from app.logger import logger
from typing import Sequence, Annotated
from fastapi import APIRouter, Query, status, Depends

from app.broker_utils.incident_tg import message_to_tg
# from app.cameras.dao import CamerasDAO
from app.incidents.models import IncidentModel
from app.incidents.schemas import IncidentAppendScheme, IncidentFullInfo, IncidentScheme, IncidentSearch
from app.incidents.dao import IncidentsDAO
from app.exceptions import ObjectMissingException
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel
from app.incidents.type.router import router as incident_type_router
# from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
    dependencies=[Depends(permission_required("incidents"))]
)
router.include_router(incident_type_router)


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


@router.get("/count")
# @cache(expire=60)
async def count_incidents(filter_query: Annotated[IncidentSearch, Query()]):
    """
    Count all incidents
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await IncidentsDAO.find_all_count(**filter_model)


@router.get("/{id}", response_model=IncidentFullInfo)
async def get_incident(id: int):
    item = await IncidentsDAO.get_incident_full_info(id=id)
    if item is None:
        raise ObjectMissingException
    else:
        return item


@router.post(
    "",
    response_model=IncidentFullInfo,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("incident_create"))]
)
async def add_incident(data: IncidentAppendScheme):
    """
    Add incident with cameras
    """
    # Save to db, without screenshots
    new_object: IncidentModel = await IncidentsDAO.add(data)
    if new_object is None:
        raise ObjectMissingException
    
    data_to_save = data.model_dump(exclude={"building_id", "incident_types"})
    if data.cameras_ids:
        # Update in db with screenshots paths
        filenames = []
        for camera_id in data.cameras_ids:
            filename = f"{new_object.id}_{data.event}_{camera_id}_{datetime.now().strftime('%d.%m.%Y_%T')}.jpg"
            filenames.append(f"{filename}")
        data_to_save["cameras_screenshots"] = filenames
        await IncidentsDAO.update(new_object.id, **data_to_save)

    incident_full_info = await IncidentsDAO.get_incident_full_info(new_object.id)
    logger.info("created incident", extra=dict(incident_full_info), exc_info=True)
    # Send to messenger
    if new_object.status in [0, 2]:
        incident_full_info = IncidentFullInfo.model_validate(incident_full_info)
        logger.info("send to queue", extra=dict(incident_full_info), exc_info=True)
        await message_to_tg(incident_full_info)
    
    return incident_full_info


# @router.post(
#     "/bulk",
#     status_code=status.HTTP_201_CREATED,
#     dependencies=[Depends(permission_required("incident_create"))]
# )
# async def bulk_add_incidents(items: Sequence[IncidentAppendScheme]) -> Sequence[IncidentScheme]:
#     return await IncidentsDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("incident_delete"))]
)
async def del_incident(id: int):
    """
    Удалить incident
    """
    existing_object = await IncidentsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await IncidentsDAO.delete(id=id)


@router.put(
    "/{id}",
    response_model=IncidentScheme,
    dependencies=[Depends(permission_required("incident_create"))]
)
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
    
