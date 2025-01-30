import re
from typing import List, Dict, Tuple

def is_company_affiliated(affiliation: str) -> bool:
    """Identifies if an affiliation is a pharmaceutical or biotech company."""
    company_keywords = ["Inc", "LLC", "Pharma", "Biotech", "Corporation"]
    return any(keyword in affiliation for keyword in company_keywords)

def extract_author_info(article_data: Dict) -> Tuple[List[str], List[str], str]:
    """Extracts non-academic authors, affiliations, and corresponding author email."""
    non_academic_authors = []
    company_affiliations = []
    corresponding_email = None

    authors = article_data.get("authors", [])
    for author in authors:
        name = author.get("name")
        affiliation = author.get("affiliation", "")
        email = author.get("email")

        if affiliation and is_company_affiliated(affiliation):
            non_academic_authors.append(name)
            company_affiliations.append(affiliation)

        if email and not corresponding_email:
            corresponding_email = email

    return non_academic_authors, company_affiliations, corresponding_email
