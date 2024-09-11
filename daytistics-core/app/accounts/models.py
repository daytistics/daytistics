from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from typing import List
from app.daytistics.models import Daytistic
from random import choices
from app.activities.models import Activity
from typing import List


class CustomUser(AbstractUser):
	"""
	Custom User model for the application, which inherits from Django's AbstractUser model and adds additional fields and methods.
	"""

	username = models.CharField(max_length=150, unique=True)
	activities = models.ManyToManyField('activities.Activity', related_name='users', blank=True)

	@property
	def all_activities(self) -> List[Activity]:
		"""
		Method to return all activities for a user, including global activities.

		Returns:
		    List[Activity]: List of all activities for the user.
		"""
		global_activities = Activity.objects.filter(is_global=True)
		return list(self.activities.all() | global_activities)

	# TODO: Remove this method and replace it with a more efficient one
	def get_todays_activities(self):
		from app.daytistics.models import Daytistic

		daytistic = Daytistic.objects.filter(user=self, date=datetime.date.today())

		if daytistic.exists():
			return daytistic[0].activities
		else:
			return None

	def get_daytistics_by_time_updated(self, limit: int = -1) -> List[Daytistic]:
		"""
		Method to return daytistics for a user, ordered by the time they were last updated.

		Args:
		    limit (int, optional): Number of daytistics to return. Defaults to -1.

		Raises:
		    ValueError: If limit is less than -1.

		Returns:
		    List[Daytistic]: Sorted list of daytistics.
		"""
		if limit < -1:
			raise ValueError('Please provide a limit >= -1')

		user_daytistics = Daytistic.objects.filter(user=self)

		if limit == -1:
			return user_daytistics

		return user_daytistics.order_by('-updated_at')[:limit]

	def get_daytistics_by_time_created(self, limit: int = -1) -> List[Daytistic]:
		"""
		Method to return daytistics for a user, ordered by the time they were created.

		Args:
		    limit (int, optional): Number of daytistics to return. Defaults to -1.

		Raises:
		    ValueError: If limit is less than -1.

		Returns:
		    List[Daytistic]: Sorted list of daytistics.
		"""
		if limit < -1:
			raise ValueError('Please provide a limit >= -1')

		user_daytistics = Daytistic.objects.filter(user=self)

		if limit == -1:
			return user_daytistics

		return user_daytistics.order_by('-created_at')[:limit]

	def get_daytistics_by_date(self, limit: int = -1) -> List[Daytistic]:
		"""
		Method to return daytistics for a user, ordered by their date field.

		Args:
		    limit (int, optional): Number of daytistics to return. Defaults to -1.

		Raises:
		    ValueError: If limit is less than -1.

		Returns:
		    List[Daytistic]: Sorted list of daytistics.
		"""

		if limit < -1:
			raise ValueError('Please provide a limit >= -1')

		user_daytistics = Daytistic.objects.filter(user=self)

		if limit == -1:
			return user_daytistics

		return user_daytistics.order_by('-date')[:limit]

	def get_daytistics_randomized(self, limit: int = 5) -> List[Daytistic]:
		"""
		Method to return a random selection of daytistics for a user.

		Args:
		    limit (int, optional): Number of daytistics to return. Defaults to 5.

		Raises:
		    ValueError: If limit is less than 1.

		Returns:
		    List[Daytistic]: Randomized list of daytistics.
		"""
		if limit < 1:
			raise ValueError('Please provide a limit > 0')

		user_daytistics = Daytistic.objects.filter(user=self)

		if limit > user_daytistics.count():
			return user_daytistics

		return choices(user_daytistics, k=limit)

	def __str__(self):
		return f'{self.username} ({self.email})'

	def __repr__(self):
		return f'CustomUser(username={self.username}, email={self.email})'
