"""Scraper for available sections"""

from bs4 import Tag

from scraper.utils import BaseURL
from scraper.base import BaseScraper


class SectionsScraper(BaseScraper):
    """Section scraper class"""

    name = "SectionsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(
        self, term_id: str, college_id: str, subject_id: str, course_id: str, path: str
    ) -> None:
        """Fetch all sections for a given course"""
        soup = self.soup(path)
        table = soup.find("table", id="listing")
        assert isinstance(table, Tag), f"Failed to find section listing table in {path}"
        rows = table.find_all("tr")
        assert len(rows) > 0, f"Failed to find section rows in {path}"

        for row in rows[1:]:
            assert isinstance(
                row, Tag
            ), f"Unexpected non-tag in section listing in {path}"
            cells = row.find_all("td")
            assert (
                len(cells) == 17
            ), f"Unexpected number of cells in section row in {path}"
            info: dict[str, Tag] = {
                "section_course_code_cell": cells[0],
                "section_number_cell": cells[1],
                "section_code_cell": cells[2],
                "section_type_cell": cells[3],
                "section_ge_cell": cells[4],
                "section_req_cell": cells[5],
                "section_days_cell": cells[6],
                "section_start_time_cell": cells[7],
                "section_end_time_cell": cells[8],
                "section_instructor_cell": cells[9],
                "section_room_cell": cells[10],
                "section_enrl_cap_cell": cells[12],
                "section_enrl_tot_cell": cells[13],
                "section_wait_tot_cell": cells[14],
            }
            for key, cell in info.items():
                assert isinstance(
                    cell, Tag
                ), f"Unexpected non-tag in {key.replace('_', ' ')} in {path}"
            section_link = info["section_code_cell"].find("a")
            assert isinstance(
                section_link, Tag
            ), f"Failed to find section link in {path}"
            course_name = section_link.get_text(strip=True).replace(" ", "-")
            section_path = section_link["href"]
            assert isinstance(
                section_path, str
            ), f"Failed to find section path in {path}"
