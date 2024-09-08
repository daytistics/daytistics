from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import render

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("daytistics/", include("app.daytistics.urls")),
)

urlpatterns += [
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

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
		settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
	)
