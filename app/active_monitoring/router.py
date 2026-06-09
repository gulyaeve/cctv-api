from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse

from app.incidents.router import add_incident
from app.incidents.schemas import IncidentFormScheme
from app.users.dependencies import get_current_user, permission_required
from app.logger import logger


router = APIRouter(
    prefix="",
    tags=["Активный мониторинг"]
)


@router.post(
    "/create_incident/{building_id}/{event_type}",
    dependencies=[
        Depends(permission_required("incident_create"))
    ],
)
async def create_incident(
    request: Request,
    query_params: Annotated[IncidentFormScheme, Form()],
    current_user = Depends(get_current_user),
    building_id: int | Literal["all", "None"] | None = "all",
    event_type: int | Literal["all", "None"] | None = "all",
    ):
    await add_incident(query_params)
    logger.info(
        "Created incident",
        extra={
            **current_user,
            "building_id": building_id,
            "event_type": event_type,
        },
        exc_info=True
    )
    if building_id == "all" or building_id == "None":
        building_id = None
    if event_type == "all":
        event_type = None

    params = {
        "building_id": building_id,
        "event_type": event_type
    }

    return RedirectResponse(
        request.url_for("page_get_active_monitoring")
        .include_query_params(**{k: v for k, v in params.items() if v is not None}),
        status_code=status.HTTP_303_SEE_OTHER,
    )
