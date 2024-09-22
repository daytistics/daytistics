from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path("csrf-token/", views.CsrfToken.as_view(), name="csrf-token"),
]
