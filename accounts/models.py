from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    activities = models.ManyToManyField('main.Activity', related_name='users', blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            from main.models import Activity
            for activity in Activity.objects.filter(is_global=True):
                self.activities.add(activity)