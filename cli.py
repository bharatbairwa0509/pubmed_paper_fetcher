import sys
import requests
import argparse
import csv
from typing import List, Dict

# Sample function to fetch papers (replace with your actual API call)
def fetch_paper_details(paper_ids: List[str], debug: bool = False) -> List[Dict]:
    # Simulating a PubMed API response (replace with actual API request)
    # Example of response as a list of dictionaries
    response = [
        {"title": "Cancer Research Paper 1", "author": "Dr. John Doe", "pubmed_id": "PMID12345"},
        {"title": "Cancer Research Paper 2", "author": "Dr. Jane Smith", "pubmed_id": "PMID67890"}
    ]
    
    if debug:
        print(f"[DEBUG] API Response: {response}")
    
    return response

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers based on query")
    parser.add_argument('query', help='Search query to fetch papers')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    parser.add_argument('-f', '--file', type=str, help='File name to save results')

    args = parser.parse_args()

    paper_ids = ["PMID12345", "PMID67890"]  # Example paper IDs (replace with actual IDs based on query)
    papers = fetch_paper_details(paper_ids, args.debug)

    if args.debug:
        print(f"[DEBUG] Fetched papers: {papers}")

    # Processing the papers
    with open(args.file, mode='w', newline='', encoding='utf-8') if args.file else sys.stdout as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Aliation(s)", "Corresponding Author Email"])
        if args.file:
            writer.writeheader()  # Write header to the CSV file
        for paper_data in papers:
            if isinstance(paper_data, str):
                print(f"[DEBUG] Unexpected string format: {paper_data}")
                paper_data = {}

            if isinstance(paper_data, dict):
                title = paper_data.get("title", "N/A")
                pubmed_id = paper_data.get("pubmed_id", "N/A")
                # Simulating other fields (modify based on actual data)
                publication_date = "2025-01-01"
                non_academic_authors = "Dr. John Doe"
                company_affiliations = "PharmaCo"
                corresponding_email = "john.doe@example.com"

                # Write the row to the CSV or print to console
                row = {
                    "PubmedID": pubmed_id,
                    "Title": title,
                    "Publication Date": publication_date,
                    "Non-academic Author(s)": non_academic_authors,
                    "Company Aliation(s)": company_affiliations,
                    "Corresponding Author Email": corresponding_email,
                }

                if args.file:
                    writer.writerow(row)
                else:
                    print(row)

if __name__ == "__main__":
    main()
