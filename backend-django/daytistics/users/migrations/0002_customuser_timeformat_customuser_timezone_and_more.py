# Generated by Django 5.1.1 on 2024-09-26 04:38

import daytistics.users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="timeformat",
            field=models.CharField(default="24h", max_length=50),
        ),
        migrations.AddField(
            model_name="customuser",
            name="timezone",
            field=models.CharField(default="UTC", max_length=50),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_login",
            field=models.DateTimeField(),
        ),
    ]