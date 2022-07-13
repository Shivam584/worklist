from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings
from pytz import timezone
from celery import Celery
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worklist.settings')

app = Celery('worklist')

app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.

# celery beat config
app.conf.beat_schedule={

}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
