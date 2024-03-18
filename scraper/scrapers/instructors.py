"""Scraper for available instructors"""

import re
from bs4 import Tag

from scraper.utils import BaseURL
from scraper.base import BaseScraper

name_re = r"^(.+),\s+(.+)$"


class InstructorsScraper(BaseScraper):
    """Instructor scraper class"""

    name = "InstructorsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self, term_id: str, college_id: str, path: str) -> None:
        """Fetch all instructors for a given college"""
        soup = self.soup(path)
        table = soup.find("table", id="listing")
        assert isinstance(
            table, Tag
        ), f"Failed to find instructor listing table in {path}"
        trs = table.find_all("tr")
        assert len(trs) > 0, f"Failed to find instructor rows in {path}"
        instr_subj_code = None
        for row in trs:
            assert isinstance(
                row, Tag
            ), f"Unexpected non-tag in instructor listing in {path}"
            cells = row.find_all("td")
            instr_subj_span = row.find("span", class_="subjectDiv")
            if instr_subj_span is not None:
                assert isinstance(
                    instr_subj_span, Tag
                ), f"Unexpected non-tag in instructor subject span in {path}"
                instr_subj_code = instr_subj_span.get_text(strip=True).removesuffix("-")
                continue
            if cells:
                assert (
                    instr_subj_code is not None
                ), f"Failed to find instructor subject code in {path}"
                assert (
                    len(cells) == 6
                ), f"Unexpected number of cells in instructor row in {path}"
                instr_name_cell = cells[0]
                instr_code_cell = cells[1]
                instr_job_title_cell = cells[2]
                instr_office_cell = cells[4]
                assert isinstance(
                    instr_name_cell, Tag
                ), f"Unexpected non-tag in instructor name cell in {path}"
                assert isinstance(
                    instr_code_cell, Tag
                ), f"Unexpected non-tag in instructor code cell in {path}"
                assert isinstance(
                    instr_job_title_cell, Tag
                ), f"Unexpected non-tag in instructor job title cell in {path}"
                assert isinstance(
                    instr_office_cell, Tag
                ), f"Unexpected non-tag in instructor office cell in {path}"
                instr_name_link = instr_name_cell.find("a")
                assert isinstance(
                    instr_name_link, Tag
                ), f"Failed to find instructor name link in {path}"
                instr_href = instr_name_link["href"]
                assert isinstance(
                    instr_href, str
                ), f"Failed to find instructor link href in {path}"
                instr_name = instr_name_link.get_text(strip=True)
                match = re.match(name_re, instr_name)
                assert (
                    match is not None
                ), f"Failed to match instructor name '{instr_name}' in {path}"
                last_name = match.group(1)
                first_middle_name = match.group(2)
                instr_code_link = instr_code_cell.find("a")
                assert isinstance(
                    instr_code_link, Tag
                ), f"Failed to find instructor code link in {path}"
                instr_code = instr_code_link.get_text(strip=True)
                instr_job_title = instr_job_title_cell.get_text(strip=True)
                instr_office = instr_office_cell.get_text(strip=True) or None

                instructor = {
                    "_id": f"{term_id}-{instr_code}",
                    "term_id": term_id,
                    "code": instr_code,
                    "last_name": last_name,
                    "first_middle_name": first_middle_name,
                    "colleges": [college_id],
                    "subjects": [f"{term_id}-{instr_subj_code}"],
                    "job_title": instr_job_title,
                    "office": instr_office,
                    "url": self.base_url.value + instr_href,
                }
                existing_instr = self.db.get_instructor(instructor["_id"])
                if existing_instr is not None:
                    if instructor["colleges"][0] not in existing_instr["colleges"]:
                        existing_instr["colleges"] += instructor["colleges"]
                    if instructor["subjects"][0] not in existing_instr["subjects"]:
                        existing_instr["subjects"] += instructor["subjects"]
                    self.db.update_instructor(existing_instr)
                else:
                    self.db.add_instructor(instructor)
