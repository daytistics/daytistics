from typing import Dict, Union, List

from .models import Daytistic
from ..users.models import CustomUser
from ..activities.models import ActivityEntry


def build_daytistic_response(
    daytistic: Daytistic,
) -> dict:

    user = CustomUser.objects.get(id=daytistic.user.pk)

    last_login = (
        user.last_login.strftime("%Y-%m-%dT%H:%M:%S") if user.last_login else "Never"
    )

    user_schema = {
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "groups": [group.name for group in user.groups.all()],
        "user_permissions": [
            permission.codename for permission in user.user_permissions.all()
        ],
        "date_joined": user.date_joined.strftime("%Y-%m-%dT%H:%M:%S"),
        "last_login": last_login,
        "date_format": user.date_format,
    }

    diary_schema = {
        "entry": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec nunc nec nunc.",
        "moment_of_happiness": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec nunc nec nunc.",
    }

    wellbeing_schema_list = [
        {
            "id": i,
            "name": f"Well-being #{i}",
            "rating": i - 1,
        }
        for i in range(1, 7)
    ]

    activity_schema_list = [
        build_activity_response(activity)
        for activity in daytistic.activities.all().order_by("start_time")
    ]

    # Converts the date to a datetime object
    daytistic_datetime = daytistic.date.strftime("%Y-%m-%d")

    return {
        "id": daytistic.pk,
        "date": daytistic_datetime,
        "average_wellbeing": 5.0,
        "total_activities": daytistic.activities.count(),
        "total_duration": daytistic.total_duration,
        "user": user_schema,
        "wellbeing": wellbeing_schema_list,
        "activities": activity_schema_list,
        "diary": diary_schema,
    }


def build_activity_response(activity: ActivityEntry) -> Dict[str, Union[int, str]]:

    return {
        "id": activity.pk,
        "name": activity.type.name,
        "duration": activity.duration,
        "start_time": activity.start_time,
        "end_time": activity.end_time,
    }
