from datetime import date
from random import choice
from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi_cache.decorator import cache

from app.broker_utils.schedule_broker import send_ai_job
from app.cameras.dao import CamerasDAO
from app.exceptions import ObjectMissingException, ScheduleNotQuitException
from app.schedule.dao import ScheduleDAO
from app.schedule.schemas import (
    ActiveMonitoringSearch,
    ScheduleAddScheme,
    ScheduleAiSchema,
    ScheduleAiTask,
    ScheduleDaily,
    ScheduleScheme,
    ScheduleSearch,
    ScheduleUpdateScheme,
)

# from app.users.auth import auth_bearer_token
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel

router = APIRouter(
    prefix="/schedule",
    tags=["Расписание"],
    dependencies=[Depends(permission_required("schedule"))],
)


@router.get("/active_monitoring")
async def get_active_monitoring(
    filter_query: Annotated[ActiveMonitoringSearch, Query()],
    current_user: UserModel = Depends(get_current_user),
):
    schedule_for_monitoring = await ScheduleDAO.get_schedule_for_active_monitoring(
        visor_id=(current_user.id),
        building_id=filter_query.building_id,
        classroom_id=filter_query.classroom_id,
        group_id=filter_query.group_id,
        event_type=filter_query.event_type,
    )
    return schedule_for_monitoring


@router.get("", response_model=Sequence[ScheduleScheme])
@cache(expire=60)
async def get_all_schedules(filter_query: Annotated[ScheduleSearch, Query()]):
    """
    Get all schedules
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await ScheduleDAO.find_all(**filter_model)


@router.get("/count")
@cache(expire=60)
async def count_schedules(filter_query: Annotated[ScheduleSearch, Query()]):
    """
    Count all schedules
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await ScheduleDAO.find_all_count(**filter_model)


@router.get("/{id}", response_model=ScheduleScheme)
async def get_schedule(id: int):
    schedule = await ScheduleDAO.find_by_id(id=id)
    if schedule is None:
        raise ObjectMissingException
    else:
        return schedule


@router.post(
    "/{id}/ai_analysis",
    dependencies=[Depends(permission_required("schedule"))],
    status_code=201,
)
async def create_ai_task(
    id: int,
    request: Request,
    query_params: Annotated[ScheduleAiSchema, Form()],
):
    schedule = await ScheduleDAO.find_by_id(id=id)
    if schedule.status != 2:
        raise ScheduleNotQuitException
    if query_params.camera_id is None:
        cameras_data = await CamerasDAO.find_all(classroom_id=schedule.classroom_id)
        cameras = [data.id for data in cameras_data]
        if not cameras:
            raise ObjectMissingException
        camera = choice(cameras)
    else:
        camera = query_params.camera_id
    data_to_analysis = ScheduleAiTask(
        camera_id=camera, id=schedule.id, date=schedule.timestamp_start.date()
    )
    # return data_to_analysis
    await send_ai_job(data_to_analysis, broker=request.app.state.broker)


@router.post(
    "",
    response_model=ScheduleScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("schedule_create"))],
)
async def add_schedule(data: ScheduleAddScheme):
    """
    Add schedule
    """
    new_object = await ScheduleDAO.add(**data.model_dump())
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("schedule_create"))],
)
async def bulk_add_schedules(
    items: Sequence[ScheduleAddScheme],
) -> Sequence[ScheduleScheme]:
    return await ScheduleDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("schedule_delete"))],
)
async def del_schedule(id: int):
    existing_object = await ScheduleDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await ScheduleDAO.delete(id=id)


@router.patch(
    "/{id}",
    response_model=ScheduleScheme,
    dependencies=[Depends(permission_required("schedule_create"))],
)
async def update_schedule(id: int, data: ScheduleUpdateScheme):

    existing_object = await ScheduleDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await ScheduleDAO.update(id, **data.model_dump(exclude_unset=True))
        return updated_object


router_daily = APIRouter(
    prefix="/schedule_daily",
    tags=["Расписание на день"],
)


# TODO: remove after test
# @router_daily.get("", response_model=Sequence[ScheduleDaily], dependencies=[Depends(auth_bearer_token)])
@router_daily.get(
    "", response_model=Sequence[ScheduleDaily], dependencies=[Depends(get_current_user)]
)
async def find_daily_schedule(date: date, building_id: int = 1):
    return await ScheduleDAO.find_by_date(date, building_id)


# router.include_router(router2)
