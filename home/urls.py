from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'pages/home/home.html'), name='home'),
    path('impressum/', lambda request: render(request, 'pages/home/impressum.html'), name='impressum'),
    path('licenses/', lambda request: render(request, 'pages/home/licenses.html'), name='licenses'),
]