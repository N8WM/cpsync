"""Scraper for available subjects"""

from scraper.scrapers.courses import CoursesScraper
from scraper.utils import BaseURL
from scraper.base import BaseScraper


class SubjectsScraper(BaseScraper):
    """Subject scraper class"""

    name = "SubjectsScraper"
    base_url = BaseURL.SCHEDULES

    def fetch(self, term_id: str, college_id: str, path: str) -> None:
        """Fetch all subjects for a given college"""
        soup = self.soup(path)
        subject_links = soup.select("#listing a[href*='subject_']")
        assert len(subject_links) > 0, f"Failed to find subject links in {path}"
        course_links = soup.select("#listing a[href*='courses_']")
        assert len(course_links) > 0, f"Failed to find course links in {path}"
        catalog_links = soup.select("#listing a[href*='catalog.calpoly.edu']")
        catalogs = {
            link.get_text(strip=True).split(" ")[1]: link for link in catalog_links
        }
        assert len(subject_links) == len(
            course_links
        ), f"Subject and course link counts do not match in {path}"

        for subject_link, course_link in zip(subject_links, course_links):
            catalog_link = catalogs.get(subject_link.get_text(strip=True), None)
            subject_code = subject_link.get_text(strip=True)
            section_path = subject_link["href"]
            assert isinstance(
                section_path, str
            ), f"Failed to find section path in {path}"
            subject_name = course_link.get_text(strip=True)
            course_path = course_link["href"]
            assert isinstance(course_path, str), f"Failed to find course path in {path}"
            catalog_url = catalog_link["href"] if catalog_link else None

            subject = {
                "_id": f"{term_id}-{subject_code}",
                "term_id": term_id,
                "college_id": college_id,
                "code": subject_code,
                "name": subject_name,
                "catalog_url": catalog_url,
                "url": self.base_url.value + course_path,
            }
            self.db.add_subject(subject)

            # Fetch dependent data
            CoursesScraper(self.db, self.cache).fetch(
                term_id, college_id, subject["_id"], course_path
            )
