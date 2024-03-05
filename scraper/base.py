"""Base class for all scrapers"""
import sys
import time

import requests
from bs4 import BeautifulSoup

from database.setup import DB
from scraper.utils import BaseURL


class BaseScraper:
    """Base scraper class"""

    name = "BaseScraper"
    base_url: BaseURL

    def __init__(self, db: DB, cache: dict[str, str] | None = None) -> None:
        self.db = db
        self.cache: dict[str, str] = {}  # Content cache {path: text-content}

    def soup(self, path: str, sleep: float = 0.3) -> BeautifulSoup:
        """
        Fetch and cache the raw text on the specified page \\
        `HTTPError` is raised if one occurred
        """
        time.sleep(sleep)
        content = self.cache.get(path, None)
        if content is None:
            response = requests.get(self.base_url.value + path)
            response.raise_for_status()
            content = response.text
            self.cache[path] = content
        return BeautifulSoup(content, "html.parser")

    def warn(self, message: str) -> None:
        """Print a warning message to stderr"""
        print(f"Warning ({self.name}): {message}", file=sys.stderr)
