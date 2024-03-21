"""Base class for all scrapers"""

import sys
import time
from typing import Callable

import requests
from bs4 import BeautifulSoup

from database.contexts.database import DB
from scraper.utils import BaseURL


class BaseScraper:
    """Base scraper class"""

    name = "BaseScraper"
    base_url: BaseURL

    def __init__(self, db: DB, cache: dict[str, str] | None = None) -> None:
        """
        Initialize the scraper

        Args:
            - db (DB): The database instance
            - cache (dict[str, str] | None): The cache to use (if not provided, a new one is created)
        """
        self.db = db
        self.cache: dict[str, str] = cache or {}  # Content cache {path: text-content}

    def soup(self, path: str, sleep: float = 0.3) -> BeautifulSoup:
        """
        Fetch and cache the raw text on the specified page \\
        `HTTPError` is raised if one occurred

        Args:
            - path (str): The path to the page
            - sleep (float): The time to sleep before fetching the page

        Returns:
            - BeautifulSoup: The parsed page
        """
        content = self.cache.get(path, None)
        if content is None:
            time.sleep(sleep)
            print(f"Fetching .../{path}")
            response = requests.get(self.base_url.value + path, timeout=10)
            response.raise_for_status()
            content = response.text
            self.cache[path] = content
        return BeautifulSoup(content, "html.parser")

    def warn(self, message: str) -> None:
        """Print a warning message to stderr"""
        print(f"Warning ({self.name}): {message}", file=sys.stderr)
