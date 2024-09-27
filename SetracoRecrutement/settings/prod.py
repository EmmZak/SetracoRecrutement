from .base import *


BASE_DIR = "C: \"

BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

DEBUG = False
