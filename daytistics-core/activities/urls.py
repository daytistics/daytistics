    


from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('list/as-options/', views.available_activities_as_options_list_view, name='activities_availables_as_options_list'),
]