from django.db import models
from django.conf import settings


class Activity(models.Model):
    """
    Model representing an activity.

    Attributes:
        name (str): The name of the activity.
        is_global (bool): Indicates if the activity is global or not.
        users (ManyToOneRel): The relationship to the users associated with the activity.
    """
    
    name = models.CharField(max_length=100)
    is_global = models.BooleanField(default=False)
    users = models.ManyToOneRel(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to="id", field_name="users"
    )

    def __str__(self):
        if self.is_global: return f"Global activity: {self.name}"

        return f"Activity: {self.name}"
    
    def __repr__(self):
        return f"Activity(name={self.name}, is_global={self.is_global})"
