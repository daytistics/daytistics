from django.middleware.csrf import get_token
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from ..activities.api import router as activities_router
from ..users.api import router as users_router
from ..daytistics.api import router as daytistics_router

api = NinjaExtraAPI(
    csrf=True,
    version="0.1.0",
    title="Backend API",
    description="API for interacting with the Daytistics backend",
)

api.register_controllers(NinjaJWTDefaultController)

api.add_router("/users/", users_router)
api.add_router("/daytistics/", daytistics_router)
api.add_router("/activities/", activities_router)


@api.get("csrf", response={200: dict, 500: dict})
def get_csrf_token(request):
    """
    GET-Endpoint to retrieve a CSRF token.

    This endpoint generates and returns a CSRF token for the current session.
    It responds with a JSON object containing the CSRF token.

    **Response:**
        200: dict - A JSON object containing the CSRF token
        500: dict - Internal server error
    """

    csrf_token = get_token(request)
    return 200, {"csrf_token": csrf_token}
