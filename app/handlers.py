from fastapi import status
from starlette.requests import Request
from fastapi.responses import JSONResponse, RedirectResponse
from app.logger import logger



def noauth_handler(request: Request, exc):
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(
            url=request.url_for("page_get_login"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return JSONResponse(
            status_code=getattr(exc, "status_code"),
            content={"message": getattr(exc, "detail")}
        )


def noperm_handler(request: Request, exc):
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(
            url=request.url_for("get_403_page"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return JSONResponse(
            status_code=getattr(exc, "status_code"),
            content={"message": getattr(exc, "detail")}
        )
    

def notfound_handler(request: Request, exc):
    logger.warning(msg=f"404 {getattr(exc, 'detail')}", exc_info=True)
    if "text/html" in request.headers.get("accept"):
        return RedirectResponse(
            url=request.url_for("get_404_page"),
            status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        return JSONResponse(
            status_code=getattr(exc, "status_code"),
            content={"message": getattr(exc, "detail")}
        )