from fastapi import APIRouter, Depends

from app.analytics.dao import AnalyticsDAO
from app.users.dependencies import permission_required


router = APIRouter(
    prefix="/analytics",
    tags=["Аналитика"],
    dependencies=[Depends(permission_required("frontend"))]
)


@router.get("")
async def get_data_for_dashboard():
    incidents = await AnalyticsDAO.get_analytics()
    return incidents