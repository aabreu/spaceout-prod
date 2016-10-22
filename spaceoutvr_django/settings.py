"""
Django settings for SpaceoutVR project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECUREKEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
IS_LOCAL = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [ 'localhost', '.mybluemix.net' ]

ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'rest_framework',
    'spaceoutvr',
    'account',
    'user_management.api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'account.context_processors.account',
]

MIGRATION_MODULES = {
    'api': 'spaceoutvr.migrations.user_management_api',  # substitute the path to your projectmigrations folder
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': {
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'user_management.api.authentication.TokenAuthentication',
    },
}

ROOT_URLCONF = 'spaceoutvr_django.urls'

WSGI_APPLICATION = 'spaceoutvr_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


if IS_LOCAL:
    DATABASES = {
    	'default': {
    		'ENGINE': 'django.db.backends.mysql',
    		'NAME': "spaceoutvr",
    		'USER': "root",
    		'PASSWORD': "root",
    		'HOST': "localhost",
    		'PORT': "8889"
    	}
    }
else:
    import json
    MYSQL = json.loads(os.environ['VCAP_SERVICES'])['cleardb'][0]['credentials']
    DATABASES = {
    	'default': {
    		'ENGINE': 'django.db.backends.mysql',
    		'NAME': MYSQL['name'],
    		'USER': MYSQL['username'],
    		'PASSWORD': MYSQL['password'],
    		'HOST': MYSQL['hostname'],
    		'PORT': MYSQL['port']
    	}
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

AUTH_USER_MODEL = 'spaceoutvr.SpaceoutUser'
SENTRY_CLIENT = 'user_management.utils.sentry.SensitiveDjangoClient'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'agustinabreu@gmail.com'
EMAIL_HOST_PASSWORD = '$pac30utVR'
# EMAIL_HOST_PASSWORD = 'G0rri0nV3ntanaT3rmo'
EMAIL_PORT = 587
