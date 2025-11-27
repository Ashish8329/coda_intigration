import logging
from scanner.services.document_sync import DocumentSyncService
from scanner.detectors.stale_doc_detector import StaleDocumentDetector
from scanner.detectors.public_doc_detector import PublicDocumentDetector
from scanner.detectors.sensitive_data_detector import SensitiveDataDetector

logger = logging.getLogger("scanner")


class ScanRunner:
    """
    Orchestrates the full scanning workflow:
    1. Sync documents from Coda
    2. Run stale document detector
    3. Run public document detector
    4. Run sensitive-data detectors on tables and pages
    """

    def __init__(self):
        """
        Initialize services and detectors.
        """
        self.doc_service = DocumentSyncService()
        self.detectors = [
            StaleDocumentDetector(threshold_days=90),
            PublicDocumentDetector(),
        ]
        self.sensitive_detector = SensitiveDataDetector(client=self.doc_service.client)

    def run_scan(self):
        """
        Execute the full scanning process:
        - Sync documents from Coda
        - Run all detectors
        - Save alerts to DB
        """
        logger.info("===== Starting full Coda scan =====")

        # Step 1: Sync documents
        docs = self.doc_service.sync_documents()
        if not docs:
            logger.warning("No documents fetched from Coda. Exiting scan.")
            return

        # Step 2: Run simple detectors
        for detector in self.detectors:
            try:
                detector.run(docs)
            except Exception as e:
                logger.error(f"Error running detector {detector.__class__.__name__}: {e}")

        # Step 3: Run sensitive data detectors
        try:
            self.sensitive_detector.run_row_scan(docs)
        except Exception as e:
            logger.error(f"Error running sensitive row scan: {e}")

        try:
            self.sensitive_detector.run_page_scan(docs)
        except Exception as e:
            logger.error(f"Error running sensitive page scan: {e}")

        logger.info("===== Full Coda scan completed =====")
