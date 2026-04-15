from typing import Annotated, Optional
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
    "/create_incident",
    dependencies=[
        Depends(permission_required("incident_create"))
    ],
)
async def create_incident(
    request: Request,
    query_params: Annotated[IncidentFormScheme, Form()],
    current_user = Depends(get_current_user),
    ):
    await add_incident(query_params)
    logger.info(
        "Created incident",
        extra=current_user,
        exc_info=True
    )
    return RedirectResponse(request.url_for("page_get_active_monitoring"), status_code=status.HTTP_303_SEE_OTHER)
    

@router.post(
    "/create_incident/{building_id}",
    dependencies=[
        Depends(permission_required("incident_create"))
    ],
)
async def create_incident_for_building(
    request: Request,
    query_params: Annotated[IncidentFormScheme, Form()],
    current_user = Depends(get_current_user),
    building_id: Optional[int] = None,
    ):
    await add_incident(query_params)
    logger.info(
        "Created incident for building",
        extra={
            **current_user,
            "building_id": building_id,
        },
        exc_info=True
    )
    if building_id is not None:
        return RedirectResponse(request.url_for("page_get_active_monitoring").include_query_params(building_id=building_id), status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse(request.url_for("page_get_active_monitoring"), status_code=status.HTTP_303_SEE_OTHER)