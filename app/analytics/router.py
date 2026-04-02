from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.analytics.dao import AnalyticsDAO
from app.analytics.schemas import RequestData
from app.users.dependencies import permission_required


router = APIRouter(
    prefix="/analytics",
    tags=["Аналитика"],
    dependencies=[Depends(permission_required("frontend"))]
)


@router.get("")
async def get_data_for_dashboard(filter_query: Annotated[RequestData, Query()]):
    filter_model = filter_query.model_dump(exclude_unset=True, exclude_defaults=True)
    return await AnalyticsDAO.get_analytics(**filter_model)