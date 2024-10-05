from ..activities.models import ActivityType
from ..users.models import CustomUser


def build_activity_type_response(activity_type: ActivityType, user: CustomUser) -> dict:
    return {
        "id": activity_type.id,
        "name": activity_type.name,
        "category": activity_type.category.name,
        "available": activity_type in user.activities.all(),
        "active": activity_type.active,
    }
