"""Scrape Schedules Website"""

import argparse

from database.contexts.database import DB
from scraper.scrapers.terms import TermsScraper


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Schedules Website")
    parser.add_argument(
        "-t",
        "--term-history",
        type=int,
        default=0,
        help="Number of terms to go back (default: 0)",
    )
    args = parser.parse_args()

    th = args.term_history
    if th < 0:
        raise ValueError("Term history must be non-negative")

    db = DB()
    db.reset()
    scraper = TermsScraper(db)
    scraper.fetch("index_curr.htm", th)
