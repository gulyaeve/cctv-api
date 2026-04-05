from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings, get_building
from app.cameras.dao import CamerasDAO
from app.classrooms.dao import ClassroomsDAO
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel


router = APIRouter(
    prefix="/buildings",
    tags=["Корпуса"],
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_buildings_page(
    request: Request,
    buildings: BuildingModel=Depends(get_all_buildings),
    current_user: UserModel = Depends(get_current_user)
    ):
    return templates.TemplateResponse(
        request=request,
        name="monitoring/buildings.html",
        context={
            "buildings": buildings,
            "current_user": current_user,
        }
    )



@router.get(
    "/{id}/classrooms",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_building_classrooms_page(
    id: int,
    request: Request,
    building: BuildingModel=Depends(get_building),
    current_user: UserModel = Depends(get_current_user),
    ):
    classrooms = await ClassroomsDAO.find_all(building_id=id)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/building_classrooms.html",
        context={
            "classrooms": classrooms,
            "building": building,
            "current_user": current_user,
        }
    )


@router.get(
    "/{id}/classrooms/list",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_building_classrooms_list_page(
    id: int,
    request: Request,
    building: BuildingModel=Depends(get_building),
    current_user: UserModel = Depends(get_current_user),
    ):
    classrooms = await ClassroomsDAO.find_all(building_id=id)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/list.html",
        context={
            "classrooms": classrooms,
            "building": building,
            "current_user": current_user,
        }
    )


@router.get(
    "/{id}/classrooms/map",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_building_classrooms_map_page(
    id: int,
    request: Request,
    building: BuildingModel=Depends(get_building),
    current_user: UserModel = Depends(get_current_user),
    ):
    classrooms = await ClassroomsDAO.find_all(building_id=id)
    cameras = await CamerasDAO.find_all(building_id=id)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/map.html",
        context={
            "classrooms": classrooms,
            "cameras": cameras,
            "building": building,
            "current_user": current_user,
        }
    )
