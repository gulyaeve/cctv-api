from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, Query, status

from app.schedule.dao import ScheduleDAO
from app.schedule.schemas import ScheduleAddScheme, ScheduleScheme, ScheduleSearch
from app.exceptions import ObjectMissingException
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel


router = APIRouter(
    prefix="/schedule",
    tags=["Расписание"],
    dependencies=[Depends(permission_required("schedule"))]
)


@router.get("/active_monitoring")
async def get_active_monitoring(current_user: UserModel = Depends(get_current_user)):
    schedule_for_monitoring = await ScheduleDAO.get_schedule_for_active_monitoring(visor_id=(current_user.id))
    return schedule_for_monitoring


@router.get("", response_model=Sequence[ScheduleScheme])
# @cache(expire=60)
async def get_all_schedules(filter_query: Annotated[ScheduleSearch, Query()]):
    """
    Get all classrooms
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await ScheduleDAO.find_all(**filter_model)


@router.get("/{id}", response_model=ScheduleScheme)
async def get_schedule(id: int):
    schedule = await ScheduleDAO.find_one_or_none(id=id)
    if schedule is None:
        raise ObjectMissingException
    else:
        return schedule


@router.post(
    "",
    response_model=ScheduleScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("schedule_create"))]
)
async def add_schedule(data: ScheduleAddScheme):
    """
    Add schedule
    """
    new_object = await ScheduleDAO.add(
        **data.model_dump()
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("schedule_create"))]
)
async def bulk_add_schedules(items: Sequence[ScheduleAddScheme]) -> Sequence[ScheduleScheme]:
    return await ScheduleDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("schedule_delete"))]
)
async def del_schedule(id: int):
    existing_object = await ScheduleDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await ScheduleDAO.delete(id=id)


@router.put(
    "/{id}",
    response_model=ScheduleScheme,
    dependencies=[Depends(permission_required("schedule_create"))]
)
async def update_schedule(id: int, data: ScheduleAddScheme):

    existing_object = await ScheduleDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await ScheduleDAO.update(id, **data.model_dump())
        return updated_object


    
