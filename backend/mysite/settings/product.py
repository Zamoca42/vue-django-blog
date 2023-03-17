import os
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

DEBUG = False

ALLOWED_HOSTS = [
    'server.zamoca.space',
]

STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

MEDIA_URL = 'https://server.zamoca.space/media/'
# SECURE_CROSS_ORIGIN_OPENER_POLICY = None

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

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
