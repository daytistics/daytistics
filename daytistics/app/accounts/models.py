from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from typing import List
from app.daytistics.models import Daytistic
from random import choices
from app.activities.models import Activity


class CustomUser(AbstractUser):
    activities = models.ManyToManyField(
        "activities.Activity", related_name="users", blank=True
    )

    @property
    def all_activities(self):
        global_activities = Activity.objects.filter(is_global=True)
        query_set = self.activities.all() | global_activities
        return list(self.activities.all() | global_activities)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            from app.daytistics.models import Activity

            for activity in Activity.objects.filter(is_global=True):
                self.activities.add(activity)

    def get_todays_activities(self):
        from app.daytistics.models import Daytistic

        daytistic = Daytistic.objects.filter(user=self, date=datetime.date.today())

        if daytistic.exists():
            return daytistic[0].activities
        else:
            return None

    def get_daytistics_by_time_updated(self, limit: int = -1) -> List[Daytistic]:
        if limit < -1:
            raise ValueError("Please provide a limit >= -1")

        user_daytistics = Daytistic.objects.filter(user=self)

        if limit == -1:
            return user_daytistics

        return user_daytistics.order_by("-updated_at")[:limit]

    def get_daytistics_by_time_created(self, limit: int = -1) -> List[Daytistic]:
        if limit < -1:
            raise ValueError("Please provide a limit >= -1")

        user_daytistics = Daytistic.objects.filter(user=self)

        if limit == -1:
            return user_daytistics

        return user_daytistics.order_by("-created_at")[:limit]

    def get_daytistics_by_date(self, limit: int = -1) -> List[Daytistic]:
        if limit < -1:
            raise ValueError("Please provide a limit >= -1")

        user_daytistics = Daytistic.objects.filter(user=self)

        if limit == -1:
            return user_daytistics

        return user_daytistics.order_by("-date")[:limit]

    def get_daytistics_randomized(self, limit: int = 5) -> List[Daytistic]:
        if limit < 1:
            raise ValueError("Please provide a limit > 0")

        user_daytistics = Daytistic.objects.filter(user=self)

        if limit > user_daytistics.count():
            return user_daytistics

        return choices(user_daytistics, k=limit)
