from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, Query

from app.ai_analysis.dao import AiAnalysisDAO
from app.ai_analysis.schemas import AiAnalysisAddScheme, AiAnalysisScheme, AiAnalysisSearchScheme
from app.exceptions import ObjectMissingException
from app.users.auth import auth_bearer_token


router = APIRouter(
    prefix="/ai_analysis",
    tags=["AI анализ"],
    # dependencies=[Depends(auth_bearer_token)]
)


@router.get("", response_model=Sequence[AiAnalysisScheme])
# @cache(expire=60)
async def get_all_ai_analysis(filter_query: Annotated[AiAnalysisSearchScheme, Query()]):
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await AiAnalysisDAO.find_all(**filter_model)


@router.get("/{id}", response_model=AiAnalysisScheme)
async def get_ai_analysis(id: int):
    ai_analysis = await AiAnalysisScheme.find_one_or_none(id=id)
    if ai_analysis is None:
        raise ObjectMissingException
    else:
        return ai_analysis
    

@router.post("", response_model=AiAnalysisScheme, dependencies=[Depends(auth_bearer_token)], status_code=201)
async def add_ai_analysis(data: AiAnalysisAddScheme):
    new_object = await AiAnalysisDAO.add(**data.model_dump())
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object