from app.config.settings.prod import *

ALLOWED_HOSTS = ['*']

# DATABASE SETTINGS

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}
