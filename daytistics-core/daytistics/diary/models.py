from django.db import models
from ..daytistics.models import Daytistic


# Create your models here.
class DiaryEntry(models.Model):
    entry = models.TextField()
    moment_of_happiness = models.TextField()
