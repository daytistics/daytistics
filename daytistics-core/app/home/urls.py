from django.urls import path
from django.shortcuts import render

urlpatterns = [
    path("", lambda request: render(request, "home/home.html"), name="home"),
    path(
        "imprint/",
        lambda request: render(request, "home/impressum.html"),
        name="imprint",
    ),
    path(
        "licenses/",
        lambda request: render(request, "home/licenses.html"),
        name="licenses",
    ),
]
