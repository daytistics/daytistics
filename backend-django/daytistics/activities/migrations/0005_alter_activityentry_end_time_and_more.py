# Generated by Django 5.1.1 on 2024-10-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0004_remove_activityentry_daytistic_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activityentry",
            name="end_time",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="activityentry",
            name="start_time",
            field=models.IntegerField(),
        ),
    ]