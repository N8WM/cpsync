"""Scraper for available courses"""

from bs4 import Tag

from scraper.utils import BaseURL
from scraper.base import BaseScraper


class CoursesScraper(BaseScraper):
    """Course scraper class"""

    name = "CoursesScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self, term_id: str, college_id: str, subject_id: str, path: str) -> None:
        """Fetch all courses for a given subject"""
        soup = self.soup(path)
        table = soup.find("table", id="listing")
        assert isinstance(table, Tag), f"Failed to find course listing table in {path}"
        rows = table.find_all("tr")
        assert len(rows) > 0, f"Failed to find course rows in {path}"

        for row in rows[1:]:
            assert isinstance(
                row, Tag
            ), f"Unexpected non-tag in course listing in {path}"
            cells = row.find_all("td")
            if len(cells) != 13:
                continue
            course_code_cell = cells[0]
            course_name_cell = cells[1]
            course_type_cell = cells[2]
            course_req_cell = cells[5]
            assert isinstance(
                course_code_cell, Tag
            ), f"Unexpected non-tag in course code cell in {path}"
            assert isinstance(
                course_name_cell, Tag
            ), f"Unexpected non-tag in course name cell in {path}"
            assert isinstance(
                course_type_cell, Tag
            ), f"Unexpected non-tag in course type cell in {path}"
            assert isinstance(
                course_req_cell, Tag
            ), f"Unexpected non-tag in course req cell in {path}"
            course_link = course_code_cell.find("a")
            if course_link is None:
                continue
            assert isinstance(course_link, Tag), f"Failed to find course link in {path}"
            course_path = course_link["href"]
            assert isinstance(course_path, str), f"Failed to find course path in {path}"
            course_code = course_link.get_text(strip=True).replace(" ", "-")
            course_name = course_name_cell.get_text(strip=True)
            course_type_span = course_type_cell.find("span")
            assert isinstance(
                course_type_span, Tag
            ), f"Failed to find course type span in {path}"
            course_type = course_type_span["title"]
            assert isinstance(course_type, str), f"Failed to find course type in {path}"
            course_req_span = course_req_cell.find("span")
            course_req_code = None
            course_req_msg = None
            if course_req_span is not None:
                assert isinstance(
                    course_req_span, Tag
                ), f"Failed to find course req span in {path}"
                course_req_code = course_req_span.get_text(strip=True)
                course_req_msg = course_req_span["title"]
                assert isinstance(
                    course_req_msg, str
                ), f"Failed to find course req msg in {path}"

            course = {
                "_id": f"{term_id}-{course_code}",
                "term_id": term_id,
                "college_id": college_id,
                "subject_id": subject_id,
                "code": course_code,
                "name": course_name,
                "types": [course_type],
                "requirement_codes": [course_req_code],
                "requirement_messages": [course_req_msg],
                "url": self.base_url.value + course_path,
            }
            self.db.add_course(course)
