from .base import *

DATA_DIR = BASE_DIR.ancestor(1).child("data")

DEBUG = True

EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'grades',
        'HOST': 'localhost',
    }
}