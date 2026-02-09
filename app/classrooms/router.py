from typing import Annotated, Sequence
from fastapi import APIRouter, Query, status

from app.classrooms.dao import ClassroomsDAO
from app.classrooms.schemas import ClassroomAddScheme, ClassroomScheme, ClassroomSearch
from app.exceptions import ObjectMissingException


router = APIRouter(
    prefix="/classrooms",
    tags=["Кабинеты"]
)


@router.get("", response_model=Sequence[ClassroomScheme])
# @cache(expire=60)
async def get_all_classrooms(filter_query: Annotated[ClassroomSearch, Query()]):
    """
    Get all classrooms
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await ClassroomsDAO.find_all(**filter_model)


@router.get("/{id}", response_model=ClassroomScheme)
async def get_classroom(id: int):
    classroom = await ClassroomsDAO.find_one_or_none(id=id)
    if classroom is None:
        raise ObjectMissingException
    else:
        return classroom


@router.post("", response_model=ClassroomScheme, status_code=status.HTTP_201_CREATED)
async def add_classroom(data: ClassroomAddScheme):
    """
    Add classroom
    """
    new_object = await ClassroomsDAO.add(
        **data.model_dump()
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_classroom(id: int):
    """
    Удалить здание
    """
    existing_object = await ClassroomsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await ClassroomsDAO.delete(id=id)


@router.put("/{id}", response_model=ClassroomScheme)
async def update_classroom(id: int, data: ClassroomAddScheme):
    """
    update building
    
    :param id: building id
    :type id: int
    :param building: building attributes
    :type building: BuildingAddScheme
    """
    existing_object = await ClassroomsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await ClassroomsDAO.update(id, **data.model_dump())
        return updated_object
    
