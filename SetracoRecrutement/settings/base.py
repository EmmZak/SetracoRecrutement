from pathlib import Path
import os

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", None)
if SECRET_KEY is None:
    print("SECRET_KEY is not found in env vars")
    exit()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = False

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

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'  # Redirect to login if not authenticated
LOGIN_REDIRECT_URL = 'home'  # Redirect after login
LOGOUT_REDIRECT_URL = 'login'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
"""
For local and qa DB is in the root
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

"""
For local and qa media files are in the root
"""
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGS_DIR = 'logs/'
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
        'config': {
            'handlers': ['config'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
