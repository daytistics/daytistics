from django.contrib import admin
from django.urls import path, include
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='home'),
    path('impressum/', lambda request: render(request, 'home/impressum.html'), name='impressum'),
    path('licenses/', lambda request: render(request, 'home/licenses.html'), name='licenses'),
]