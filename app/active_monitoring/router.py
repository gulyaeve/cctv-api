from typing import Annotated
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import RedirectResponse

from app.incidents.router import add_incident
from app.incidents.schemas import IncidentFormScheme
from app.users.dependencies import get_current_user, permission_required


router = APIRouter(
    prefix="",
    tags=["Активный мониторинг"]
)


@router.post(
    "/create_incident",
    dependencies=[
        Depends(permission_required("incident_create"))
    ]
)
async def create_incident(
    query_params: Annotated[IncidentFormScheme, Form()],
    ):
    await add_incident(query_params)
    return RedirectResponse("/active_monitoring", status_code=status.HTTP_303_SEE_OTHER)
