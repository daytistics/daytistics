from django.db import models


class ActivityEntry(models.Model):
    """
    Model representing an activity entry. An activity entry is a specific activity that a user has done on a specific day.
    """

    type = models.ForeignKey(
        "ActivityType", on_delete=models.CASCADE, related_name="type"
    )
    start_time = models.IntegerField()  # Time in minutes
    end_time = models.IntegerField()  # Time in minutes

    @property
    def duration(self) -> int:
        """
        Calculate the duration of the activity.
        """

        return self.end_time - self.start_time


# Will soon be removed
class ActivityCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, default="")

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    """
    Model representing an activity type. An activity type is a specific type of activity that a user can do.
    """

    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        ActivityCategory, on_delete=models.CASCADE, related_name="activities"
    )
    active = models.BooleanField(default=False)
