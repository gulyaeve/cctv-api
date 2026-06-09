from os import path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.users.dependencies import permission_required
from app.utils.find_image import find_screenshot


router = APIRouter(
    prefix="/screenshots",
    tags=["Screenshots"],
    dependencies=[Depends(permission_required("incidents"))]
)


@router.get("/{file_path:path}")
async def serve_screenshots(file_path: str):
    image_path = path.normpath(path.join("screenshots_bank", file_path))
    if path.isfile(image_path):
        return FileResponse(image_path)
    else:
        return HTTPException(400, "File does not exists")
    

@router.get("")
async def get_screenshot_by_ids(incident_id: int, camera_id: int):
    file = find_screenshot(incident_id, camera_id)
    if file is not None:
        return await serve_screenshots(file)
    else:
        return HTTPException(400, "File does not exists")
