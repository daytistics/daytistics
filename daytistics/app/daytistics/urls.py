from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "daytistics"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.create_daytistic, name="create_daytistic"),
    path("<int:daytistic_id>/edit/", views.edit_daytistic, name="edit_daytistic"),
    path(
        "<int:daytistic_id>/add-activity/",
        views.add_activity_to_daytistic,
        name="add_activity_to_daytistic",
    ),
]
