import json
import os

from django.conf import settings
from django.apps import AppConfig


class ActivitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "daytistics.activities"

    def ready(self) -> None:

        if settings.TESTING:
            return

        default_activities = settings.DEFAULT_ACTIVITIES

        from django.templatetags.static import static
        from .models import ActivityCategory, ActivityType

        for key, value in default_activities.items():
            category, _ = ActivityCategory.objects.get_or_create(name=key)

            for activity in value:
                try:
                    ActivityType.objects.get_or_create(
                        name=activity, category=category, active=True
                    )
                except BaseException:
                    continue
