from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
