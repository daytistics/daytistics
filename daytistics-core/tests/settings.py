from config.settings.dev import *

# DJANGO SETTINGS

DEBUG = False

ALLOWED_HOSTS = ['localhost', 'example.com']

# DATABASE SETTINGS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}