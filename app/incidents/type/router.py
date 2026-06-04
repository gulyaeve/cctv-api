from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, Query, status

from app.incidents.type.dao import IncidentTypeDAO
from app.incidents.type.schemas import IncidentTypeAddScheme, IncidentTypeScheme, IncidentTypeSearch
from app.exceptions import ObjectMissingException
from app.users.dependencies import permission_required


router = APIRouter(
    prefix="/types",
    # tags=["Типы инцидентов"],
    dependencies=[Depends(permission_required("incidents"))]
)


@router.get("", response_model=Sequence[IncidentTypeScheme])
# @cache(expire=60)
async def get_all_incident_types(filter_query: Annotated[IncidentTypeSearch, Query()]):
    """
    Get all incident types
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await IncidentTypeDAO.find_all(**filter_model)


@router.get("/{id}", response_model=IncidentTypeScheme)
async def get_incident_type(id: int):
    incident_type = await IncidentTypeDAO.find_one_or_none(id=id)
    if incident_type is None:
        raise ObjectMissingException
    else:
        return incident_type


@router.post(
    "",
    response_model=IncidentTypeScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("incident_create"))]
)
async def add_incident_type(data: IncidentTypeAddScheme):
    """
    Add incident type
    """
    new_object = await IncidentTypeDAO.add(
        **data.model_dump()
    )
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object


@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("incident_create"))]
)
async def bulk_add_incident_types(items: Sequence[IncidentTypeAddScheme]) -> Sequence[IncidentTypeScheme]:
    return await IncidentTypeDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("incident_delete"))]
)
async def del_incident_type(id: int):
    """
    Удалить incident type
    """
    existing_object = await IncidentTypeDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await IncidentTypeDAO.delete(id=id)


@router.patch(
    "/{id}",
    response_model=IncidentTypeScheme,
    dependencies=[Depends(permission_required("incident_create"))]
)
async def update_incident_type(id: int, data: IncidentTypeAddScheme):
    """
    update incident type
    """
    existing_object = await IncidentTypeDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await IncidentTypeDAO.update(id, **data.model_dump(exclude_unset=True))
        return updated_object
    
