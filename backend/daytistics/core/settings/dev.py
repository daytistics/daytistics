from daytistics.core.settings.base import *

# DJANGO SETTINGS

DEBUG = True

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
CSRF_ALLOWED_ORIGINS = os.getenv("CSRF_ALLOWED_ORIGINS", "").split(",")


# CORS SETTINGS

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True

# EMAIL SETTINGS

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)


# DATABASE SETTINGS

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": BASE_DIR.parent / os.getenv("DATABASE_NAME", "db.sqlite3"),
    }
}
