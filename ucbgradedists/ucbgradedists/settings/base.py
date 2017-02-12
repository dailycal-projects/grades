import os
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from unipath import Path

# Number of digits to use in rounding mean and standard deviation
PRECISION = 3

def env_var(var_name):
    """Get the environment variable VAR_NAME, or raise an Exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        msg = "You need to set the {} environment variable.".format(var_name)
        raise ImproperlyConfigured(msg)

# Basic settings

SECRET_KEY = env_var('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = []
ADMINS = (
    (env_var('ADMIN_NAME'), env_var('ADMIN_EMAIL')),
)

# Email settings, assuming you use gmail.

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
SERVER_EMAIL = ''

# Set up directory structure and static files

BASE_DIR = Path(__file__).ancestor(3)
DATA_DIR = BASE_DIR.ancestor(1).child("data")
MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child("staticfiles")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR.child("static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mathfilters',
    'sass_processor',
    'django_extensions',
    'bakery',
    'core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ucbgradedists.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child("templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ucbgradedists.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = { 'default': dj_database_url.config() }
DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Bakery

BUILD_DIR = BASE_DIR.child("build")

BAKERY_VIEWS = (
    'graphic.views.GraphicView',
)

AWS_BUCKET_NAME = env_var('AWS_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env_var('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env_var('AWS_SECRET_ACCESS_KEY')
