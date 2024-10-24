from django.db import models
from ..users.models import CustomUser


class Daytistic(models.Model):
    """
    Model representing a daytistic. A daytistic is a collection of activities for a specific day. This model is the core of the application.
    """

    date = models.DateField()
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="daytistics"
    )
    diary = models.OneToOneField(
        "diary.DiaryEntry",
        null=True,
        on_delete=models.SET_NULL,
        related_name="daytistic",
    )
    activities = models.ManyToManyField(
        "activities.ActivityEntry", related_name="daytistics", blank=True
    )
    wellbeings = models.ManyToManyField(
        "wellbeing.WellbeingEntry", related_name="daytistics", blank=True
    )

    @property
    def total_duration(self):
        """
        Calculate the total duration of all activities in the daytistic.

        Returns:
            int: The total duration of all activities in the daytistic
        """

        return sum(activity.duration for activity in self.activities.all())

    def __str__(self):
        return f"Daytistic: {self.date} ({self.user.username})"

    def __repr__(self):
        return f"Daytistic(user={self.user.username}, date={self.date})"
