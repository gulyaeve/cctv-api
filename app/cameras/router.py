from typing import Annotated, Sequence
from fastapi import APIRouter, Query, status

from app.cameras.dao import CamerasDAO
from app.cameras.schemas import CameraAddScheme, CameraScheme, CameraSearch
from app.exceptions import ObjectMissingException


router = APIRouter(
    prefix="/cameras",
    tags=["Камеры"]
)


@router.get("", response_model=Sequence[CameraScheme])
# @cache(expire=60)
async def get_all_cameras(filter_query: Annotated[CameraSearch, Query()]):
    """
    Get all cameras
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await CamerasDAO.find_all(**filter_model)


@router.post("", response_model=CameraScheme, status_code=status.HTTP_201_CREATED)
async def add_camera(data: CameraAddScheme):
    """
    Add camera
    """
    new_object = await CamerasDAO.add(
        **data.model_dump()
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_camera(id: int):
    """
    Удалить camera
    """
    existing_object = await CamerasDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await CamerasDAO.delete(id=id)


@router.put("/{id}", response_model=CameraScheme)
async def update_camera(id: int, data: CameraAddScheme):
    """
    update camera
    """
    existing_object = await CamerasDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await CamerasDAO.update(id, **data.model_dump())
        return updated_object
    
