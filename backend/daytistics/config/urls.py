from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .api import api
from django.urls import re_path
from django.shortcuts import redirect
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    re_path(
        r"^.*$",
        lambda request: redirect(os.environ.get("FRONTEND_URL")),
        name="catch_all",
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
