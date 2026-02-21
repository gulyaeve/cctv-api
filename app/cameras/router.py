from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, Query, status

from app.cameras.dao import CamerasDAO
from app.cameras.schemas import CameraAddScheme, CameraScheme, CameraSearch
from app.exceptions import ObjectMissingException
from app.users.dependencies import permission_required


router = APIRouter(
    prefix="/cameras",
    tags=["Камеры"],
    dependencies=[Depends(permission_required("cameras"))]
)


@router.get("", response_model=Sequence[CameraScheme])
# @cache(expire=60)
async def get_all_cameras(filter_query: Annotated[CameraSearch, Query()]):
    """
    Get all cameras
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await CamerasDAO.find_all(**filter_model)


@router.get("/{id}", response_model=CameraScheme)
async def get_camera(id: int):
    camera = await CamerasDAO.find_one_or_none(id=id)
    if camera is None:
        raise ObjectMissingException
    else:
        return camera


@router.post(
    "",
    response_model=CameraScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("camera_create"))]
)
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


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("camera_create"))]
)
async def bulk_add_cameras(items: Sequence[CameraAddScheme]) -> Sequence[CameraScheme]:
    return await CamerasDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("camera_delete"))]
)
async def del_camera(id: int):
    """
    Удалить camera
    """
    existing_object = await CamerasDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await CamerasDAO.delete(id=id)


@router.put(
    "/{id}",
    response_model=CameraScheme,
    dependencies=[Depends(permission_required("camera_create"))]
)
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
    
