from django.db.models.signals import post_migrate
from django.dispatch import receiver
from app.activities.models import Activity
from django.db.models.base import ModelBase
from django.conf import settings


# Todo: tests
@receiver(post_migrate)
def create_default_activities(sender: ModelBase, **kwargs) -> None:
    """
    Creates the default activities if they do not exist. 
    The activities are by default in english and are loaded from the constants in the Django settings. 
    This function is automatically called after the migration of the activities app. 
    It should not be called manually.

    Args:
        sender (ModelBase): The model that sent the signal.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        None
    """
    if sender.name == "activities":
        for activity in settings.DEFAULT_ACTIVITIES:
            if not Activity.objects.filter(name=activity).exists():
                Activity.objects.create(name=activity, is_global=True)
                print(f"Activity {activity} created")
        print("Default activities created if they did not exist")
