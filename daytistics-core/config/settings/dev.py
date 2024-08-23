from config.settings.base import *

# DJANGO SETTINGS

DEBUG = True


# EMAIL SETTINGS

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# DATABASE SETTINGS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}