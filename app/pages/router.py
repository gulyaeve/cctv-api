from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.classrooms.models import ClassroomModel
from app.classrooms.router import get_all_classrooms


router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/monitoring", response_class=HTMLResponse)
async def get_monitoring_page(
    request: Request,
    classroom: ClassroomModel=Depends(get_all_classrooms),
    ):
    return templates.TemplateResponse(
        request=request,
        name="monitoring/monitoring.html",
        context={"classroom": classroom}
        )
