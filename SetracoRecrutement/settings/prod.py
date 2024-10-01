from .base import *


BASE_DIR = "C:\""

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
ALLOWED_HOSTS = ["localhost", '127.0.0.1']

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True