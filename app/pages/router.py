from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse

from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings, get_building
from app.camera_utils.streaming import Camera, gen_frames
from app.cameras.dao import CamerasDAO
from app.cameras.models import CameraModel
from app.cameras.router import get_camera
from app.classrooms.dao import ClassroomsDAO
from app.classrooms.models import ClassroomModel
from app.classrooms.router import get_classroom
from app.incidents.dao import IncidentsDAO
from app.schedule.router import get_active_monitoring
from app.users.dependencies import get_current_user, get_fake_user
from app.users.models import UserModel


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
    classrooms = await ClassroomsDAO.find_all(building_id=id)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/building_classrooms.html",
        context={"classrooms": classrooms, "building": building}
        )


@router.get("/classroom_cameras_view/{id}", response_class=HTMLResponse)
async def page_get_cameras_view_page(
    id: int,
    request: Request,
    classroom: ClassroomModel=Depends(get_classroom),
    ):
    cameras = await CamerasDAO.find_all(classroom_id=id)
    return templates.TemplateResponse(
        request=request,
        name="monitoring/camera_stream.html",
        context={"cameras": cameras, "classroom": classroom}
        )


@router.get("/active_monitoring", response_class=HTMLResponse)
async def page_get_active_monitoring(
    request: Request,
    monitoring_data = Depends(get_active_monitoring),
    current_user: UserModel = Depends(get_fake_user) # TODO: Убрать fake
    ):
    if monitoring_data:
        cameras = await CamerasDAO.find_all(classroom_id=monitoring_data.current_classroom_id)
        incidents_data = await IncidentsDAO.get_incidents_info(
            visor_id=current_user.id,
            event_id=monitoring_data.current_subject_id,
        ) 
        return templates.TemplateResponse(
            request=request,
            name="monitoring/active_monitoring.html",
            context={
                "monitoring_data": monitoring_data,
                "current_user": current_user,
                "cameras": cameras,
                "incidents_data": incidents_data,
                "len_cameras": len(cameras)
            }
            )


@router.get("/camera_view/{id}", response_class=StreamingResponse)
async def camera_stream(
    id: int,
    camera: CameraModel=Depends(get_camera),
    ):
    camera_stream = Camera(camera.rtsp_url)
    return StreamingResponse(gen_frames(camera_stream), media_type='multipart/x-mixed-replace; boundary=frame')


@router.get("/login", response_class=HTMLResponse)
async def page_get_login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})
