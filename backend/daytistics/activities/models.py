from django.db import models


class ActivityEntry(models.Model):
    type = models.ForeignKey(
        "ActivityType", on_delete=models.CASCADE, related_name="type"
    )
    start_time = models.IntegerField()  # Time in minutes
    end_time = models.IntegerField()  # Time in minutes

    @property
    def duration(self) -> int:
        """
        Returns the duration of the activity in minutes.
        """
        return self.end_time - self.start_time


class ActivityCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        ActivityCategory, on_delete=models.CASCADE, related_name="activities"
    )
    active = models.BooleanField(default=False)
