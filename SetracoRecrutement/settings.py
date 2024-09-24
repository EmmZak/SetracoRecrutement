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
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+v3ue5j1_eys8t)3da+g7p8)#yppd!8llm-*y@$^tjd0i+bs)p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

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
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT = STATIC_URL


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'  # Redirect to login if not authenticated
LOGIN_REDIRECT_URL = 'home'  # Redirect after login
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
            'filename': os.path.join(BASE_DIR, 'logs', 'config.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'profiles': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'profiles.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        # 'profiles_ajax': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.TimedRotatingFileHandler',
        #     'filename': os.path.join(BASE_DIR, 'logs', 'profiles_ajax.log'),
        #     'when': 'D',
        #     'interval': 1,
        #     'backupCount': 7,
        #     'formatter': 'verbose',
        # },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'access_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'access.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'formatter': 'access',
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['file', 'error_file'],
        #     'level': 'DEBUG',
        #     'propagate': False,  # Disable propagation to prevent logs from leaking to root logger
        # },
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
