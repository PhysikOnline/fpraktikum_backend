"""
Django settings for po_fp project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import re
import logging

from corsheaders.defaults import default_headers

import environ

ROOT_DIR = environ.Path(
    __file__) - 2  # ==>( po-fp-django/po_fp/settings.py - 2 = po-fp-django/)
# po-fp-django/po_fp/settings.py - 2 = po-fp-django/
APPS_DIR = ROOT_DIR.path('fpraktikum')


env = environ.Env()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", 'secret')
# '55$vbbbgy8kyw=^=w45%s))24*#0_^y8p4ngp*mxf&snnr1v&7'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = bool(os.environ.get("DEBUG", default=False))

ALLOWED_HOSTS = environ.Env().list('DJANGO_ALLOWED_HOSTS')

#['web', 'localhost' ,'po-fp-staging.physikelearning.de'] if os.environ.get("NODEBUG") is None else ["po-fp.physikelearning.de"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fpraktikum',
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'import_export',
    'raven.contrib.django.raven_compat',
    'gunicorn'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'

]

ROOT_URLCONF = 'po_fp.urls'

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

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.load_template_source',
#     'django.template.loaders.app_directories.load_template_source',
# )

WSGI_APPLICATION = 'po_fp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if os.environ.get("IN_DOCKER"):

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'HOST': 'db',
            'PASSWORD': 'password',
            'PORT': 5432,
        },
        'ilias_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': str(os.environ.get("ILIAS_DB_NAME")),
            'USER': str(os.environ.get("ILIAS_DB_USER")),
            'PASSWORD': str(os.environ.get("ILIAS_DB_PASS")),
            'HOST': str(os.environ.get("ILIAS_DB_HOST")),
            'PORT': int(os.environ.get("ILIAS_DB_PORT")),
        },
    }


elif os.environ.get("DATABASE_URL"):

    USER, PASSWORD, HOST, PORT, NAME = re.match(
        "^postgres://(?P<username>.*?)\:(?P<password>.*?)\@(?P<host>.*?)\:(?P<port>\d+)\/(?P<db>.*?)$",
        os.environ.get("DATABASE_URL", "")).groups()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': NAME,
            'USER': USER,
            'PASSWORD': PASSWORD,
            'HOST': HOST,
            'PORT': int(PORT),
        },
        'ilias_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': str(os.environ.get("ILIAS_DB_NAME")),
            'USER': str(os.environ.get("ILIAS_DB_USER")),
            'PASSWORD': str(os.environ.get("ILIAS_DB_PASS")),
            'HOST': str(os.environ.get("ILIAS_DB_HOST")),
            'PORT': int(os.environ.get("ILIAS_DB_PORT")),
        },
    }
else:
    pass

# e-mail settings

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# STATIC_ROOT = ''
#
# # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
# STATIC_URL = '/staticfiles/'
#
# # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
# STATICFILES_DIRS = ()

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FILE_UPLOAD_MAX_MEMORY_SIZE
FILE_UPLOAD_MAX_MEMORY_SIZE = 200000000

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES':
        ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
    'DEFAULT_RENDERER_CLASSES':
        ('rest_framework.renderers.JSONRenderer',
         'rest_framework.renderers.BrowsableAPIRenderer'
         ),
    'TEST_REQUEST_DEFAULT_FORMAT':
        'json',
}

# CORS Headers Configuration

# for testing this will be set, in futere we will integrate the Whitelist

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = default_headers + ('token',)

ADMINS =[("Christian Grossmüller", "christian@elearning.physik.uni-frankfurt.de")]

# CORS_ORIGIN_WHITELIST = ()

if not DEBUG:
    # Sentry Configuration
    SENTRY_DSN = env("DJANGO_SENTRY_DSN")
    SENTRY_CLIENT = env(
        "DJANGO_SENTRY_CLIENT", default="raven.contrib.django.raven_compat.DjangoClient"
    )
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "root": {"level": "WARNING", "handlers": ["sentry"], },
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                          "%(process)d %(thread)d %(message)s"
            },
        },
        "handlers": {
            "sentry": {
                "level": "ERROR",
                "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django.db.backends": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            "raven": {"level": "DEBUG", "handlers": ["console"], "propagate": False, },
            "sentry.errors": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
            "django.security.DisallowedHost": {
                "level": "ERROR",
                "handlers": ["console", "sentry"],
                "propagate": False,
            },
        },
    }
    SENTRY_CELERY_LOGLEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)
    RAVEN_CONFIG = {
        "CELERY_LOGLEVEL": env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO),
        "DSN": SENTRY_DSN,
    }
