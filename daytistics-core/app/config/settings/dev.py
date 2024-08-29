from app.config.settings.base import *

# DJANGO SETTINGS

DEBUG = True


# EMAIL SETTINGS

EMAIL_BACKEND = "django.app.mail.backends.console.EmailBackend"


# DATABASE SETTINGS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
    }
}
