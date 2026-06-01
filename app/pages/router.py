from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.buildings.dao import BuildingsDAO
from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings
from app.cameras.dao import CamerasDAO
from app.cameras.router import get_all_cameras
from app.classrooms.models import ClassroomModel
from app.classrooms.router import get_classroom
from app.incidents.dao import IncidentsDAO
from app.incidents.models import IncidentModel
from app.incidents.router import get_all_incidents
from app.incidents.type.router import get_all_incident_types
from app.logger import logger
from app.pages.buildings import router as buildings_frontend_router
from app.pages.schedule import router as schedule_frontend_router
from app.schedule.router import get_active_monitoring
from app.users.dependencies import get_current_user, permission_required
from app.users.models import UserModel

router = APIRouter(
    tags=["Фронтенд"],
)


router.include_router(schedule_frontend_router)
router.include_router(buildings_frontend_router)

templates = Jinja2Templates(directory="app/templates")


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))],
)
async def page_get_dashboard_page(
    request: Request,
    buildings: BuildingModel = Depends(get_all_buildings),
    current_user: UserModel = Depends(get_current_user),
):
    logger.info("User open dashboard", extra=current_user, exc_info=True)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/dashboard.html",
        context={
            "buildings": buildings,
            "current_user": current_user,
        },
    )


@router.get(
    "/incidents",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))],
)
async def page_get_incidents_page(
    request: Request,
    incidents: List[IncidentModel] = Depends(get_all_incidents),
    current_user: UserModel = Depends(get_current_user),
):
    logger.info("User open incidents", extra=current_user, exc_info=True)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/incidents.html",
        context={
            "incidents": incidents,
            "current_user": current_user,
        },
    )


@router.get(
    "/classrooms/{id}/streams",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))],
)
async def page_get_cameras_view_page(
    id: int,
    request: Request,
    # building: BuildingModel=Depends(get_building),
    classroom: ClassroomModel = Depends(get_classroom),
    current_user: UserModel = Depends(get_current_user),
):
    cameras = await CamerasDAO.find_all(classroom_id=id)
    building = await BuildingsDAO.find_one_or_none(id=classroom.building_id)

    logger.info(
        f"User open cameras webrtc page for classroom {id}",
        extra={
            **current_user,
            "building_id": classroom.building_id,
            "classroom_id": classroom.id,
        },
        exc_info=True,
    )
    return templates.TemplateResponse(
        request=request,
        # name="monitoring/camera_stream.html",
        name="monitoring/camera_webrtc.html",
        context={
            "request": request,
            "cameras": cameras,
            "classroom": classroom,
            "building": building,
            "current_user": current_user,
        },
    )


@router.get(
    "/videowall",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))],
)
async def page_get_videowall_page(
    request: Request,
    cameras=Depends(get_all_cameras),
    current_user: UserModel = Depends(get_current_user),
):
    logger.info("User open videowall", extra=current_user, exc_info=True)
    return templates.TemplateResponse(
        request=request,
        # name="monitoring/camera_stream.html",
        name="monitoring/videowall.html",
        context={"request": request, "cameras": cameras, "current_user": current_user},
    )


@router.get(
    "/active_monitoring",
    response_class=HTMLResponse,
    dependencies=[Depends(permission_required("frontend"))],
)
async def page_get_active_monitoring(
    request: Request,
    building_id: Optional[int] = None,
    event_type: Optional[int] = None,
    monitoring_data=Depends(get_active_monitoring),
    incident_types=Depends(get_all_incident_types),
    current_user: UserModel = Depends(get_current_user),
):
    logger.info(
        "User open active_monitoring",
        extra={
            **current_user,
            "building_id": building_id,
            "event_type": event_type,
        },
        exc_info=True,
    )
    if monitoring_data:
        cameras = await CamerasDAO.find_all(
            classroom_id=monitoring_data.current_classroom_id
        )
        incidents_data = await IncidentsDAO.get_incidents_info(
            visor_id=current_user.id,
            event_id=monitoring_data.current_subject_id,
        )
        return templates.TemplateResponse(
            request=request,
            name="monitoring/active_monitoring.html",
            context={
                "request": request,
                "building_id": building_id,
                "event_type": event_type,
                "monitoring_data": monitoring_data,
                "current_user": current_user,
                "incident_types": incident_types,
                "cameras": cameras,
                "incidents_data": incidents_data,
                "len_cameras": len(cameras),
                "cameras_ids": ",".join(str(camera.id) for camera in cameras),
            },
        )
    else:
        return templates.TemplateResponse(
            request=request,
            name="monitoring/active_monitoring_wait.html",
            context={
                "current_user": current_user,
            },
        )


# Removed opencv
# @router.get(
#     "/camera_view/{id}",
#     response_class=StreamingResponse,
#     dependencies=[Depends(permission_required("frontend"))]
# )
# async def camera_stream(
#     # id: int,
#     camera: CameraModel=Depends(get_camera),
#     ):
#     camera_stream = Camera(camera.rtsp_url)
#     return StreamingResponse(gen_frames(camera_stream), media_type='multipart/x-mixed-replace; boundary=frame')


@router.get("/login", response_class=HTMLResponse)
async def page_get_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/403", response_class=HTMLResponse)
async def get_403_page(request: Request):
    return templates.TemplateResponse("auth/403.html", {"request": request})


@router.get("/404", response_class=HTMLResponse)
async def get_404_page(request: Request):
    return templates.TemplateResponse("auth/404.html", {"request": request})
