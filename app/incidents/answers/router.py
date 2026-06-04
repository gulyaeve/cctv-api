from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, Query, status

from app.incidents.answers.dao import IncidentAnswerDAO
from app.incidents.answers.schemas import IncidentAnswerAddScheme, IncidentAnswerScheme, IncidentAnswerSearch, IncidentAnswerUpdateScheme
from app.exceptions import ObjectMissingException
from app.users.dependencies import permission_required


router = APIRouter(
    prefix="/answers",
    # tags=["Типы инцидентов"],
    dependencies=[Depends(permission_required("incidents"))]
)


@router.get("", response_model=Sequence[IncidentAnswerScheme])
# @cache(expire=60)
async def get_all_incident_answers(filter_query: Annotated[IncidentAnswerSearch, Query()]):
    """
    Get all incident answers
    """
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await IncidentAnswerDAO.find_all(**filter_model)


@router.get("/{id}", response_model=IncidentAnswerScheme)
async def get_incident_answer(id: int):
    incident_answer = await IncidentAnswerDAO.find_one_or_none(id=id)
    if incident_answer is None:
        raise ObjectMissingException
    else:
        return incident_answer


@router.post(
    "",
    response_model=IncidentAnswerScheme,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(permission_required("incident_create"))]
)
async def add_incident_answer(data: IncidentAnswerAddScheme):
    """
    Add incident answer
    """
    new_object = await IncidentAnswerDAO.add(
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
async def bulk_add_incident_answers(items: Sequence[IncidentAnswerAddScheme]) -> Sequence[IncidentAnswerScheme]:
    return await IncidentAnswerDAO.add_bulk([item.model_dump() for item in items])


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(permission_required("incident_delete"))]
)
async def del_incident_answer(id: int):
    """
    Удалить incident answer
    """
    existing_object = await IncidentAnswerDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        return await IncidentAnswerDAO.delete(id=id)


@router.patch(
    "/{id}",
    response_model=IncidentAnswerScheme,
    dependencies=[Depends(permission_required("incident_create"))]
)
async def update_incident_answer(id: int, data: IncidentAnswerUpdateScheme):
    """
    update incident answer
    """
    existing_object = await IncidentAnswerDAO.find_one_or_none(id=id)
    if existing_object is None:
        raise ObjectMissingException
    else:
        updated_object = await IncidentAnswerDAO.update(id, **data.model_dump(exclude_unset=True))
        return updated_object
    
