"""Utilities used by the scrapers"""

from enum import Enum, IntEnum
from typing import Optional

class BaseURL(Enum):
    """Base URLs for the scrapers"""
    SCHEDULES = "https://schedules.calpoly.edu/"
    REQUIREMENTS = "REQUIREMENTS_URL"  # TODO: Add the URL
