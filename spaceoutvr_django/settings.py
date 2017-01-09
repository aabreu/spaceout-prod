"""
Django settings for SpaceoutVR project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from imp import reload

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECUREKEY')
SECRET_KEY = "efhiuwehfiuwehfiuehuighiowejfioewjio"

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
IS_LOCAL = DEBUG
IS_DEV = True

TEMPLATE_DEBUG = False

if IS_LOCAL:
    reload(sys)
    sys.setdefaultencoding("utf-8")


SPACEOUT_SEND_NOTIFICATIONS = True
SPACEOUT_STORE_COMMENTS = True
# SPACEOUT_STORE_COMMENTS = not IS_LOCAL

ONESIGNAL_API_KEY = 'MzZjNTUwMjYtNTU5Yy00M2UzLWFkZGYtZmMyYmQwZWVmNjU3'
ONESIGNAL_APP_ID = '2309120b-b9a7-498a-b7ae-97749ab28130'

# SERVER_URL = 'https://spaceoutvr-dev.mybluemix.net'
SERVER_URL = 'https://spaceoutvr-prod.mybluemix.net'
if IS_LOCAL:
    # SERVER_URL = 'http://192.168.0.109:8000'
    SERVER_URL = 'http://127.0.0.1:8000'


ALLOWED_HOSTS = [ 'localhost', '.mybluemix.net' ]

# ACCOUNT_EMAIL_UNIQUE = True
# ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True

AUTH_USER_MODEL = 'spaceoutvr.SpaceoutUser'
AUTH_EMAIL_VERIFICATION = True

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'spaceoutvr',
    'authemail',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

ROOT_URLCONF = 'spaceoutvr_django.urls'

WSGI_APPLICATION = 'spaceoutvr_django.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


if IS_LOCAL:
    DATABASES = {
    	# 'default': {
    	# 	'ENGINE': 'django.db.backends.mysql',
    	# 	'NAME': "spaceoutvr_prod",
    	# 	'USER': "root",
    	# 	'PASSWORD': "root",
    	# 	'HOST': "localhost",
    	# 	'PORT': "8889"
    	# }
    	'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'spaceoutvr_prod',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
elif IS_DEV:
    # dev
    import json
    import dj_database_url
    print("###################### DB CONFIG #######")
    DATABASES = {'default': dj_database_url.config()}

    print(DATABASES)
    # DATABASES = {
    # 	'default': {
    # 		'ENGINE': 'django.db.backends.postgresql_psycopg2',
    # 		'NAME': 'zplzauwd',
    # 		'USER': 'zplzauwd',
    # 		'PASSWORD': 'LNkFZnLiYKIfu598mv7UnVJnTIal9zZr',
    # 		'HOST': 'echo-01.db.elephantsql.com',
    # 		'PORT': '5432'
    # 	}
    # }


else:
    # production
    import json
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
    # MYSQL = json.loads(os.environ['VCAP_SERVICES'])['cleardb'][0]['credentials']
    # DATABASES = {
    # 	'default': {
    # 		'ENGINE': 'django.db.backends.mysql',
    # 		'NAME': MYSQL['name'],
    # 		'USER': MYSQL['username'],
    # 		'PASSWORD': MYSQL['password'],
    # 		'HOST': MYSQL['hostname'],
    # 		'PORT': MYSQL['port']
    # 	}
    # }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = 'http://spaceoutvr-static.mybluemix.net/'

if IS_LOCAL:
    STATIC_ROOT = '../spaceoutvr-static'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
else:
    STATIC_ROOT = "static"


# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

SENTRY_CLIENT = 'user_management.utils.sentry.SensitiveDjangoClient'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'do-not-reply@spaceoutvr.com'
EMAIL_HOST_PASSWORD = 'faimzfcvlipfulqo'
# EMAIL_HOST_PASSWORD = 'picklejuice'
# EMAIL_HOST_USER = 'spaceoutvrplaceholder@gmail.com'
# EMAIL_HOST_PASSWORD = 'Daydr3am10'
EMAIL_PORT = 587
DEFAULT_EMAIL_BCC = ''
DEFAULT_EMAIL_FROM = ''

GOOGLE_API_KEY = "&key=AIzaSyBeonrqnW72dlUQnhfYwiy6lpir-S3MtLo"

GOOGLE_SEARCH_ENGINE_ID = "&cx=006816680771764323813:srygeqcrtpc"
GOOGLE_SEARCH_URL = "&fileType=png+jpg&searchType=image&filter=1"
GOOGLE_SEARCH_BASE_URL = "https://www.googleapis.com/customsearch/v1"

STREET_VIEW_API_URL = "http://maps.googleapis.com/maps/api/streetview?size=512x512&location=%s,%s&fov=%s&heading=%s&pitch=%s%s"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=%s%s"

LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}

OBJECT_STORAGE_PROJECT_ID = '000d40f501d24442a0e152e3d285a79d'
OBJECT_STORAGE_USER_ID = '0b288ba024754160b0e904842fe32ce8'
OBJECT_STORAGE_PASSWORD = 'it-kDXeduV5x]0gP'

OBJECT_STORAGE_COMMENTS_CONTAINER = 'comments-prod'
OBJECT_STORAGE_WATSON_CONTAINER = 'watson-prod'
OBJECT_STORAGE_MISC_CONTAINER = 'misc-prod'

if(IS_LOCAL or IS_DEV):
    OBJECT_STORAGE_COMMENTS_CONTAINER = 'comments-local'
    OBJECT_STORAGE_WATSON_CONTAINER = 'watson-local'
    OBJECT_STORAGE_MISC_CONTAINER = 'misc-local'

# STATICFILES_STORAGE = 'spaceoutvr.storage.StaticStorage'
# STATIC_URL = "https://dal.objectstorage.open.softlayer.com/v1/AUTH_%s/%s/" % (OBJECT_STORAGE_PROJECT_ID, OBJECT_STORAGE_STATIC_CONTAINER)
