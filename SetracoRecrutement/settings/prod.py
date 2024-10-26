"""
Django settings for SetracoRecrutement project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

DEBUG = False

BASE_DIR_PATH = "/home/ubuntu/SetracoRecrutement"
BASE_DIR = Path(BASE_DIR_PATH)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DB_PATH = "/home/ubuntu/db.sqlite3"
MEDIA_URL = '/media/'
MEDIA_ROOT = "/home/ubuntu/media"

LOGS_DIR = "/home/ubuntu/logs"

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [
    'https://cvtheque.devexperimentation.fr',
    'https://www.cvtheque.devexperimentation.fr'
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'config',
    'profiles',
    'accounts',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SetracoRecrutement.urls'

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

WSGI_APPLICATION = 'SetracoRecrutement.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_PATH,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# STATIC_ROOT = BASE_DIR / 'static' if DEBUG else os.getenv('STATIC_PATH')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'  # Redirect to login if not authenticated
LOGIN_REDIRECT_URL = '/profiles'  # Redirect after login
LOGOUT_REDIRECT_URL = 'login'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'access': {
            'format': '{asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'config': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'config.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'profiles': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'profiles.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        # 'profiles_ajax': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'filename': os.path.join(LOGS_DIR, 'profiles_ajax.log'),
        #     'when': 'D',
        #     'interval': 1,
        #     'backupCount': 7,
        #     'formatter': 'verbose',
        # },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'django.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'errors.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'access_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'access.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'access',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],
            'level': 'ERROR',
            'propagate': False,  # Disable propagation to prevent logs from leaking to root logger
        },
        'django.server': {
            'level': 'WARNING'
        },
        'django.utils.autoreload': {
            'level': 'CRITICAL'
        },
        'access': {
            'handlers': ['access_file'],
            'level': 'INFO',
            'propagate': False,  # Ensure it only logs in 'access.log'
        },
        'django.db.backends': {
            'handlers': ['file'],  # Sends SQL logs only to django.log
            'level': 'WARNING',  # Set to WARNING to disable detailed SQL debug logs
            'propagate': False,
        },
        'profiles': {
            'handlers': ['profiles'],
            'level': 'INFO',
            'propagate': True,  # Ensure it only logs in 'access.log'
        },
        # 'profiles_ajax': {
        #     'handlers': ['profiles_ajax'],
        #     'level': 'DEBUG',
        #     'propagate': True,  # Ensure it only logs in 'access.log'
        # },
        'config': {
            'handlers': ['config'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
