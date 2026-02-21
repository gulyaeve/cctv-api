from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.users.auth import auth_user, create_token
from app.users.dependencies import get_current_user, permission_checker


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        # Validate username/password credentials
        user = await auth_user(email, password)
        if user:
            token = create_token({"sub": str(user.id)})
            request.session.update({"token": token})
        
        # And update session
        # request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        user = await get_current_user(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
    
        superadmin = await permission_checker(user.id, "superadmin")
        if not superadmin:
            print("NOT superadmin")
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
