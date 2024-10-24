from django.db import models
from ..daytistics.models import Daytistic


class WellbeingEntry(models.Model):
    """
    Model representing a wellbeing entry. A wellbeing entry is a specific type of wellbeing that a user has rated on a specific day.
    """

    daytistic = models.ForeignKey(
        Daytistic, on_delete=models.CASCADE, related_name="wellbeing_entries"
    )
    type = models.ForeignKey(
        "WellbeingType", on_delete=models.CASCADE, related_name="wellbeing_entries"
    )
    rating = models.IntegerField(default=5)


class WellbeingType(models.Model):
    """
    Model representing a wellbeing type. A wellbeing type is a specific type of wellbeing that a user can rate
    """

    name = models.CharField(max_length=255)
