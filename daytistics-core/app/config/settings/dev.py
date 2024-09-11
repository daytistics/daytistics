from app.config.settings.base import *

# DJANGO SETTINGS

DEBUG = True

CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS += [f'http://{host}' for host in ALLOWED_HOSTS]
CSRF_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

print(f'CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}')

# EMAIL SETTINGS

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')


# DATABASE SETTINGS

DATABASES = {
	'default': {
		'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
		'NAME': BASE_DIR.parent / os.getenv('DATABASE_NAME', 'db.sqlite3'),
	}
}
