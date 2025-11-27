import logging
from scanner.models import Alert

logger = logging.getLogger("scanner")


class PublicDocumentDetector:
    """
    Flags publicly published/externally shared documents.
    """

    def run(self, documents):
        """
        Detects public documents and generates alerts.
        """
        logger.info("Running public document detector...")

        for doc in documents:
            if doc.is_published:
                Alert.objects.create(
                    document=doc,
                    rule="PUBLIC_DOCUMENT",
                    severity="high",
                    description=f"Document '{doc.name}' is publicly shared.",
                )
                logger.info(f"Public alert created for document: {doc.name}")
