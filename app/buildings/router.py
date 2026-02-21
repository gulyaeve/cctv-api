from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, Query, status

from app.buildings.dao import BuildingsDAO
from app.buildings.schemas import BuildingAddScheme, BuildingScheme, BuildingSearch
from app.exceptions import ObjectMissingException
from app.users.dependencies import permission_required


router = APIRouter(
    prefix="/buildings",
    tags=["Здания"],
    dependencies=[Depends(permission_required("buildings"))]
    )


@router.get("", response_model=Sequence[BuildingScheme])
# @cache(expire=60)
async def get_all_buildings(filter_query: Annotated[BuildingSearch, Query()]):
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


@router.post(
    "",
    response_model=BuildingScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("building_create"))]
)
async def add_building(building: BuildingAddScheme):
    """
    Add building
    """
    new_building = await BuildingsDAO.add(
        **building.model_dump()
    )
    return new_building


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("building_create"))]
)
async def bulk_add_buildings(items: Sequence[BuildingAddScheme]) -> Sequence[BuildingScheme]:
    return await BuildingsDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("building_delete"))]
)
async def del_buildings(id: int):
    """
    Удалить здание
    """
    existing_building = await BuildingsDAO.find_one_or_none(id=id)
    if not existing_building:
        raise ObjectMissingException
    else:
        return await BuildingsDAO.delete(id=id)


@router.put(
    "/{id}",
    response_model=BuildingScheme,
    dependencies=[Depends(permission_required("building_create"))]
)
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
    
