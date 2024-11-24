from django.db import models


class DiaryEntry(models.Model):
    """
    Model representing a diary entry. A diary entry is a specific entry that a user has written on a specific
    """

    entry = models.TextField()
    moment_of_happiness = models.TextField()
