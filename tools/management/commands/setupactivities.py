from django.core.management.base import BaseCommand
from main.models import Activity
from settings.main import DEFAULT_ACTIVITIES

class Command(BaseCommand):
    help = 'Setup activities'

    def handle(self, *args, **options):
        for activity in DEFAULT_ACTIVITIES:
            if not Activity.objects.filter(name=activity).exists():
                Activity.objects.create(name=activity, is_global=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully created activity {activity}'))
            else:
                self.stdout.write(self.style.WARNING(f'Activity {activity} already exists'))
        self.stdout.write(self.style.SUCCESS('Successfully created activities'))