    


from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('list', views.available_activities_view, name='activities_list'),
]