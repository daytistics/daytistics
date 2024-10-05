from django.middleware.csrf import get_token
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from ..activities.api import router as activities_router
from ..users.api import router as users_router
from ..daytistics.api import router as daytistics_router

api = NinjaExtraAPI(
    csrf=True,
    version="Pre-Release",
    title="core-api",
    description="API for interacting with the backend core of Daytistics",
)

api.register_controllers(NinjaJWTDefaultController)

api.add_router("/users/", users_router)
api.add_router("/daytistics/", daytistics_router)
api.add_router("/activities/", activities_router)


@api.get("csrf/", response={200: dict, 500: dict})
def get_csrf_token(request):
    csrf_token = get_token(request)
    return 200, {"csrfToken": csrf_token}
