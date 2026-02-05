from fastapi import APIRouter

from app.buildings.dao import BuildingsDAO


router = APIRouter(
    prefix="/buildings",
    tags=["Здания"]
)


@router.get("")
async def get_all_buildings():
    buildings = await BuildingsDAO.find_all()
    return buildings