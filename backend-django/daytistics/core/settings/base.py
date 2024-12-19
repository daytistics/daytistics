from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

from daytistics.core.settings.constants import *


# DJANGO SETTINGS

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = str(os.getenv("DJANGO_ALLOWED_HOSTS")).split(",")

ROOT_URLCONF = "daytistics.core.urls"

WSGI_APPLICATION = "daytistics.core.wsgi.application"

SITE_URL = "http://127.0.0.1:8000"

TESTING = False

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    # Custom Apps
    "daytistics.daytistics",
    "daytistics.activities",
    "daytistics.users",
    "daytistics.wellbeing",
    "daytistics.diary",
    # Django Apps
    "django.contrib.admin",
    "django.contrib.modules.users",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # Third Party Apps
    "corsheaders",
    "ninja_extra",
    # Authentication
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.modules.users.middleware.modules.usersenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]


# AUTHENTICATION SETTINGS

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = [
    "allauth.account.modules.users_backends.modules.usersenticationBackend",
    "django.contrib.modules.users.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.modules.users.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.modules.users.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.modules.users.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.modules.users.password_validation.NumericPasswordValidator",
    },
]


# CSRF SETTINGS
CSRF_COOKIE_NAME = "csrf_token"
CSRF_USE_SESSIONS = False

# TEMPLATE SETTINGS

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.modules.users.context_processors.modules.users",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "builtins": [],
            "libraries": {},
        },
    },
]

# STATIC FILES SETTINGS

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# TAILWIND SETTINGS

TAILWIND_APP_NAME = "daytistics.theme"

INTERNAL_IPS = [
    "127.0.0.1",
]

# LOADING ENVIRONMENT VARIABLES

FRONTEND_URL = os.getenv("FRONTEND_URL")

# INTERNATIONALIZATION SETTINGS

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

# MISCELLANEOUS SETTINGS

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

NPM_BIN_PATH = "/usr/bin/npm"
