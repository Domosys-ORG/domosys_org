"""
Django settings for domosys_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#SESSION_ENGINE='django.contrib.sessions.backends.cached_db'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = open("domosys_web/SECRET_KEY", "r").read()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = open("domosys_web/ALLOWED_HOSTS", "r").read().split('\n')

TEMPLATE_DIRS = (
    BASE_DIR + '/templates/'
)
TEMPLATE_LOADERS=(
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},
	'handlers': {
		'console':{
			'level': 'WARNING',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'propagate': True,
			'level': 'INFO',
		},
		'conf.views': {
			'handlers': ['console'],
			'level': 'DEBUG',
		},
	}
}
	
import djcelery
djcelery.setup_loader()
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
	'base',
	'conf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'domosys_web.urls'

WSGI_APPLICATION = 'domosys_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'django',
		'USER': 'django', 
		'PASSWORD': open("domosys_web/pg_django.pass", "r").read(), 
		'HOST': 'localhost', 
		'PORT': '', 
	}
} 
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
#STATICFILES_DIRS = (
#	
#)
''' Celery Config '''
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json'] #, 'yaml']
CELERY_TIMEZONE = 'Europe/Paris'
CELERY_ENABLE_UTC = True
NOTIFY_USE_JSONFIELD=True

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'

if not DEBUG:
	CACHES = {
		"default": {
			"BACKEND": "redis_cache.cache.RedisCache",
			"LOCATION": "localhost:6379:0",
			"OPTIONS": {
			    "CLIENT_CLASS": "redis_cache.client.DefaultClient",
			}
		}
	}
else:
	CACHES = {
		'default': {
			'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
		}
	}

