import requests
import re
from datetime import datetime, date

NEWS_API_URL = r"https://api.hypixel.net/skyblock/news"

class SkyBlockNewsItem:
    """
    Represents a news item in SkyBlock.

    Attributes:
        material (str | None): The material associated with the news item (e.g., 'GOLD_BLOCK').
        link (str): The URL link to the full news article.
        date_str (str): The original date string provided in the API response.
        date (datetime | None): The date of the news item, parsed from date_str.
        title (str): The title of the news item.
    """

    def __init__(self, material: str | None, link: str, date_str: str, title: str) -> None:
        self.material: str | None = material
        self.link: str = link
        self.date_str: str = date_str
        self.date: datetime | None = self._parse_date(date_str)
        self.title: str = title

    def _parse_date(self, date_str: str) -> datetime | None:
        """Parse the date string into a datetime object."""
        try:
            date_str_clean = re.sub(r'(\d{1,2})(?:st|nd|rd|th)', r'\1', date_str)
            return datetime.strptime(date_str_clean, '%d %B %Y')
        except ValueError as e:
            print(f"Date parsing error for '{date_str}': {e}")
            return None

    def __str__(self) -> str:
        date_display = self.date.strftime('%d %B %Y') if self.date else self.date_str
        return f"{self.title} ({date_display})"

class SkyBlockNews:
    """
    Handles fetching and managing all the news items from the API.

    Attributes:
        api_endpoint (str): The endpoint URL to fetch the news data.
        api_key (str): The API key required for the request.
        news_items (list[SkyBlockNewsItem]): A list of SkyBlockNewsItem objects.
    """

    def __init__(self, api_key: str, api_endpoint: str = NEWS_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self.api_key: str = api_key
        self.news_items: list[SkyBlockNewsItem] = []
        self._load_news()

    def _load_news(self) -> None:
        """Fetch news data from the API and initialize SkyBlockNewsItem objects."""
        try:
            params = {'key': self.api_key}
            response = requests.get(self.api_endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("success") and "items" in data and data["items"]:
                self.news_items = []
                for news_data in data["items"]:
                    material_data = news_data.get('item', {})
                    material = material_data.get('material')

                    news_item = SkyBlockNewsItem(
                        material=material,
                        link=news_data.get('link'),
                        date_str=news_data.get('text'),
                        title=news_data.get('title'),
                    )
                    self.news_items.append(news_item)
            else:
                raise ValueError("No news data available in the response")
        except requests.exceptions.HTTPError as e:
            response_status = response.status_code
            if response_status == 403:
                raise PermissionError("Access forbidden: Invalid API key.")
            elif response_status == 429:
                raise ConnectionError("Request limit reached: Throttling in effect.")
            else:
                raise ConnectionError(f"An error occurred while fetching news: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching news: {e}")

    def get_latest_news(self) -> SkyBlockNewsItem | None:
        """
        Retrieve the latest news item.

        Returns:
            SkyBlockNewsItem | None: The latest SkyBlockNewsItem object, or None if no news is available.
        """
        return self.news_items[0] if self.news_items else None

    def get_all_news(self) -> list[SkyBlockNewsItem]:
        """
        Retrieve all news items.

        Returns:
            list[SkyBlockNewsItem]: A list of all SkyBlockNewsItem objects.
        """
        return self.news_items

    def search_news_by_title(self, keyword: str) -> list[SkyBlockNewsItem]:
        """
        Search news items by a keyword in their title.

        Args:
            keyword (str): The keyword to search for in the news titles.

        Returns:
            list[SkyBlockNewsItem]: A list of news items that contain the keyword in their title.
        """
        return [
            news_item for news_item in self.news_items
            if keyword.lower() in news_item.title.lower()
        ]

    def get_news_by_date(self, target_date: date) -> list[SkyBlockNewsItem]:
        """
        Retrieve news items for a specific date.

        Args:
            target_date (date): The date to filter news items by.

        Returns:
            list[SkyBlockNewsItem]: A list of news items published on the specified date.
        """
        return [
            news_item for news_item in self.news_items
            if news_item.date and news_item.date.date() == target_date
        ]
