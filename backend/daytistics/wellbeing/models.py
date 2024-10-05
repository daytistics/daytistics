from django.db import models
from ..daytistics.models import Daytistic


# Create your models here.
class WellbeingEntry(models.Model):
    daytistic = models.ForeignKey(
        Daytistic, on_delete=models.CASCADE, related_name="wellbeing_entries"
    )
    type = models.ForeignKey(
        "WellbeingType", on_delete=models.CASCADE, related_name="wellbeing_entries"
    )
    rating = models.IntegerField(default=5)


# Wellbeing Type Model
class WellbeingType(models.Model):
    name = models.CharField(max_length=255)