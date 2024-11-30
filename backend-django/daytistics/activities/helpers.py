from ..activities.models import ActivityType
from ..users.models import CustomUser


def build_activity_type_response(activity_type: ActivityType, user: CustomUser) -> dict:
    """
    Build a response schema for an ActivityType. This function takes an ActivityType object and a CustomUser object and returns a dictionary with the response schema.

    Args:
        activity_type (ActivityType): The ActivityType object to build the response schema for.
        user (CustomUser): The CustomUser object to check if the ActivityType is available for the user.

    Returns:
        dict: The response schema for the ActivityType.
    """

    return {
        "id": activity_type.pk,
        "name": activity_type.name,
        "category": activity_type.category.name,
        "available": activity_type in user.activities.all(),
        "active": activity_type.active,
    }
