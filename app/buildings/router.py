from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, Query, status

from app.buildings.dao import BuildingsDAO
from app.buildings.schemas import BuildingAddScheme, BuildingScheme, BuildingSearch
from app.exceptions import ObjectMissingException
from app.users.dependencies import get_current_user
from app.users.models import UserModel


router = APIRouter(
    prefix="/buildings",
    tags=["Здания"]
)


@router.get("", response_model=Sequence[BuildingScheme])
# @cache(expire=60)
async def get_all_buildings(filter_query: Annotated[BuildingSearch, Query()], current_user: UserModel = Depends(get_current_user)):
    """
    Get all buildings
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await BuildingsDAO.find_all(**filter_model)


@router.get("/{id}", response_model=BuildingScheme)
async def get_building(id: int):
    building = await BuildingsDAO.find_one_or_none(id=id)
    if building is None:
        raise ObjectMissingException
    else:
        return building


@router.post("", response_model=BuildingScheme, status_code=status.HTTP_201_CREATED)
async def add_building(building: BuildingAddScheme):
    """
    Add building
    """
    new_building = await BuildingsDAO.add(
        **building.model_dump()
    )
    return new_building


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_buildings(id: int):
    """
    Удалить здание
    """
    existing_building = await BuildingsDAO.find_one_or_none(id=id)
    if not existing_building:
        raise ObjectMissingException
    else:
        return await BuildingsDAO.delete(id=id)


@router.put("/{id}", response_model=BuildingScheme)
async def update_building(id: int, building: BuildingAddScheme):
    """
    update building
    
    :param id: building id
    :type id: int
    :param building: building attributes
    :type building: BuildingAddScheme
    """
    existing_building = await BuildingsDAO.find_one_or_none(id=id)
    if not existing_building:
        raise ObjectMissingException
    else:
        updated_building = await BuildingsDAO.update(id, **building.model_dump())
        return updated_building
    
