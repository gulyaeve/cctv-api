from typing import Sequence, Annotated
from fastapi import APIRouter, Depends, Query, status

from app.teachers.schemas import TeacherScheme, TeacherSearch, TeacherBaseScheme
from app.teachers.dao import TeachersDAO
from app.exceptions import ObjectMissingException
from app.users.dependencies import permission_required
# from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
    dependencies=[Depends(permission_required("teachers"))]
)


@router.get("", response_model=Sequence[TeacherScheme])
# @cache(expire=60)
async def get_all_teachers(filter_query: Annotated[TeacherSearch, Query()]):
    """
    Get all teachers
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await TeachersDAO.find_all(**filter_model)


@router.get("/{id}", response_model=TeacherScheme)
async def get_teacher(id: int):
    teacher = await TeachersDAO.find_one_or_none(id=id)
    if teacher is None:
        raise ObjectMissingException
    else:
        return teacher


@router.post(
    "",
    response_model=TeacherScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("teacher_create"))]
)
async def add_teacher(data: TeacherBaseScheme):
    """
    Add teacher
    """
    new_object = await TeachersDAO.add(
        **data.model_dump()
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("teacher_create"))]
)
async def bulk_add_teachers(items: Sequence[TeacherBaseScheme]) -> Sequence[TeacherScheme]:
    return await TeachersDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("teacher_delete"))]
)
async def del_teacher(id: int):
    """
    Удалить teacher
    """
    existing_object = await TeachersDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await TeachersDAO.delete(id=id)


@router.put(
    "/{id}",
    response_model=TeacherScheme,
    dependencies=[Depends(permission_required("teacher_create"))]
)
async def update_teacher(id: int, data: TeacherBaseScheme):
    """
    update teacher
    """
    existing_object = await TeachersDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await TeachersDAO.update(id, **data.model_dump())
        return updated_object
    
