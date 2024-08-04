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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.activity.name} - {self.start_time} - {self.end_time}'
    
    def duration(self):
        return self.end_time - self.start_time
    
class Daytistic(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    activities = models.ManyToManyField(Activity, related_name='daytistics', max_length=100)

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.activity.name} - {self.duration}'
    