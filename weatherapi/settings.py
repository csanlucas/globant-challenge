"""
Django settings for weatherapi project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

from .secrets import Config
from .environments import ALLOWED_ENVS, ENV_LOCAL, ENV_PROD

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_8z8f84_+fqucb%)773i(284vebm#wi&omo1#xrkkp509q+t6f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Current ENVIRONMENT config
GLOBANTAPI_ENV = os.environ.get('GLOBANTAPI_ENV', ENV_LOCAL)
if GLOBANTAPI_ENV == ENV_PROD:
    DEBUG = False
if GLOBANTAPI_ENV not in ALLOWED_ENVS:
    raise Exception('GLOBANTAPI_ENV must be on of ({})'.format(ALLOWED_ENVS))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'weather'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'weatherapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'weatherapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

Config.set_database_credentials(env=GLOBANTAPI_ENV)

if not Config.DATABASE_CRED:
    raise Exception("Can not setup database configuration for {} not defined".format(GLOBANTAPI_ENV))

if GLOBANTAPI_ENV == ENV_PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': Config.DATABASE_CRED['NAME'],
            'USER': Config.DATABASE_CRED['USER'],
            'PASSWORD': Config.DATABASE_CRED['PASSWORD'],
            'HOST': Config.DATABASE_CRED['HOST'],
            'PORT': Config.DATABASE_CRED['PORT'],
            'ATOMIC_REQUESTS': True
        }
    }
elif GLOBANTAPI_ENV == ENV_LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': Config.DATABASE_CRED['NAME'],
            'USER': Config.DATABASE_CRED['USER'],
            'PASSWORD': Config.DATABASE_CRED['PASSWORD'],
            'HOST': Config.DATABASE_CRED['HOST'],
            'PORT': Config.DATABASE_CRED['PORT'],
            'ATOMIC_REQUESTS': True
        }
    }
else:
    raise Exception("Database configuration for {} not defined".format(GLOBANTAPI_ENV))

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'weather_cache_table',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
