from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.buildings.models import BuildingModel
from app.buildings.router import get_all_buildings
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
async def get_buildings_page(
    request: Request,
    # classroom: ClassroomModel=Depends(get_all_classrooms),
    buildings: BuildingModel=Depends(get_all_buildings)
    ):
    return templates.TemplateResponse(
        request=request,
        name="monitoring/buildings.html",
        context={"buildings": buildings}
        )


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


# @router.get("/register", response_class=HTMLResponse)
# async def get_register_page(request: Request):
#     return templates.TemplateResponse("auth/register.html", {"request": request})
