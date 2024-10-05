from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
