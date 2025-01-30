import sys
import requests
import argparse
import csv
from typing import List, Dict
from pubmed_paper_fetcher.fetcher import fetch_paper_ids, fetch_paper_details
from pubmed_paper_fetcher.parser import extract_author_info

def process_papers(query: str, debug: bool = False) -> List[Dict]:
    """Fetch and process papers based on the query."""
    paper_ids = fetch_paper_ids(query, debug)
    if not paper_ids:
        print("[INFO] No papers found for the given query.")
        return []

    papers = fetch_paper_details(paper_ids, debug)
    processed_papers = []

    for paper_id in paper_ids:
        paper_data = papers.get(paper_id, {})

        title = paper_data.get("title", "N/A")
        publication_date = paper_data.get("pubdate", "N/A")
        non_academic_authors, company_affiliations, corresponding_email = extract_author_info(paper_data)

        processed_papers.append({
            "PubmedID": paper_id,
            "Title": title,
            "Publication Date": publication_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_email or "N/A",
        })

    return processed_papers

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers based on query")
    parser.add_argument("query", help="Search query to fetch papers")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-f", "--file", type=str, help="File name to save results")

    args = parser.parse_args()

    # Fetch and process papers
    processed_papers = process_papers(args.query, args.debug)

    if not processed_papers:
        print("[INFO] No papers found or processed.")
        return

    # Determine output destination (CSV or console)
    output_file = open(args.file, mode="w", newline="", encoding="utf-8") if args.file else sys.stdout
    with output_file as file:
        fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if args.file:
            writer.writeheader()

        for paper in processed_papers:
            if args.file:
                writer.writerow(paper)
            else:
                print(paper)

if __name__ == "__main__":
    main()
