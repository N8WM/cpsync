"""Scraper for available rooms"""

from bs4 import Tag

from scraper.utils import BaseURL
from scraper.base import BaseScraper


class RoomsScraper(BaseScraper):
    """Room scraper class"""

    name = "RoomsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self, term_id: str, path: str) -> None:
        """Fetch all rooms for a given building"""
        soup = self.soup(path)
        table = soup.find("table", id="listing")
        assert isinstance(table, Tag), f"Failed to find room listing table in {path}"
        trs = table.find_all("tr")
        assert len(trs) > 0, f"Failed to find room rows in {path}"
        bldg_num = None
        for row in trs:
            assert isinstance(row, Tag), f"Unexpected non-tag in room listing in {path}"
            cells = row.find_all("td")
            if row.has_attr("id"):
                bldg_num = row["id"]
            if cells:
                assert bldg_num is not None, f"Failed to find building number in {path}"
                room_num_cell = cells[0]
                assert isinstance(
                    room_num_cell, Tag
                ), f"Unexpected non-tag in room number cell in {path}"
                link = room_num_cell.find("a")
                assert isinstance(
                    link, Tag
                ), f"Failed to find room number link in {path}"
                room_number = link.get_text(strip=True)
                schedule_url = link["href"]
                assert isinstance(
                    schedule_url, str
                ), f"Failed to find room schedule url in {path}"
                loc_cap_cell = cells[2]
                assert isinstance(
                    loc_cap_cell, Tag
                ), f"Unexpected non-tag in location capacity cell in {path}"
                registered_location_capacity = loc_cap_cell.get_text(strip=True)
                # check if numeric, then convert to int
                if registered_location_capacity == "":
                    registered_location_capacity = None
                else:
                    assert (
                        registered_location_capacity.isnumeric()
                    ), f"Location capacity is not numeric in {path}"
                    registered_location_capacity = int(registered_location_capacity)

                room = {
                    "_id": f"{term_id}-{room_number}",
                    "term_id": term_id,
                    "building_id": f"{term_id}-{bldg_num}",
                    "number": room_number,
                    "schedule_url": self.base_url.value + schedule_url,
                    "registered_location_capacity": registered_location_capacity,
                    "url": self.base_url.value + path + f"#{bldg_num}",
                }
                self.db.add_room(room)
