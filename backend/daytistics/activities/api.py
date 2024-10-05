from typing import List

from ninja import Router
from ninja_jwt.authentication import JWTAuth

from .schemes import ActivityTypeResponse
from .models import ActivityType
from .helpers import build_activity_type_response

router = Router()


@router.get("", response=List[ActivityTypeResponse], auth=JWTAuth())
def list_activities(request, all: bool = False):
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
