from app.config.settings.base import *

# DJANGO SETTINGS

DEBUG = True


# EMAIL SETTINGS

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")


# DATABASE SETTINGS

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": BASE_DIR.parent / os.getenv("DATABASE_NAME", "db.sqlite3"),
    }
}
