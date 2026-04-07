from fastapi import APIRouter, Depends

from app.ai_analysis.dao import AiAnalysisDAO
from app.ai_analysis.schemas import AiAnalysisAddScheme, AiAnalysisScheme
from app.exceptions import ObjectMissingException
from app.users.auth import auth_bearer_token


router = APIRouter(
    prefix="/ai_analysis",
    tags=["AI анализ"],
    # dependencies=[Depends(auth_bearer_token)]
)


@router.post("", response_model=AiAnalysisScheme, dependencies=[Depends(auth_bearer_token)], status_code=201)
async def add_ai_analysis(data: AiAnalysisAddScheme):
    new_object = await AiAnalysisDAO.add(**data.model_dump())
    if new_object is None:
        raise ObjectMissingException
    else:
        return new_object