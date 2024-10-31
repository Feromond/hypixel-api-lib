import requests
import re
from datetime import datetime

NEWS_API_URL = "https://api.hypixel.net/skyblock/news"

class SkyBlockNewsItem:
    """
    Represents a news item in SkyBlock.

    Attributes:
        material (str): The material associated with the news item (e.g., 'GOLD_BLOCK').
        link (str): The URL link to the full news article.
        date (datetime): The date of the news item.
        title (str): The title of the news item.
    """

    def __init__(self, material, link, date_str, title):
        self.material = material
        self.link = link
        self.date_str = date_str
        self.date = self._parse_date(date_str)
        self.title = title

    def _parse_date(self, date_str):
        """Parse the date string into a datetime object."""
        try:
            date_str_clean = re.sub(r'(\d{1,2})(?:st|nd|rd|th)', r'\1', date_str)
            return datetime.strptime(date_str_clean, '%d %B %Y')
        except ValueError as e:
            print(f"Date parsing error for '{date_str}': {e}")
            return None

    def __str__(self):
        date_display = self.date.strftime('%d %B %Y') if self.date else self.date_str
        return f"{self.title} ({date_display})"

class SkyBlockNews:
    """
    Handles fetching and managing all the news items from the API.

    Attributes:
        api_endpoint (str): The endpoint URL to fetch the news data.
        api_key (str): The API key required for the request.
        news_items (list of SkyBlockNewsItem): A list of SkyBlockNewsItem objects.
    """

    def __init__(self, api_key, api_endpoint=NEWS_API_URL):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.news_items = []
        self._load_news()

    def _load_news(self):
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

    def get_latest_news(self):
        """
        Retrieve the latest news item.

        Returns:
            SkyBlockNewsItem or None: The latest SkyBlockNewsItem object, or None if no news is available.
        """
        return self.news_items[0] if self.news_items else None

    def get_all_news(self):
        """
        Retrieve all news items.

        Returns:
            list of SkyBlockNewsItem: A list of all SkyBlockNewsItem objects.
        """
        return self.news_items

    def search_news_by_title(self, keyword):
        """
        Search news items by a keyword in their title.

        Args:
            keyword (str): The keyword to search for in the news titles.

        Returns:
            list of SkyBlockNewsItem: A list of news items that contain the keyword in their title.
        """
        return [
            news_item for news_item in self.news_items
            if keyword.lower() in news_item.title.lower()
        ]

    def get_news_by_date(self, date):
        """
        Retrieve news items for a specific date.

        Args:
            date (datetime.date): The date to filter news items by.

        Returns:
            list of SkyBlockNewsItem: A list of news items published on the specified date.
        """
        return [
            news_item for news_item in self.news_items
            if news_item.date and news_item.date.date() == date
        ]
