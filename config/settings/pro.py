from .base import *

# SECURTY CONFIGURATION

DEBUG = env.bool('DJANGO_DEBUG', False)
ALLOWED_HOSTS = ['.herokuapp.com']

# SSL CONFIGURATION

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# STATIC FILES CONFIGURATION

STATIC_ROOT = str(ROOT_DIR.path('staticfiles'))
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# CELERY CONFIGURATION

BROKER_URL = env('REDIS_URL')
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
