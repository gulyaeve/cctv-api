from typing import Sequence
from fastapi import APIRouter, Depends, status

from app.classrooms.type.dao import ClassroomTypeDAO
from app.classrooms.type.schemas import ClassroomTypeAddScheme, ClassroomTypeScheme, ClassroomTypeUpdateScheme
from app.exceptions import ObjectMissingException
from app.users.dependencies import permission_required


router = APIRouter(
    prefix="/types",
    # tags=["Типы кабинетов"],
    dependencies=[Depends(permission_required("classrooms"))]
)


# @router.get("", response_model=Sequence[ClassroomTypeScheme])
@router.get("")
# @cache(expire=60)
async def get_all_classroom_types():
    """
    Get all classroom types
    """
    return await ClassroomTypeDAO.find_all()


@router.get("/{id}", response_model=ClassroomTypeScheme)
async def get_classroom_type(id: int):
    classroom_type = await ClassroomTypeDAO.find_one_or_none(id=id)
    if classroom_type is None:
        raise ObjectMissingException
    else:
        return classroom_type


@router.post(
    "",
    response_model=ClassroomTypeScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("classroom_create"))]
)
async def add_classroom_type(data: ClassroomTypeAddScheme):
    """
    Add classroom type
    """
    new_object = await ClassroomTypeDAO.add(
        **data.model_dump()
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("classroom_create"))]
)
async def bulk_add_classroom_types(items: Sequence[ClassroomTypeAddScheme]) -> Sequence[ClassroomTypeScheme]:
    return await ClassroomTypeDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("classroom_delete"))]
)
async def del_classroom_type(id: int):
    """
    Удалить classroom type
    """
    existing_object = await ClassroomTypeDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await ClassroomTypeDAO.delete(id=id)


@router.patch(
    "/{id}",
    response_model=ClassroomTypeScheme,
    dependencies=[Depends(permission_required("classroom_create"))]
)
async def update_classroom_type(id: int, data: ClassroomTypeUpdateScheme):
    """
    update classroom type
    """
    existing_object = await ClassroomTypeDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await ClassroomTypeDAO.update(id, **data.model_dump(exclude_unset=True))
        return updated_object
    
