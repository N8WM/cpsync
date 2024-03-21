"""Scraper for available terms"""

import re
from datetime import datetime

from bs4 import BeautifulSoup

from scraper.scrapers.buildings import BuildingsScraper
from scraper.scrapers.colleges import CollegesScraper
from scraper.scrapers.rooms import RoomsScraper
from scraper.utils import BaseURL
from scraper.base import BaseScraper
from database.contexts.database import DB

daterange_re = r"^\s*[0-9]{2}/[0-9]{2}/[0-9]{4}\s+to\s+[0-9]{2}/[0-9]{2}/[0-9]{4}\s*$"


class TermsScraper(BaseScraper):
    """Term scraper class"""

    name = "TermsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self, starting_path: str, hist: int) -> None:
        """
        Fetch all available terms

        Finds the first term's page and then iterates through all terms
        to get their details
        """
        path = starting_path
        tmp_soup = self.soup(path)
        tmp_path = get_prev_path(tmp_soup)
        last_path = path

        while tmp_path is not None and hist > 0:
            # Traverse to the first term
            tmp_soup = self.soup(tmp_path)
            last_path = tmp_path
            tmp_path = get_prev_path(tmp_soup)
            hist -= 1

        tmp_path = last_path

        while tmp_path is not None:
            # Traverse through all populated terms starting from the first term
            tmp_soup = self.soup(tmp_path)
            tmp_location_link = get_location_link(tmp_soup)
            if tmp_location_link is None:
                break
            details = assemble_term_details(tmp_soup, self.base_url.value + tmp_path)
            if details is not None:
                self.db.add_term(details)
                # Fetch dependent data
                BuildingsScraper(self.db, self.cache).fetch(
                    details["_id"], tmp_location_link
                )
                RoomsScraper(self.db, self.cache).fetch(
                    details["_id"], tmp_location_link
                )
                CollegesScraper(self.db, self.cache).fetch(details["_id"], tmp_path)
            else:
                self.warn(f"Failed to assemble term details for {tmp_path}")
            tmp_path = get_next_path(tmp_soup)


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
    assert table is not None, "Unable to find the index table"
    th = table.find_next(string=re.compile(daterange_re))
    assert th is not None, "Unable to find the daterange"
    text = th.text.strip()  # e.g., "01/08/2024 to 03/15/2024"
    start, end = text.split("to")
    start_dt = datetime.strptime(start.strip(), "%m/%d/%Y")
    end_dt = datetime.strptime(end.strip(), "%m/%d/%Y")
    start = int(start_dt.strftime("%Y%m%d"))
    end = int(end_dt.strftime("%Y%m%d"))
    return start, end


def get_location_link(soup: BeautifulSoup) -> str | None:
    """Get the location link for the term"""
    table = soup.select_one("#index")
    if table is None:
        return None
    loc_link = table.select_one("a[href*='all_location_']")
    if loc_link is None:
        return None
    href = loc_link["href"]
    assert isinstance(href, str), f"Expected str, got {type(href)}"
    return href


def assemble_term_details(soup: BeautifulSoup, url: str):
    """Assemble term data into a dict"""
    id = get_id(soup)
    daterange = get_daterange(soup)
    if id is None or daterange is None:
        return None
    season, year = daterange_to_season_year(daterange[0], daterange[1])
    return {
        "_id": id,
        "start": daterange[0],
        "end": daterange[1],
        "season": season,
        "year": year,
        "url": url,
    }


def daterange_to_season_year(start: int, end: int) -> tuple[str, int]:
    """Get the season for the daterange"""
    start_ts = datetime.strptime(str(start), "%Y%m%d").timestamp()
    end_ts = datetime.strptime(str(end), "%Y%m%d").timestamp()
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


if __name__ == "__main__":
    """Run the scraper"""
    db = DB()
    db.reset()
    scraper = TermsScraper(db)
    scraper.fetch("index_curr.htm", 0)
