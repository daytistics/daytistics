from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    activities = models.ManyToManyField('activities.Activity', related_name='users', blank=True)

    def get_todays_activities(self):
        from daytistics.models import Daytistic
        import datetime
        daytistic = Daytistic.objects.filter(user=self, date__date=datetime.date.today())

        if daytistic.exists():
            return daytistic[0].activities
        else:
            return None

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            from daytistics.models import Activity
            for activity in Activity.objects.filter(is_global=True):
                self.activities.add(activity)