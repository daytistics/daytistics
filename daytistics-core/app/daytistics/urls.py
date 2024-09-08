from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'daytistics'

urlpatterns = [
	path('dashboard/', views.dashboard, name='dashboard'),
	path('create/', views.create_daytistic, name='create_daytistic'),
	path('<int:daytistic_id>/edit/', views.edit_daytistic, name='edit_daytistic'),
	path('<int:daytistic_id>/list-activities/json', views.list_activities_as_json, name='list_activities_as_json'),
	path(
		'<int:daytistic_id>/add-activity/',
		views.add_activity_to_daytistic,
		name='add_activity_to_daytistic',
	),
	path(
		'<int:daytistic_id>/delete/',
		views.delete_daytistic,
		name='delete_daytistic',
	),
	path(
		'<int:daytistic_id>/edit-activity-entry/',
		views.edit_activity_entry,
		name='edit_activity_entry',
	),
	path(
		'<int:daytistic_id>/toggle-important/',
		views.toggle_important,
		name='toggle_important',
	),
    
]
