"""Base class for all scrapers"""

import sys
import time
from typing import Callable, Optional

import requests
from bs4 import BeautifulSoup

from database.setup import DB
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
            response = requests.get(self.base_url.value + path, timeout=10)
            response.raise_for_status()
            content = response.text
            self.cache[path] = content
        return BeautifulSoup(content, "html.parser")

    def warn(self, message: str) -> None:
        """Print a warning message to stderr"""
        print(f"Warning ({self.name}): {message}", file=sys.stderr)


class ID:
    """
    Placeholder for an ID that require opening a new path

    Provides a callback to get the actual ID (BeautifulSoup -> str)
    """

    def __init__(
        self, path: str, term_id: str, callback: Callable[[BeautifulSoup], str]
    ) -> None:
        """
        Initialize the placeholder

        Args:
            - path (str): The path to open
            - term_id (str): The term ID to use
            - callback (Callable[[BeautifulSoup], str]): The callback to use
        """
        self.path = path
        self.term_id = term_id
        self.callback = callback

    def __call__(self, soup: BeautifulSoup) -> str:
        """
        Call the callback with the provided soup

        Args:
            - soup (BeautifulSoup): The soup to use

        Returns:
            - str: The actual ID
        """
        return f"{self.term_id}-{self.callback(soup)}"

    def __str__(self) -> str:
        return f"ID<{self.path}>"


class IDs:
    """
    Placeholder for IDs that require opening a new path

    Provides a callback to get the actual IDs (BeautifulSoup, str -> list[ID])
    """

    def __init__(
        self,
        path: str,
        term_id: str,
        callback: Callable[[BeautifulSoup, str], list[ID]],
    ) -> None:
        """
        Initialize the placeholder

        Args:
            - path (str): The path to open
            - term_id (str): The term ID to use
            - callback (Callable[[BeautifulSoup, str], list[ID]]): The callback to use
        """
        self.path = path
        self.term_id = term_id
        self.callback = callback

    def __call__(self, soup: BeautifulSoup) -> list[ID]:
        """
        Call the callback with the provided soup

        Args:
            - soup (BeautifulSoup): The soup to use

        Returns:
            - list[ID]: The IDs
        """
        return self.callback(soup, self.term_id)

    def __str__(self) -> str:
        return f"IDs<{self.path}>"
