from django.db import models
from django.conf import settings
from app.activities.models import Activity
from datetime import timedelta


class Daytistic(models.Model):
	"""
	Model representing a daytistic. A daytistic is a collection of activities for a specific day. This model is the core of the application.
	"""

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date = models.DateField(default=None)
	important = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
 
	def get_total_duration(self, human_readable=True):
		"""
		Property to return the total duration of all activities in the daytistic.

		Returns:
			timedelta: Total duration of all activities in the daytistic.
		"""
		
		total_duration = sum([activity.duration for activity in self.activities.all()], timedelta())
  
		if human_readable:
			hours, remainder = divmod(total_duration.seconds, 3600)
			minutes, _ = divmod(remainder, 60)
			return f'{hours:02}:{minutes:02}'
		return total_duration


	def __str__(self):
		return f'Datistic: {self.date} ({self.user.username})'

	def __repr__(self):
		return f'Daytistic(user={self.user.username}, date={self.date})'


class ActivityEntry(models.Model):
	"""
	Model representing an activity entry. An activity entry is a record of an activity performed by a user on a specific day. Activity entries are associated with a daytistic.
	"""

	daytistic = models.ForeignKey(Daytistic, on_delete=models.CASCADE, related_name='activities')
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	duration = models.DurationField(default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property
	def human_readable_duration(self):
		"""
		Property to return the duration of the activity entry in a human-readable format.

		Returns:
			str: Human-readable duration of the activity entry.
		"""
		hours, remainder = divmod(self.duration.seconds, 3600)
		minutes, _ = divmod(remainder, 60)

		return f'{hours:02}:{minutes:02}'

	def __str__(self):
		return f'Activity Entry: {self.activity.name} ({self.daytistic.date} - {self.daytistic.user.username})'

	def __repr__(self):
		return f'ActivityEntry(daytistic={self.daytistic}, activity={self.activity}, duration={self.duration})'
