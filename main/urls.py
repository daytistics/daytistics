from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('current_template', views.edit_daytistic_view, name='current_template'),
    path('activities/list', views.available_activities_view, name='activities_list'),
    path('daytistic/today/activities', views.get_todays_activities, name='todays_activities'),
]