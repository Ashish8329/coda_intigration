import logging
import re
from scanner.models import Alert

logger = logging.getLogger("scanner")


class SensitiveDataDetector:
    """
    Detects sensitive information in table rows and page content.
    """

    # Add more patterns as needed TODO use Json for production
    SENSITIVE_PATTERNS = {
        "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
        "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "EMAIL": re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
        "PASSWORD_FIELD": re.compile(r"password|passwd|secret|api_key", re.IGNORECASE),
    }

    def __init__(self, client):
        """
        :param client: Instance of CodaClient
        """
        self.client = client

    def run_row_scan(self, documents):
        """
        Scan all tables and rows in each document for sensitive data.
        """
        logger.info("Starting row scan for sensitive data...")

        for doc in documents:
            try:
                tables_data = self.client.list_tables(doc.doc_id).get("items", [])
            except Exception as e:
                logger.warning(f"Failed to fetch tables for doc {doc.doc_id}: {e}")
                continue

            for table_item in tables_data:
                table_id = table_item.get("id")
                table_name = table_item.get("name", "Unnamed Table")

                try:
                    rows_data = self.client.list_rows(doc.doc_id, table_id).get("items", [])
                except Exception as e:
                    logger.warning(f"Failed to fetch rows for table {table_id}: {e}")
                    continue

                for row in rows_data:
                    row_values = row.get("values", {})
                    for field, value in row_values.items():
                        if not isinstance(value, str):
                            continue
                        for rule, pattern in self.SENSITIVE_PATTERNS.items():
                            if pattern.search(value):
                                Alert.objects.create(
                                    document=doc,
                                    rule=f"SENSITIVE_DATA_{rule}",
                                    severity="high",
                                    description=f"Sensitive data found in table '{table_name}', field '{field}'",
                                )
                                logger.info(f"Sensitive alert: {doc.name} - {table_name} - {field}")


    def run_page_scan(self, documents):
        """
        Export page content as HTML, strip HTML tags, and scan for sensitive patterns.
        """
        import html

        logger.info("Starting page scan for sensitive content...")

        for doc in documents:
            try:
                pages = getattr(doc, "pages", [])  # if you implement pages in DB
                # Or use CodaClient API to list pages (not yet stored)
                for page in pages:
                    page_id = page.get("id")
                    page_name = page.get("name", "Unnamed Page")

                    try:
                        html_content = self.client.export_page_html(doc.doc_id, page_id)
                        text_content = html.unescape(re.sub(r"<[^>]+>", "", html_content))
                    except Exception as e:
                        logger.warning(f"Failed to export page {page_id}: {e}")
                        continue

                    for rule, pattern in self.SENSITIVE_PATTERNS.items():
                        if pattern.search(text_content):
                            Alert.objects.create(
                                document=doc,
                                rule=f"SENSITIVE_PAGE_{rule}",
                                severity="high",
                                description=f"Sensitive data found on page '{page_name}'",
                            )
                            logger.info(f"Sensitive page alert: {doc.name} - {page_name}")

            except Exception as e:
                logger.warning(f"Page scan failed for doc {doc.doc_id}: {e}")
