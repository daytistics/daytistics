from config.settings.dev import *

# DJANGO SETTINGS

DEBUG = False


# DATABASE SETTINGS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}