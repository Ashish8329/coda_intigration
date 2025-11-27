import os
import requests

CODA_BASE_URL = os.getenv("CODA_BASE_URL")
CODA_API_TOKEN = os.getenv("CODA_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {CODA_API_TOKEN}",
}

class CodaClient:
    """
    coda client for handling simple api and getting data with the apis
    """
    def list_docs(self):
        url = f"{CODA_BASE_URL}/docs"
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return r.json()

    def list_tables(self, doc_id):
        url = f"{CODA_BASE_URL}/docs/{doc_id}/tables"
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return r.json()

    def list_rows(self, doc_id, table_id):
        url = f"{CODA_BASE_URL}/docs/{doc_id}/tables/{table_id}/rows"
        r = requests.get(url, headers=HEADERS)
        r.raise_for_status()
        return r.json()

    def export_page_html(self, doc_id, page_id):
        url = f"{CODA_BASE_URL}/docs/{doc_id}/pages/{page_id}/export"
        r = requests.get(url, headers=HEADERS, params={"format": "html"})
        r.raise_for_status()
        return r.text

    def delete_page(self, doc_id: str, page_id: str):
        """
        Deletes a page inside a Coda document.
        """
        endpoint = f"/docs/{doc_id}/pages/{page_id}"
        return self._request("DELETE", endpoint)
