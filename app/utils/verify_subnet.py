import ipaddress

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.config import settings
from starlette.middleware.base import BaseHTTPMiddleware
    

#  Middleware for subnet access
class SubnetAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("X-Forwarded-For") is not None:
            client_ip = ipaddress.ip_address(request.headers.get("X-Forwarded-For").split(',')[0].strip())
        else:
            client_ip = ipaddress.ip_address(request.client.host)
        print(settings.secured_paths)
        if any(request.url.path.startswith(path) for path in settings.secured_paths):
            if not any(client_ip in subnet for subnet in settings.allowed_subnets):
                return RedirectResponse(request.url_for("get_404_page"), status_code=303)
        
        return await call_next(request)