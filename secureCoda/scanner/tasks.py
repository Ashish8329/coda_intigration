import logging

from celery import shared_task
from celery.schedules import crontab

from scanner.services.scan_runner import ScanRunner

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
