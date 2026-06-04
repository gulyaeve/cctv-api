from datetime import datetime
from typing import Sequence, Annotated
from fastapi import APIRouter, Depends, Query, status

from app.groups.schemas import GroupScheme, GroupSearch, GroupAddScheme, GroupUpdateScheme
from app.groups.dao import GroupsDAO
from app.exceptions import ObjectMissingException
from app.users.dependencies import permission_required
# from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    dependencies=[Depends(permission_required("groups"))]
)


@router.get("", response_model=Sequence[GroupScheme])
# @cache(expire=60)
async def get_all_groups(filter_query: Annotated[GroupSearch, Query()]):
    """
    Get all groups
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await GroupsDAO.find_all(**filter_model)


@router.get("/{id}", response_model=GroupScheme)
async def get_group(id: int):
    item = await GroupsDAO.find_one_or_none(id=id)
    if item is None:
        raise ObjectMissingException
    else:
        return item
    

@router.get("/{id}/schedule")
async def get_schedule_for_group(id: int, timestamp: datetime = datetime.now()):
    item = await GroupsDAO.find_schedule_for_group(id, timestamp)
    if item is None:
        raise ObjectMissingException
    else:
        return item


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("group_create"))]
)
async def add_group(data: GroupAddScheme):
    """
    Add group
    """
    await GroupsDAO.add(
        **data.model_dump()
    )


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("group_create"))]
)
async def bulk_add_groups(items: Sequence[GroupAddScheme]):
    await GroupsDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("group_delete"))]
)
async def del_group(id: int):
    """
    Удалить group
    """
    existing_object = await GroupsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await GroupsDAO.delete(id=id)


@router.patch(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(permission_required("group_create"))]
)
async def update_groups(id: int, data: GroupUpdateScheme):
    """
    update group
    """
    await GroupsDAO.update(id, **data.model_dump(exclude_unset=True))
    
