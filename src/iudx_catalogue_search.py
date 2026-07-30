"""Discover Bengaluru transport resources published through IUDX."""

import json
from pathlib import Path


CATALOGUE_URL = "https://api.catalogue.iudx.org.in/iudx/cat/v1"
SEARCH_TERMS = ("BMTC", "Bengaluru traffic", "Bengaluru vehicle GPS", "Bengaluru NO2")
OUTPUT_PATH = Path("outputs/iudx_catalogue_search.json")


def discover_resources():
    try:
        from iudx.cat.Catalogue import Catalogue
        from iudx.cat.CatalogueQuery import CatalogueQuery
    except ImportError as error:
        raise RuntimeError(
            "Install the IUDX SDK first: "
            "pip install git+https://github.com/datakaveri/iudx-python-sdk"
        ) from error

    catalogue = Catalogue(
        cat_url=CATALOGUE_URL,
        headers={"content-type": "application/json"},
    )
    query_builder = CatalogueQuery()
    searches = []

    for term in SEARCH_TERMS:
        result = catalogue.search_entity(query_builder.text_search(term))
        searches.append(
            {
                "search_term": term,
                "status": result.status,
                "total_hits": result.total_hits,
                "documents": result.documents,
            }
        )
        print(f"{term}: {result.total_hits} result(s), status {result.status}")

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(searches, indent=2), encoding="utf-8")
    print(f"Saved: {OUTPUT_PATH}")
    return searches


if __name__ == "__main__":
    discover_resources()
