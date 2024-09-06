from django.db import models
from django.conf import settings
from app.activities.models import Activity


class Daytistic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.date})"


class ActivityEntry(models.Model):
    daytistic = models.ForeignKey(
        Daytistic, on_delete=models.CASCADE, related_name="activities"
    )
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    duration = models.DurationField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def duration_in_seconds(self):
        return self.duration.total_seconds()

    def __str__(self):
        return (
            f"{self.daytistic.user.username} - {self.activity.name} - {self.duration}"
        )
