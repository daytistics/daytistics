from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Activity
from config.app_settings import DEFAULT_ACTIVITIES

@receiver(post_migrate)
def create_default_activities(sender, **kwargs):
    if sender.name == 'daytistics':  # Ensure the signal is only processed for the 'main' app
        for activity in DEFAULT_ACTIVITIES:
            if not Activity.objects.filter(name=activity).exists():
                Activity.objects.create(name=activity, is_global=True)
                print(f'Activity {activity} created')
        print('Default activities created if they did not exist')
