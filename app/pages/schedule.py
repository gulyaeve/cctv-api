from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings
from app.schedule.models import ScheduleModel
from app.schedule.router import get_all_schedules
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel


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
    buildings: BuildingModel=Depends(get_all_buildings),
    current_user: UserModel = Depends(get_current_user)
    ):
    return templates.TemplateResponse(
        request=request,
        name="schedules/schedules_buildings.html",
        context={
            # "schedules": schedules,
            "current_user": current_user,
            "buildings": buildings,
        }
    )