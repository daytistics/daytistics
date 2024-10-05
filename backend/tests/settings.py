from daytistics.config.settings.prod import *

ALLOWED_HOSTS = ["*"]

TESTING = True

# DATABASE SETTINGS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "tests.sqlite3",
    }
}
