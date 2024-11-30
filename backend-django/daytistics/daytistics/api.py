from datetime import datetime
from typing import List

from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from ninja_jwt.authentication import JWTAuth

from .schemes import (
    CreateDaytisticRequest,
    CreateDaytisticResponse,
    DaytisticResponse,
    AddActivityEntryRequest,
    AddActivityEntryResponse,
)
from .models import Daytistic
from .helpers import build_daytistic_response, build_activity_response
from ..utils.schemes import Message
from ..activities.models import ActivityEntry, ActivityType

router = Router()


@router.post(
    "create",
    response={201: CreateDaytisticResponse, 400: Message, 409: Message, 422: Message},
    auth=JWTAuth(),
)
def create_daytistic(request, payload: CreateDaytisticRequest):
    """
    POST-Endpoint to create a new Daytistic.

    This endpoint creates a new Daytistic for the current user. It is protected by JWT authentication.

    **Body:**
        date: str - The date of the Daytistic in ISO format (YYYY-MM-DD)

    **Response:**
        201: CreateDaytisticResponse - The ID of the created Daytistic
        400: Message - Date is in the future
        409: Message - Daytistic already exists
        422: Message - Invalid date format. Must be in ISO format (YYYY-MM-DD)
        500: Message - Internal server error
    """

    try:
        date = datetime.fromisoformat(payload.date)
        now = datetime.now()
    except ValueError:
        return 422, {
            "detail": "Invalid date format. Must be in ISO format (YYYY-MM-DD)"
        }

    if Daytistic.objects.filter(user=request.user, date=date).exists():
        return 409, {"detail": "Daytistic already exists"}

    if date > now:
        return 400, {"detail": "Date is in the future"}

    daytistic = Daytistic.objects.create(user=request.user, date=date)

    return 201, {"id": daytistic.pk}


@router.get(
    "list",
    response={400: Message, 200: List[DaytisticResponse]},
    auth=JWTAuth(),
)
@paginate(PageNumberPagination, page_size=5)
def list_daytistics(request):
    """
    GET-Endpoint to list all Daytistics.

    This endpoint lists all Daytistics for the current user. It is protected by JWT authentication. The Daytistics are paginated with a page size of 5.

    **Query:**
        page: int - The page number to retrieve

    **Response:**
        200: List[DaytisticResponse] - A list of Daytistics
        400: Message - Invalid page number
        500: Message - Internal server error
    """

    user = request.user

    return [
        build_daytistic_response(daytistic)
        for daytistic in Daytistic.objects.filter(user=user).order_by("-date")
    ]


@router.get(
    "{daytistic_id}", response={200: DaytisticResponse, 404: Message}, auth=JWTAuth()
)
def get_daytistic(request, daytistic_id: int):
    """
    GET-Endpoint to retrieve a single Daytistic.

    This endpoint retrieves a single Daytistic for the current user by its ID. It is protected by JWT authentication.

    **Query:**
        daytistic_id: int - The ID of the Daytistic to retrieve

    **Response:**
        200: DaytisticResponse - The Daytistic object as JSON
        404: Message - Daytistic not found
        500: Message - Internal server error
    """

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return 404, {"detail": "Daytistic not found"}

    daytistic = Daytistic.objects.get(id=daytistic_id)

    return 200, build_daytistic_response(daytistic)


@router.post(
    "{daytistic_id}/add-activity",
    response={201: AddActivityEntryResponse, 404: Message, 422: Message},
    auth=JWTAuth(),
)
def add_activity_to_daytistic(
    request, daytistic_id: int, payload: AddActivityEntryRequest
):
    """
    POST-Endpoint to add an Activity to a Daytistic.

    This endpoint adds an Activity to a Daytistic for the current user. It is protected by JWT authentication.

    **Path:**
        daytistic_id: int - The ID of the Daytistic to add the Activity to

    **Body:**
        id: int - The ID of the Activity
        start_time: int - The start time of the Activity in minutes since midnight
        end_time: int - The end time of the Activity in minutes since midnight

    **Response:**
        201: AddActivityEntryResponse - A list of all Activities in the Daytistic
        404: Message - Daytistic not found
        422: Message - Invalid start time, end time, or Activity overlaps with existing Activity
        500: Message - Internal server error
    """

    activity_id = payload.id
    start_time = payload.start_time
    end_time = payload.end_time

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return 404, {"detail": "Daytistic not found"}

    daytistic = Daytistic.objects.get(id=daytistic_id)

    if not ActivityType.objects.filter(pk=activity_id).exists():
        return 404, {"detail": "Activity not found"}

    activity_type = ActivityType.objects.get(id=activity_id)

    if start_time < 0 or start_time > 1440:
        return 422, {"detail": "Invalid start time"}

    if end_time < 0 or end_time > 1440:
        return 422, {"detail": "Invalid end time"}

    if start_time >= end_time:
        print("Start time must be before end time")
        return 422, {"detail": "Start time must be before end time"}

    if ActivityEntry.objects.filter(
        daytistics=daytistic, start_time=start_time, end_time=end_time
    ).exists():
        print("Activity overlaps with existing activity")
        return 422, {"detail": "Activity overlaps with existing activity"}

    if ActivityEntry.objects.filter(
        daytistics=daytistic, start_time__lt=end_time, end_time__gt=start_time
    ).exists():
        print("Activity overlaps with existing activity")
        return 422, {"detail": "Activity overlaps with existing activity"}

    activity_entry, _ = ActivityEntry.objects.get_or_create(
        type=activity_type,
        start_time=start_time,
        end_time=end_time,
    )

    daytistic.activities.add(activity_entry)

    return 201, {
        "activities": [
            build_activity_response(activity) for activity in daytistic.activities.all()
        ]
    }
