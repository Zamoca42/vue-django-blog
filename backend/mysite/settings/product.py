import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'server.zamoca.space',
]

STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': get_secret("AWS_RDS_HOST"),
        'PORT': '5432',
        'NAME': get_secret("AWS_RDS_NAME"),
        'USER': get_secret("AWS_RDS_USER"),
        'PASSWORD': get_secret("AWS_RDS_PASSWORD"),
    }
}
