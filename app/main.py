from contextlib import asynccontextmanager
from app.utils.verify_subnet import SubnetAccessMiddleware
from app.version import version
from app.logger import logger
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
from sqladmin import Admin

from app.admin.views import (
    BuildingsAdmin,
    CamerasAdmin,
    ClassroomsAdmin,
    GroupsAdmin,
    IncidentsAdmin,
    PermissionsAdmin,
    RolesAdmin,
    ScheduleAdmin,
    TeachersAdmin,
    UsersAdmin,
)
from app.admin.auth import authentication_backend
from app.broker_utils.broker_init import declare_exchange_and_queue
from app.buildings.router import router as buildings_router
from app.cameras.router import router as cameras_router
from app.classrooms.router import router as classrooms_router

from app.database import engine
from app.exceptions import IncorrectEmailOrPassword, OperationNotPermited, TokenMissing, TokenIncorrect, UserNotPresent
from app.groups.router import router as groups_router
from app.incidents.router import router as incidents_router
from app.pages.router import router as pages_router
from app.schedule.router import router as schedule_router
from app.schedule.router import router_daily as schedule_router_daily
from app.teachers.router import router as teachers_router
from app.users.auth import noauth_handler, noperm_handler, notfound_handler
from app.users.router import router as users_router
from app.active_monitoring.router import router as active_monitoring_router
from app.analytics.router import router as analytics_router
from app.ai_analysis.router import router as ai_analysis_router
from app.config import settings

api = APIRouter(
    prefix="/api",
)
api.include_router(buildings_router)
api.include_router(classrooms_router)
api.include_router(users_router)
api.include_router(cameras_router)
api.include_router(teachers_router)
api.include_router(schedule_router)
api.include_router(schedule_router_daily)
api.include_router(groups_router)
api.include_router(incidents_router)
api.include_router(analytics_router)
api.include_router(ai_analysis_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before startup
 
    # Create exchange and queue in RabbitMQ
    await declare_exchange_and_queue()
    logger.info("RabbitMQ data ready")

    logger.info(f"Started app {app.title} v{app.version}")

    yield

    # After shutdown
    logger.info("Application shutdown")


app = FastAPI(
    title="Система видеонаблюдения",
    version=version,
    lifespan=lifespan,
    root_path=settings.ROOT_PATH,
    redoc_url=None,
)

app.add_middleware(SubnetAccessMiddleware)

app.mount("/static", StaticFiles(directory="app/static"), "static")
app.include_router(api)
app.include_router(pages_router)
app.include_router(active_monitoring_router)

app.add_exception_handler(404, notfound_handler)
app.add_exception_handler(OperationNotPermited, noperm_handler)
app.add_exception_handler(IncorrectEmailOrPassword, noauth_handler)
app.add_exception_handler(TokenIncorrect, noauth_handler)
app.add_exception_handler(TokenMissing, noauth_handler)
app.add_exception_handler(UserNotPresent, noauth_handler)


@app.get("/download-cert")
async def download_cert():
    file_path = "/src/app/static/files/cctv.itmoscow.crt"
    return FileResponse(
        path=file_path, 
        filename="cctv.itmoscow.crt"
    )


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    # allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_methods=["*"],
    # allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
    #                "Access-Control-Allow-Origin", "Authorization"],
    allow_headers=["*"],
)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


admin = Admin(app, engine, authentication_backend=authentication_backend)
# admin = Admin(app, engine)
admin.add_view(UsersAdmin)
admin.add_view(RolesAdmin)
admin.add_view(PermissionsAdmin)
admin.add_view(BuildingsAdmin)
admin.add_view(ClassroomsAdmin)
admin.add_view(CamerasAdmin)
admin.add_view(ScheduleAdmin)
admin.add_view(TeachersAdmin)
admin.add_view(GroupsAdmin)
admin.add_view(IncidentsAdmin)


@app.get("/", response_class=RedirectResponse)
def redirect_to_login_page(request: Request):
    start_page = request.url_for("page_get_dashboard_page")
    return RedirectResponse(start_page)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)

    # start_time = time.time()
    # process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    # logger.info("Request handling time", extra={
    #     "process_time": round(process_time, 4)
    # })
    return response