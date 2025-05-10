import os

from ._base import *

DEBUG = os.getenv("DEBUG")

# add desired paths and ips for this file
ALLOWED_HOSTS = list(os.getenv("ALLOWED_HOSTS"))
LOCAL_TEST = None

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'ENGINE': "django.db.backends.postgresql",
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

CSRF_TRUSTED_ORIGINS = list(os.getenv("CSRF_TRUSTED_ORIGINS"))

# CELERY_BEAT_SCHEDULE = {
#     'is_expired_crontab': {
#         "task": "hamresan.app.advertisements.tasks.update_advertisement_expiration",
#         "schedule": timedelta(days=1),
#     }
# }
from celery.schedules import crontab

# CELERY_BEAT_SCHEDULE = {
#     'check_expired_ads_every_10_minutes': {
#         'task': 'hamresan.app.advertisements.tasks.check_and_expire_advertisements',
#
#         'schedule': crontab(minute=30, hour=3),
#
#
#     },
# }
