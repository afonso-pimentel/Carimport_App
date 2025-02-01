from abc import ABC, abstractmethod

class Scraper(ABC):
    """Abstract base class for all scrapers."""

    @abstractmethod
    def fetch_ads(self):
        """Fetch ads from the source and return a list of Ad objects."""
        pass
