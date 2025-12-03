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
    def _paginate(self, url):
        while url:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                yield item 
            
            url = data.get('nextPageLink', None)

    def list_docs(self):
        url = f"{CODA_BASE_URL}/docs"
        return list(self._paginate(url))

    def list_tables(self, doc_id):
        url = f"{CODA_BASE_URL}/docs/{doc_id}/tables"
        return list(self._paginate(url))

    def list_rows(self, doc_id, table_id):
        url = f"{CODA_BASE_URL}/docs/{doc_id}/tables/{table_id}/rows"
        return list(self._paginate(url))       


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
