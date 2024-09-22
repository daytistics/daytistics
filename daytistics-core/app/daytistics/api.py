from calendar import Day
from datetime import datetime, timedelta, time
from typing import List

from ninja import Router
from ninja.pagination import paginate, PageNumberPagination
from ninja_jwt.authentication import JWTAuth

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
from ..users.models import CustomUser

router = Router()


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
        date = datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        return 422, {"detail": "Invalid date format. Use %m/%d/%Y"}

    if Daytistic.objects.filter(user=request.user, date=date).exists():
        return 409, {"detail": "Daytistic already exists"}

    if date < datetime.now() - timedelta(weeks=4):
        return 400, {"detail": "Date must be within the last 4 weeks"}

    if date > datetime.now():
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


# TODO: Write tests for this endpoint
@router.get(
    "{daytistic_id}", response={200: DaytisticResponse, 404: Message}, auth=JWTAuth()
)
def get_daytistic(request, daytistic_id: int):
    user = request.user

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return 404, {"detail": "Daytistic not found"}

    daytistic = Daytistic.objects.get(id=daytistic_id)

    return 200, build_daytistic_response(daytistic)


# TODO: Write tests for this endpoint
@router.post(
    "{daytistic_id}/add-activity/",
    response={201: CreateActivityEntryResponse, 404: Message, 422: Message},
    auth=JWTAuth(),
)
def add_activity_to_daytistic(
    request, daytistic_id: int, payload: CreateActivityEntryRequest
):
    user: CustomUser = request.user
    activity_name = payload.name.lower()
    start_time = payload.start_time
    end_time = payload.end_time

    if not Daytistic.objects.filter(user=request.user, id=daytistic_id).exists():
        return 404, {"detail": "Daytistic not found"}

    daytistic = Daytistic.objects.get(id=daytistic_id)

    if not ActivityType.objects.filter(name=activity_name).exists():
        activity_type = ActivityType.objects.create(name=activity_name)
        user.activities.add(activity_type)
        user.save()

    activity_type = ActivityType.objects.get(name=activity_name)

    if start_time < 0 or start_time > 1440:
        return 422, {"detail": "Start time must be between 0 and 1440"}

    if end_time < 0 or end_time > 1440:
        return 422, {"detail": "End time must be between 0 and 1440"}

    if start_time >= end_time:
        return 422, {"detail": "Start time must be before end time"}
    
    
    start_hours, start_minutes = divmod(start_time, 60)
    end_hours, end_minutes = divmod(end_time, 60)

    # Create datetime.time objects
    start_time_obj = time(start_hours, start_minutes)
    end_time_obj = time(end_hours, end_minutes)

    # Combine date with time objects
    iso_start_time = datetime.combine(daytistic.date, start_time_obj)
    iso_end_time = datetime.combine(daytistic.date, end_time_obj)

    if ActivityEntry.objects.filter(daytistic=daytistic, start_time__lt=iso_end_time, end_time__gt=iso_start_time).exists():
        return 422, {"detail": "Activity overlaps with existing activity"}

    ActivityEntry.objects.create(
        daytistic=daytistic,
        type=activity_type,
        start_time=iso_start_time,
        end_time=iso_end_time,
    )

    return 201, {"activities": [build_activity_response(activity) for activity in ActivityEntry.objects.filter(daytistic=daytistic)]}
