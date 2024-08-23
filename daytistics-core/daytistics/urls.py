from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='daytistics_dashboard'),
    path('create/', views.create_daytistic, name='daytistics_create'),
    path("<int:daytistic_id>/edit/", views.edit_daytistic_view,  name="daytistics_edit"),
    path('<int:daytistic_id>/add-activity/', views.add_activity_to_daytistic_view, name='daytistics_add_activity'),
]