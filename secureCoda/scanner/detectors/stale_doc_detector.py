import logging
from datetime import timedelta

from django.utils import timezone

from scanner.models import Alert

logger = logging.getLogger("scanner")


class StaleDocumentDetector:
    """
    Flags documents that haven't been updated for X days.
    """

    def __init__(self, threshold_days):
        self.threshold = timedelta(days=threshold_days)

    def run(self, documents):
        """
        Runs detection logic on a list of Document objects.
        Creates alerts for stale documents.
        """
        logger.info("Running stale document detector...")

        now = timezone.now()

        for doc in documents:
            if not doc.updated_at:
                continue  # skip invalid docs

            if now - doc.updated_at > self.threshold:
                Alert.objects.update_or_create(
                    document=doc,
                    rule="STALE_DOCUMENT",
                    severity="low",
                    description=f"Document '{doc.name}' has not been updated for over {self.threshold.days} days.",
                )
                logger.info(f"Stale alert created for document: {doc.name}")
