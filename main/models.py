from django.db import models
from django.conf import settings


# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=100)
    is_global = models.BooleanField(default=False)
    user = models.ManyToOneRel(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to='id', field_name='user')

    def __str__(self):
        return self.name
    
class ActivityEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    duration = models.DurationField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def duration_in_seconds(self):
        return self.duration.total_seconds()

    def __str__(self):
        return f'{self.user.username} - {self.activity.name} - {self.start_time} - {self.end_time}'
    
class Daytistic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    activities = models.ManyToManyField(ActivityEntry, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.activity.name} - {self.duration}'
    