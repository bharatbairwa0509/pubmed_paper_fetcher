import requests
from typing import List, Dict

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_paper_ids(query: str, debug: bool = False) -> List[str]:
    """Fetches paper IDs from PubMed based on a search query."""
    url = f"{BASE_URL}esearch.fcgi?db=pubmed&term={query}&retmode=json"
    
    if debug:
        print(f"[DEBUG] Request URL: {url}")

    response = requests.get(url)
    data = response.json()
    
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(paper_ids: List[str], debug: bool = False) -> Dict:
    """Fetches paper details using the PubMed API."""
    if not paper_ids:
        return {}

    ids = ",".join(paper_ids)
    url = f"{BASE_URL}esummary.fcgi?db=pubmed&id={ids}&retmode=json"

    if debug:
        print(f"[DEBUG] Fetching details from: {url}")

    response = requests.get(url)

    # Print raw response
    if debug:
        print(f"[DEBUG] Response Status Code: {response.status_code}")
        print(f"[DEBUG] Response Headers: {response.headers}")
        print(f"[DEBUG] Raw Response:\n{response.text[:500]}")  # Print first 500 characters

    try:
        json_data = response.json()
        return json_data.get("result", {})
    except requests.exceptions.JSONDecodeError:
        print("[ERROR] JSON Decode Failed. Full Response:")
        print(response.text)  # Print full response for debugging
        raise