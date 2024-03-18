"""Scraper for available sections"""

import re
from bs4 import Tag

from scraper.utils import BaseURL
from scraper.base import BaseScraper

instructor_link_re = r"^person_(.+)_.+.htm$"


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
            row_classes = row["class"]
            if "active" not in row_classes:
                continue
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
                "section_ics_download_path_cell": cells[16],
            }
            for key, cell in info.items():
                assert isinstance(
                    cell, Tag
                ), f"Unexpected non-tag in {key.replace('_', ' ')} in {path}"
            section_link = info["section_course_code_cell"].find("a")
            assert isinstance(
                section_link, Tag
            ), f"Failed to find section link in {path}"
            course_code = section_link.get_text(strip=True).replace(" ", "-")
            section_path = section_link["href"]
            assert isinstance(
                section_path, str
            ), f"Failed to find section path in {path}"
            section_number = info["section_number_cell"].get_text(strip=True)
            section_code = info["section_code_cell"].get_text(strip=True)
            if not section_code.isnumeric():
                continue
            section_type_span = info["section_type_cell"].find("span")
            assert isinstance(
                section_type_span, Tag
            ), f"Failed to find section type span in {path}"
            section_type = section_type_span["title"]
            assert isinstance(
                section_type, str
            ), f"Failed to find section type in {path}"
            section_req_span = info["section_req_cell"].find("span")
            section_req_code = None
            section_req_msg = None
            if section_req_span is not None:
                assert isinstance(
                    section_req_span, Tag
                ), f"Failed to find section req span in {path}"
                section_req_code = section_req_span.get_text(strip=True)
                section_req_msg = section_req_span["title"]
                assert isinstance(
                    section_req_msg, str
                ), f"Failed to find section req msg in {path}"
            section_days_span = info["section_days_cell"].find("span")
            section_days = None
            if section_days_span is not None:
                assert isinstance(
                    section_days_span, Tag
                ), f"Failed to find section days span in {path}"
                section_days = section_days_span.get_text(strip=True)
            section_start_time = (
                info["section_start_time_cell"].get_text(strip=True) or None
            )
            section_end_time = (
                info["section_end_time_cell"].get_text(strip=True) or None
            )
            section_instructor_link = info["section_instructor_cell"].find("a")
            instructor_code = None
            if section_instructor_link is not None:
                assert isinstance(
                    section_instructor_link, Tag
                ), f"Failed to find section instructor link in {path}"
                instructor_href = section_instructor_link["href"]
                assert isinstance(
                    instructor_href, str
                ), f"Failed to find section instructor href in {path}"
                match = instructor_code = re.search(instructor_link_re, instructor_href)
                assert (
                    match is not None
                ), f"Failed to find instructor id for link {instructor_href} in {path}"
                instructor_code = match.group(1)
            section_room_link = info["section_room_cell"].find("a")
            section_room_code = None
            if section_room_link is not None:
                assert isinstance(
                    section_room_link, Tag
                ), f"Failed to find section room link in {path}"
                section_room_code = section_room_link.get_text(strip=True)
            section_enrl_cap = (
                info["section_enrl_cap_cell"].get_text(strip=True) or None
            )
            if section_enrl_cap is not None:
                assert (
                    section_enrl_cap.isdigit()
                ), f"Failed to find numeric section enrollment cap in {path}"
                section_enrl_cap = int(section_enrl_cap)
            section_enrl_tot = (
                info["section_enrl_tot_cell"].get_text(strip=True) or None
            )
            if section_enrl_tot is not None:
                assert (
                    section_enrl_tot.isdigit()
                ), f"Failed to find numeric section enrollment total in {path}"
                section_enrl_tot = int(section_enrl_tot)
            section_wait_tot = (
                info["section_wait_tot_cell"].get_text(strip=True) or None
            )
            if section_wait_tot is not None:
                assert (
                    section_wait_tot.isdigit()
                ), f"Failed to find numeric section waitlist total in {path}"
                section_wait_tot = int(section_wait_tot)
            ics_download_link = info["section_ics_download_path_cell"].find("a")
            ics_download_path = None
            if ics_download_link is not None:
                assert isinstance(
                    ics_download_link, Tag
                ), f"Failed to find section ics download link in {path}"
                ics_download_path = ics_download_link["href"]
                assert isinstance(
                    ics_download_path, str
                ), f"Failed to find section ics download path in {path}"

            section = {
                "_id": f"{term_id}-{section_code}-{section_days or 'NoDays'}-{section_room_code or 'NoLoc'}",
                "term_id": term_id,
                "college_id": college_id,
                "subject_id": subject_id,
                "course_id": course_id,
                "code": section_code,
                "alias": f"{course_code}-{section_number}",
                "number": section_number,
                "type": section_type,
                "requirement_code": section_req_code,
                "requirement_message": section_req_msg,
                "days": section_days,
                "start": section_start_time,
                "end": section_end_time,
                "instructor_id": (
                    f"{term_id}-{instructor_code}" if instructor_code else None
                ),
                "room_id": (
                    f"{term_id}-{section_room_code}" if section_room_code else None
                ),
                "enrollment_capacity": section_enrl_cap,
                "enrolled": section_enrl_tot,
                "waitlisted": section_wait_tot,
                "ics_download_url": (
                    self.base_url.value + ics_download_path
                    if ics_download_path
                    else None
                ),
                "url": self.base_url.value + section_path,
            }
            existing_section = self.db.get_section(section["_id"])
            if existing_section is None:
                self.db.add_section(section)
