import logging
from scanner.services.document_sync import DocumentSyncService
from scanner.detectors.stale_doc_detector import StaleDocumentDetector
from scanner.detectors.public_doc_detector import PublicDocumentDetector

logger = logging.getLogger("scanner")


class ScanRunner:
    """
    Orchestrates the full scanning flow:
    1. Sync documents
    2. Run detectors
    """

    def __init__(self):
        self.doc_service = DocumentSyncService()
        self.detectors = [
            StaleDocumentDetector(threshold_days=90),
            PublicDocumentDetector(),
        ]

    def run_scan(self):
        """
        Main entry point to run all scanning tasks.
        """
        logger.info("Starting full scan...")

        docs = self.doc_service.sync_documents()

        for detector in self.detectors:
            detector.run(docs)

        logger.info("Full scan completed.")
