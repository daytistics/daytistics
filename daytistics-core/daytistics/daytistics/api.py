from datetime import datetime, timedelta, time
from typing import List

from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from ninja_jwt.authentication import JWTAuth
from tomlkit import date

from .schemes import (
    CreateDaytisticRequest,
    CreateDaytisticResponse,
    DaytisticResponse,
    CreateActivityEntryRequest,
    CreateActivityEntryResponse,
)
from .models import Daytistic
from .helpers import build_daytistic_response, build_activity_response
from ..utils.schemes import Message
from ..activities.models import ActivityEntry, ActivityType
from zoneinfo import ZoneInfo

router = Router()


# TODO: Change from receiving date as string to ISO format UTC time
@router.post(
    "create/",
    response={201: CreateDaytisticResponse, 400: Message, 409: Message, 422: Message},
    auth=JWTAuth(),
)
def create_daytistic(request, payload: CreateDaytisticRequest):
    date_str = payload.date

    if not date_str:
        return 422, {"detail": "Date is required"}

    try:
        date = datetime.fromisoformat(date_str)

        # If the parsed date doesn't have tzinfo, use the user's timezone
        if date.tzinfo is None:
            user_timezone = ZoneInfo(request.user.timezone)
            date = date.replace(tzinfo=user_timezone)

        # Get the current time in the same timezone as the parsed date
        now = datetime.now(date.tzinfo)
    except ValueError:
        return 422, {"detail": "Invalid date format. Must be in ISO format"}

    if Daytistic.objects.filter(user=request.user, date=date).exists():
        return 409, {"detail": "Daytistic already exists"}

    if date < now - timedelta(weeks=4):
        return 400, {"detail": "Date must be within the last 4 weeks"}

    if date > now:
        return 400, {"detail": "Date is in the future"}

    daytistic = Daytistic.objects.create(user=request.user, date=date)

    return 201, {"id": daytistic.id}


@router.get("", response={200: List[DaytisticResponse]}, auth=JWTAuth())
@paginate(PageNumberPagination, page_size=5)
def list_daytistics(request):
    user = request.user

    return [
        build_daytistic_response(daytistic)
        for daytistic in Daytistic.objects.filter(user=user).order_by("-date")
    ]


@router.get(
    "{daytistic_id}", response={200: DaytisticResponse, 404: Message}, auth=JWTAuth()
)
def get_daytistic(request, daytistic_id: int):
    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return 404, {"detail": "Daytistic not found"}

    daytistic = Daytistic.objects.get(id=daytistic_id)

    return 200, build_daytistic_response(daytistic)


@router.post(
    "{daytistic_id}/add-activity/",
    response={201: CreateActivityEntryResponse, 404: Message, 422: Message},
    auth=JWTAuth(),
)
def add_activity_to_daytistic(
    request, daytistic_id: int, payload: CreateActivityEntryRequest
):
    activity_id = payload.id

    try:
        start_time = datetime.fromisoformat(payload.start_time)
        end_time = datetime.fromisoformat(payload.end_time)
    except ValueError:
        # TODO: Test this
        print("Invalid date format. Must be in ISO format")
        return 422, {"detail": "Invalid date format. Must be in ISO format"}

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return 404, {"detail": "Daytistic not found"}

    daytistic = Daytistic.objects.get(id=daytistic_id)

    # TODO: Test this
    if daytistic.date != start_time.date():
        print("Activity date must match daytistic date")
        return 422, {"detail": "Activity date must match daytistic date"}

    if not ActivityType.objects.filter(pk=activity_id).exists():
        return 404, {"detail": "Activity not found"}

    activity_type = ActivityType.objects.get(id=activity_id)

    if start_time.timestamp() >= end_time.timestamp():
        print("Start time must be before end time")
        return 422, {"detail": "Start time must be before end time"}

    if ActivityEntry.objects.filter(
        daytistics=daytistic, start_time=start_time, end_time=end_time
    ).exists():
        print("Activity overlaps with existing activity")
        return 422, {"detail": "Activity overlaps with existing activity"}

    activity_entry, _ = ActivityEntry.objects.get_or_create(
        type=activity_type,
        start_time=start_time,
        end_time=start_time,
    )

    daytistic.activities.add(activity_entry)

    return 201, {
        "activities": [
            build_activity_response(activity) for activity in daytistic.activities.all()
        ]
    }
