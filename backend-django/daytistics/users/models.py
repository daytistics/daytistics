from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom User model for the application, which inherits from Django's AbstractUser model and adds additional fields and methods.
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False)
    activities = models.ManyToManyField(
        "activities.ActivityType", related_name="users", blank=True
    )
    date_format = models.CharField(max_length=10, default="%Y-%m-%d")
