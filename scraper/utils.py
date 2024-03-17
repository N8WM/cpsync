"""Utilities used by the scrapers"""

from enum import Enum


class BaseURL(Enum):
    """Base URLs for the scrapers"""

    SCHEDULES = "https://schedules.calpoly.edu/"
    # Add more base URLs here
