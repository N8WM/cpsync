"""Scraper for all available terms and departments"""

import sys
import re
from datetime import datetime

from bs4 import BeautifulSoup

from scraper.utils import BaseURL
from scraper.base import BaseScraper, ID, IDs

starting_path = "index_curr.htm"
daterange_re = r"^\s*[0-9]{2}/[0-9]{2}/[0-9]{4}\s+to\s+[0-9]{2}/[0-9]{2}/[0-9]{4}\s*$"


class TermsScraper(BaseScraper):
    """Term scraper class"""

    name = "TermsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self) -> None:
        """
        Fetch all available terms

        Finds the first term's page and then iterates through all terms
        to get their details
        """
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
                self.db.add_term(details)
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
    start = datetime.strptime(start.strip(), "%m/%d/%Y").timestamp()
    end = datetime.strptime(end.strip(), "%m/%d/%Y").timestamp()
    return round(start), round(end)


def get_buildings(soup: BeautifulSoup, term_id: str) -> IDs:
    """Get the buildings for the term"""
    table = soup.select_one("#index")
    assert table is not None, "Unable to find the index table"
    # href contains "all_location_..."
    loc_link = table.select_one("a[href*='all_location_']")
    assert loc_link is not None, "Unable to find the location link"
    href = loc_link["href"]
    assert isinstance(href, str), f"Expected str, got {type(href)}"
    return IDs(href, term_id, get_building_ids)


def get_building_ids(soup: BeautifulSoup, term_id: str) -> list[ID]:
    """Get the building ids"""
    buildings: list[ID] = []
    table = soup.select_one("#listing")
    assert table is not None, "Unable to find the listing table"
    loc_tds = table.select("tr > td.location:nth-of-type(1)")
    assert len(loc_tds) > 0, "Unable to find the location links"
    loc_links = [td.select_one("a[href]") for td in loc_tds]
    for a in loc_links:
        assert a is not None, "Unable to find the location link"
        href = a["href"]
        assert isinstance(href, str), f"Expected str, got {type(href)}"
        buildings.append(ID(href, term_id, get_building_id))
    return buildings


def get_building_id(soup: BeautifulSoup) -> str:
    """Get the building id"""
    span = soup.select_one("#descriptor span.alias")
    assert span is not None, "Unable to find building id"
    return span.text.strip()


def get_colleges(soup: BeautifulSoup, term_id: str) -> list[ID]:
    """Get the colleges for the term"""
    colleges: list[ID] = []
    dep_links = soup.select("a[href]")
    for a in dep_links
        href = a["href"]
        assert isinstance(href, str), f"Expected str, got {type(href)}"
        if href.startswith("depts_")
            colleges.append(ID(href, term_id, get_college_id))
    return colleges


def get_college_id(soup: BeautifulSoup) -> str:
    """Get the college id"""
    span = soup.select_one("#descriptor span.alias")
    assert span is not None, "Unable to find college id"
    return span.text.strip()


def assemble_term_details(soup: BeautifulSoup, path: str):
    """Assemble term data into a dict"""
    id = get_id(soup)
    daterange = get_daterange(soup)
    if id is None or daterange is None:
        return None
    season, year = daterange_to_season_year(daterange[0], daterange[1])
    buildings = get_buildings(soup)
    colleges = get_colleges(soup)
    return {
        "id": id,
        "start": daterange[0],
        "end": daterange[1],
        "season": season,
        "year": year,
        "buildings": [],
        "colleges": colleges,
        "path": path,
    }


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
