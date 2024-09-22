from faker import Faker

from .models import Daytistic
from ..activities.models import ActivityEntry

fake = Faker()


# FIXME: This function contains currently fake data, because some fields are not implemented yet.
def build_daytistic_response(daytistic: Daytistic) -> dict:

    user = daytistic.user

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
        "date_joined": user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S"),
    }

    diary_schema = {
        "entry": fake.text(max_nb_chars=200),
        "moment_of_happiness": fake.sentence(nb_words=6),
    }

    wellbeing_schema_list = [
        {
            "id": i,
            "name": fake.word(),
            "rating": fake.random_int(1, 5),
        }
        for i in range(5)
    ]

    activity_schema_list = [
        build_activity_response(activity)
        for activity in daytistic.activities.all()
    ]

    return {
        "id": daytistic.id,
        "date": daytistic.date.strftime("%m/%d/%Y"),
        "average_wellbeing": 5.0,
        "total_activities": daytistic.activities.count(),
        "total_duration": daytistic.total_duration,
        "user": user_schema,
        "wellbeing": wellbeing_schema_list,
        "activities": activity_schema_list,
        "diary": diary_schema,
    }

def build_activity_response(activity: ActivityEntry) -> dict:
    return {
        "id": activity.id,
        "name": activity.type.name,
        "duration": activity.duration,
        "start_time": activity.start_time.hour * 60 + activity.start_time.minute,
        "end_time": activity.end_time.hour * 60 + activity.end_time.minute,
    }