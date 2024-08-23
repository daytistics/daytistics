from django.db import models
from django.conf import settings

class Activity(models.Model):
    name = models.CharField(max_length=100)
    is_global = models.BooleanField(default=False)
    users = models.ManyToOneRel(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to='id', field_name='users')

    def __str__(self):
        return self.name