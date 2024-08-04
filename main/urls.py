from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('daytistic/create/', views.create_daytistic, name='create_daytistic'),
    path('daytistic/save/', views.save_daytistic, name='save_daytistic'),
]