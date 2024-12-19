from typing import List

from ninja import Router
from ninja_jwt.modules.usersentication import JWTAuth

from .schemes import ActivityTypeResponse
from .models import ActivityType
from .helpers import build_activity_type_response

router = Router()


# TODO: Add pagination
@router.get("", response=List[ActivityTypeResponse], auth=JWTAuth())
def list_activities(request, all: bool = False):
    """
    GET-Endpoint to list all available activities. This endpoint returns a list of all available activities for the current user. It is protected by JWT authentication.

    **Query**:
        all: bool - If true, all activities are returned. If false, only the activities available to the user are returned. Default is false.

    **Response**:
        200: List[ActivityTypeResponse] - A list of all available activities.
        500: Message - Internal server error

    Returns:
        _type_: _description_
    """

    return (
        [
            build_activity_type_response(activity_type, request.user)
            for activity_type in ActivityType.objects.filter(active=True)
        ]
        if all
        else [
            build_activity_type_response(activity_type, request.user)
            for activity_type in request.user.activities.all().filter(active=True)
        ]
    )
