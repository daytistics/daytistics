from django.db import models
from ..daytistics.models import Daytistic


class ActivityEntry(models.Model):
    daytistic = models.ForeignKey(
        Daytistic, on_delete=models.CASCADE, related_name="activity_entries"
    )
    type = models.ForeignKey(
        "ActivityType", on_delete=models.CASCADE, related_name="activity_entries"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def duration(self):
        """
        Returns the duration of the activity in minutes.
        """
        return (self.end_time - self.start_time).total_seconds() / 60


# Activity Type Model
class ActivityType(models.Model):
    name = models.CharField(max_length=255, unique=True)
