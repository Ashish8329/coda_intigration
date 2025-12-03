import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secureCoda.settings")

app = Celery("secureCoda")

# Read config from Django settings, using CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# crone job for sync of new data from coda platform
app.conf.beat_schedule = {
    "run-coda-scan-every-hour": {
        "task": "scanner.tasks.run_full_scan",
        "schedule": crontab(minute=0, hour="*"),  # every hour
    },
}
