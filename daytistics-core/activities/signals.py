from django.db.models.signals import post_migrate
from django.dispatch import receiver
from activities.models import Activity
import os

@receiver(post_migrate)
def create_default_activities(sender, **kwargs):
    if sender.name == 'activities':  
        for activity in os.environ.get('DEFAULT_ACTIVITIES', '').split(','):
            if not Activity.objects.filter(name=activity).exists():
                Activity.objects.create(name=activity, is_global=True)
                print(f'Activity {activity} created')
        print('Default activities created if they did not exist')
