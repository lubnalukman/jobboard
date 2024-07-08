

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobproject.settings')

# Create a Celery instance and configure it using the settings from Django
celery = Celery('jobproject')

# Load task modules from all registered Django app configs
celery.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
celery.autodiscover_tasks()