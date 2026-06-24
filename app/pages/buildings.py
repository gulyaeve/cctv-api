from datetime import datetime, timedelta, date

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.ai_analysis.dao import AiAnalysisDAO
from app.buildings.dao import BuildingsDAO
from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings, get_building
from app.cameras.dao import CamerasDAO
from app.classrooms.dao import ClassroomsDAO
from app.incidents.dao import IncidentsDAO
from app.schedule.dao import ScheduleDAO
from app.schedule.models import ScheduleModel
from app.schedule.router import get_schedule
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel
from app.logger import logger


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
    logger.info(
        "User open list of buildings",
        extra=current_user,
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="buildings/buildings.html",
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
    logger.info(
        "User open list of classrooms",
        extra={
            **current_user,
            "building_id": id,
        },
        exc_info=True
    )
    classrooms = await ClassroomsDAO.find_all(building_id=id)
    return templates.TemplateResponse(
        request=request,
        name="buildings/building_classrooms.html",
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
    logger.info(
        "User open list of classrooms",
        extra={
            **current_user,
            "building_id": id,
        },
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="buildings/list.html",
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
    logger.info(
        "User open map of classrooms",
        extra={
            **current_user,
            "building_id": id,
        },
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="buildings/map.html",
        context={
            "classrooms": classrooms,
            "cameras": cameras,
            "building": building,
            "current_user": current_user,
        }
    )


@router.get(
    "/{id}/schedule",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_building_schedule_page(
    id: int,
    request: Request,
    building: BuildingModel = Depends(get_building),
    current_user: UserModel = Depends(get_current_user),
    date_from: date = (datetime.now() - timedelta(days=datetime.now().weekday())).date(),
    date_to: date = (datetime.now() + timedelta(days=5)).date()
):
    schedules = await ScheduleDAO.find_all(building_id=id, date_from=date_from, date_to=date_to)
    logger.info(
        "User open list of schedules",
        extra={
            **current_user,
            "building_id": id,
        },
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="buildings/building_schedule.html",
        context={
            "schedules": schedules,
            "building": building,
            "current_user": current_user,
        }
    )


@router.get(
    "/{building_id}/schedule/{id}",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_building_schedule_info_page(
    request: Request,
    schedule: ScheduleModel=Depends(get_schedule),
    current_user: UserModel = Depends(get_current_user)
):
    incidents = await IncidentsDAO.find_all(event=schedule.id)
    ai_analysis = await AiAnalysisDAO.find_all(event=schedule.id)
    logger.info(
        "User open schedule info page",
        extra={
            "current_user": current_user,
            "schedule": schedule,
        },
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="schedules/schedule_info.html",
        context={
            "request": request,
            "current_user": current_user,
            "schedule": schedule,
            "incidents": incidents,
            "ai_analysis": ai_analysis,
        }
    )
