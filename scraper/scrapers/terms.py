"""Scraper for all available terms and departments"""

import sys
import re
from datetime import datetime

from bs4 import BeautifulSoup

from scraper.utils import BaseURL
from scraper.base import BaseScraper

starting_path = "index_curr.htm"
daterange_re = r"^\s*[0-9]{2}/[0-9]{2}/[0-9]{4}\s+to\s+[0-9]{2}/[0-9]{2}/[0-9]{4}\s*$"


class TermDetails:
    """Details for a term"""

    def __init__(self, id: str, path: str, start_ts: int, end_ts: int) -> None:
        self.id = id
        self.path = path
        self.start_ts = start_ts
        self.end_ts = end_ts
        self.season, self.year = daterange_to_season_year(start_ts, end_ts)

    def __repr__(self) -> str:
        return (
            f"TermDetails({self.id}, {self.path}, {self.start_ts}, "
            + f"{self.end_ts})  # {self.season} {self.year}"
        )

    def to_dict(self) -> dict[str, str]:
        """Convert the term details to a dictionary"""
        return {
            "id": self.id,
            "path": self.path,
            "start_ts": str(self.start_ts),
            "end_ts": str(self.end_ts),
            "season": self.season,
            "year": str(self.year),
        }


class TermsScraper(BaseScraper):
    """Term scraper class"""

    name = "TermsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self) -> None:
        """
        Fetch and cache all available terms

        Finds the first term's page and then iterates through all terms
        to get their details (utilizing built-in caching)

        Returns:
            list[TermDetails]: A list of term details
        """
        terms: list[TermDetails] = []
        path = starting_path
        tmp_soup = self.soup(path)
        tmp_path = get_prev_path(tmp_soup)
        last_path = tmp_path

        while tmp_path is not None:
            tmp_soup = self.soup(tmp_path)
            last_path = tmp_path
            tmp_path = get_prev_path(tmp_soup)

        tmp_path = last_path

        while tmp_path is not None:
            tmp_soup = self.soup(tmp_path)
            details = assemble_term_details(tmp_soup, tmp_path)
            if details is not None:
                terms.append(details)
            else:
                self.warn(f"Failed to assemble term details for {tmp_path}")
            tmp_path = get_next_path(tmp_soup)

        return terms

    def get(self) -> list[TermDetails]:
        """
        Get a list of all available terms

        Finds the first term's page and then iterates through all terms
        to get their details (utilizing built-in caching)

        Returns:
            list[TermDetails]: A list of term details
        """
        terms: list[TermDetails] = []
        path = starting_path
        tmp_soup = self.soup(path)
        tmp_path = get_prev_path(tmp_soup)
        last_path = tmp_path

        while tmp_path is not None:
            tmp_soup = self.soup(tmp_path)
            last_path = tmp_path
            tmp_path = get_prev_path(tmp_soup)

        tmp_path = last_path

        while tmp_path is not None:
            tmp_soup = self.soup(tmp_path)
            details = assemble_term_details(tmp_soup, tmp_path)
            if details is not None:
                terms.append(details)
            else:
                self.warn(f"Failed to assemble term details for {tmp_path}")
            tmp_path = get_next_path(tmp_soup)

        return terms


def get_prev_path(soup: BeautifulSoup) -> str | None:
    """Get the previous term path"""
    span = soup.select_one("#masthead1 span[title='Previous Term']")
    if span is None:
        return None
    a = span.parent
    if a is None:
        return None
    return a.attrs.get("href", None)

def get_next_path(soup: BeautifulSoup) -> str | None:
    """Get the next term path"""
    span = soup.select_one("#masthead1 span[title='Next Term']")
    if span is None:
        return None
    a = span.parent
    if a is None:
        return None
    return a.attrs.get("href", None)

def get_id(soup: BeautifulSoup) -> str | None:
    """Get the term id"""
    spans = soup.select("#descriptor span.term")
    span = spans[0] if spans else None
    if span is None:
        return None
    return span.text.strip()

def get_daterange(soup: BeautifulSoup) -> tuple[int, int] | None:
    """Get the term daterange"""
    table = soup.select_one("#index")
    if table is None:
        return None
    th = table.find_next(string=re.compile(daterange_re))
    if th is None:
        return None
    text = th.text.strip()  # e.g., "01/08/2024 to 03/15/2024"
    start, end = text.split("to")
    start = datetime.strptime(start.strip(), "%m/%d/%Y").timestamp()
    end = datetime.strptime(end.strip(), "%m/%d/%Y").timestamp()
    return round(start), round(end)

def assemble_term_details(soup: BeautifulSoup, path: str) -> TermDetails | None:
    """Get the term details"""
    id = get_id(soup)
    daterange = get_daterange(soup)
    if id is None or daterange is None:
        return None
    return TermDetails(id, path, *daterange)

def daterange_to_season_year(start_ts: int, end_ts: int) -> tuple[str, int]:
    """Get the season for the daterange"""
    avg_ts = (start_ts + end_ts) / 2
    avg = datetime.fromtimestamp(avg_ts)
    month = avg.month
    if month >= 1 and month <= 3:
        season = "Winter"
    elif month >= 4 and month <= 6:
        season = "Spring"
    elif month >= 7 and month <= 9:
        season = "Summer"
    else:
        season = "Fall"
    return season, avg.year

def main() -> None:
    ts = TermsScraper()
    terms = ts.get()

    for term in terms:
        print(term)

if __name__ == "__main__":
    main()
