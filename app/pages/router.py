import logging
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings, get_building
from app.cameras.dao import CamerasDAO
from app.classrooms.dao import ClassroomsDAO
from app.classrooms.models import ClassroomModel
from app.classrooms.router import get_classroom
# from app.classrooms.models import ClassroomModel
# from app.classrooms.router import get_all_classrooms


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/buildings", response_class=HTMLResponse)
async def page_get_buildings_page(
    request: Request,
    buildings: BuildingModel=Depends(get_all_buildings)
    ):
    return templates.TemplateResponse(
        request=request,
        name="monitoring/buildings.html",
        context={"buildings": buildings}
        )


@router.get("/building_classrooms/{id}", response_class=HTMLResponse)
async def page_get_building_classrooms_page(
    id: int,
    request: Request,
    building: BuildingModel=Depends(get_building),
    ):
    logging.info(f"{building=}")
    classrooms = await ClassroomsDAO.find_all(building_id=id)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/building_classrooms.html",
        context={"classrooms": classrooms, "building": building}
        )


@router.get("/classroom_cameras/{id}", response_class=HTMLResponse)
async def page_get_classroom_cameras(
    id: int,
    request: Request,
    classroom: ClassroomModel=Depends(get_classroom),
    ):
    logging.info(f"{classroom=}")
    cameras = await CamerasDAO.find_all(classroom_id=id)
    logging.info(f"{cameras=}")

    return templates.TemplateResponse(
        request=request,
        name="monitoring/classroom_cameras.html",
        context={"cameras": cameras, "classroom": classroom}
        )


@router.get("/login", response_class=HTMLResponse)
async def page_get_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


# @router.get("/register", response_class=HTMLResponse)
# async def get_register_page(request: Request):
#     return templates.TemplateResponse("auth/register.html", {"request": request})
