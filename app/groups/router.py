from typing import Sequence, Annotated
from fastapi import APIRouter, Query, status

from app.groups.schemas import GroupScheme, GroupSearch, GroupBaseScheme
from app.groups.dao import GroupsDAO
from app.exceptions import ObjectMissingException
# from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
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


@router.post("", response_model=GroupScheme, status_code=status.HTTP_201_CREATED)
async def add_teacher(data: GroupBaseScheme):
    """
    Add group
    """
    new_object = await GroupsDAO.add(
        **data.model_dump()
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.post("/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_add_groups(items: Sequence[GroupBaseScheme]):
    await GroupsDAO.add_bulk([item.model_dump() for item in items])


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_group(id: int):
    """
    Удалить group
    """
    existing_object = await GroupsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await GroupsDAO.delete(id=id)


@router.put("/{id}", response_model=GroupScheme)
async def update_group(id: int, data: GroupBaseScheme):
    """
    update group
    """
    existing_object = await GroupsDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await GroupsDAO.update(id, **data.model_dump())
        return updated_object
    
