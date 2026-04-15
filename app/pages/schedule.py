from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.ai_analysis.dao import AiAnalysisDAO
from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings
from app.incidents.dao import IncidentsDAO
from app.schedule.models import ScheduleModel
from app.schedule.router import get_all_schedules, get_schedule
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel
from app.logger import logger


router = APIRouter(
    prefix="/schedules",
    tags=["Расписания"],
)

templates = Jinja2Templates(
    directory="app/templates"
)



@router.get(
    "/all",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_schedules_page(
    request: Request,
    schedules: ScheduleModel=Depends(get_all_schedules),
    current_user: UserModel = Depends(get_current_user)
):
    logger.info(
        "User open list of schedules",
        extra=current_user,
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="schedules/schedules.html",
        context={
            "schedules": schedules,
            "current_user": current_user,
        }
    )


@router.get(
    "/buildings",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_schedules_buildings_page(
    request: Request,
    # schedules: ScheduleModel=Depends(get_all_schedules),
    buildings: List[BuildingModel]=Depends(get_all_buildings),
    current_user: UserModel = Depends(get_current_user)
):
    logger.info(
        "User open list of buildings in schedules",
        extra=current_user,
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="schedules/schedules_buildings.html",
        context={
            # "schedules": schedules,
            "current_user": current_user,
            "buildings": buildings,
        }
    )


@router.get(
    "/{id}",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))]
)
async def page_get_schedule_info_page(
    request: Request,
    schedule: ScheduleModel=Depends(get_schedule),
    current_user: UserModel = Depends(get_current_user)
):
    incidents = await IncidentsDAO.find_all(event=schedule.id)
    ai_analysis = await AiAnalysisDAO.find_all(event=schedule.id)
    logger.info(
        "User open schedule page",
        extra=current_user,
        exc_info=True
    )
    return templates.TemplateResponse(
        request=request,
        name="schedules/schedule_info.html",
        context={
            "current_user": current_user,
            "schedule": schedule,
            "incidents": incidents,
            "ai_analysis": ai_analysis,
        }
    )


