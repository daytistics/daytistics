from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('current_template', views.edit_daytistic_view, name='current_template'),
    path('daytistic/create', views.create_daytistic, name='create_daytistic'),
    path("daytistic/<int:daytistic_id>/edit/", views.edit_daytistic_view,  name="edit_daytistic"),
    path('activities/list', views.available_activities_view, name='activities_list'),
    path('daytistic/<int:daytistic_id>/add_activity/', views.add_activity_to_daytistic_view, name='add_activity_to_daytistic'),
]