from celery import shared_task
from scanner.services.scan_runner import ScanRunner
import logging

from celery.schedules import crontab

logger = logging.getLogger("scanner")


@shared_task
def run_full_scan():
    """
    Runs the full Coda scan as a Celery task.
    """
    logger.info("Running full scan via Celery task")
    scan = ScanRunner()
    scan.run_scan()
    logger.info("Celery scan task completed")



app.conf.beat_schedule = {
    "run-coda-scan-every-hour": {
        "task": "scanner.tasks.run_full_scan",
        "schedule": crontab(minute=0, hour="*"),  # every hour
    },
}
