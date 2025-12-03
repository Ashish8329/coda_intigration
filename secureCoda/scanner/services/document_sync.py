import logging
from dateutil.parser import parse as parse_datetime
from django.utils import timezone
from scanner.coda_client import CodaClient
from scanner.models import Document

logger = logging.getLogger("scanner")

class DocumentSyncService:
    """
    Handles fetching documents from Coda API and updating the local DB.
    """

    def __init__(self):
        self.client = CodaClient()

    def sync_documents(self):
        """
        Fetches all Coda documents and updates DB records.
        Converts API timestamps to datetime objects.
        Returns a list of Document instances.
        """
        logger.info("Starting document sync...")

        try:
            data = self.client.list_docs()
        except Exception as e:
            logger.error(f"Failed to fetch documents from Coda: {e}")
            return []

        docs = data
        synced_docs = []

        for item in docs:
            doc_id = item.get("id")
            name = item.get("name", "Untitled Document")
            created_at_str = item.get("createdAt")
            updated_at_str = item.get("updatedAt")
            is_published = item.get("browserLink") is not None

            # Convert timestamps to datetime objects
            try:
                created_at = parse_datetime(created_at_str) if created_at_str else None
                updated_at = parse_datetime(updated_at_str) if updated_at_str else None
            except Exception as e:
                logger.warning(f"Failed to parse timestamps for doc {doc_id}: {e}")
                created_at = None
                updated_at = None

            # Save/update in DB
            doc, _ = Document.objects.update_or_create(
                doc_id=doc_id,
                defaults={
                    "name": name,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "is_published": is_published,
                    "last_scanned_at": timezone.now(),
                },
            )

            synced_docs.append(doc)

        logger.info(f"Document sync complete — synced {len(synced_docs)} documents")
        return synced_docs