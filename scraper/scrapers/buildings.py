"""Scraper for available buildings"""

import re

from scraper.utils import BaseURL
from scraper.base import BaseScraper

building_re = r"^([A-Za-z0-9]+)\s+(.+)$"


class BuildingsScraper(BaseScraper):
    """Building scraper class"""

    name = "BuildingsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self, term_id: str, path: str) -> None:
        """Fetch all buildings for a given term"""
        soup = self.soup(path)
        buildings = soup.find_all(class_="locationDivDescr")
        building_num_names = [bldg_num_name(b.text) for b in buildings]
        for num, name in building_num_names:
            tmp_building = {
                "_id": f"{term_id}-{num}",
                "term_id": term_id,
                "number": num,
                "name": name,
                "url": self.base_url.value + path + f"#{num}",
            }
            self.db.add_building(tmp_building)


def bldg_num_name(label: str) -> tuple[str, str]:
    """Extract building number and name"""
    match = re.match(building_re, label)
    if match is None:
        return label, "Unlabeled Building"
    return match.group(1), match.group(2)
