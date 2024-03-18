"""Scraper for available colleges"""

import re

from scraper.scrapers.instructors import InstructorsScraper
from scraper.scrapers.subjects import SubjectsScraper
from scraper.utils import BaseURL
from scraper.base import BaseScraper

college_f_subj_re = r"^Subjects\s+(.*)$"


class CollegesScraper(BaseScraper):
    """College scraper class"""

    name = "CollegesScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self, term_id: str, path: str) -> None:
        """Fetch all colleges for a given term"""
        soup = self.soup(path)
        college_links = soup.select("#index a[href*='depts_']")
        assert len(college_links) > 0, f"Failed to find college links in {path}"
        subject_links = soup.select("#index a[href*='all_subject_']")
        assert len(subject_links) > 0, f"Failed to find subject links in {path}"
        instructor_links = soup.select("#index a[href*='all_person_']")
        assert len(instructor_links) > 0, f"Failed to find instructor links in {path}"
        assert (
            len(subject_links) == len(instructor_links) == len(college_links)
        ), f"College, subject and instructor link counts do not match in {path}"

        for college_link, subject_link, instructor_link in zip(
            college_links, subject_links, instructor_links
        ):
            college_name = college_link.get_text(strip=True)
            subject_text = subject_link.get_text(strip=True)
            match = re.match(college_f_subj_re, subject_text)
            assert match, f"Failed to find the college code in {subject_text}"
            college_code = match.group(1)
            subject_path = subject_link["href"]
            assert isinstance(
                subject_path, str
            ), f"Failed to find subject path in {path}"
            instructor_path = instructor_link["href"]
            assert isinstance(
                instructor_path, str
            ), f"Failed to find instructor path in {path}"

            college = {
                "_id": f"{term_id}-{college_code}",
                "term_id": term_id,
                "code": college_code,
                "name": college_name,
                "url": self.base_url.value + subject_path,
            }
            self.db.add_college(college)
            # Fetch dependent data
            SubjectsScraper(self.db, self.cache).fetch(
                term_id, college["_id"], subject_path
            )
            InstructorsScraper(self.db, self.cache).fetch(
                term_id, college["_id"], instructor_path
            )
