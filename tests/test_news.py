import unittest
from unittest.mock import patch
import requests
from datetime import date

from hypixel_api_lib.News import SkyBlockNews, SkyBlockNewsItem

class TestSkyBlockNews(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response
        self.sample_api_response = {
            "success": True,
            "items": [
                {
                    "item": {"material": "GOLD_BLOCK"},
                    "link": "https://hypixel.net/threads/5783275/",
                    "text": "15th October 2024",
                    "title": "SkyBlock v0.20.7"
                },
                {
                    "item": {"material": "DIAMOND_PICKAXE"},
                    "link": "https://hypixel.net/threads/5763578/",
                    "text": "17th September 2024",
                    "title": "SkyBlock v0.20.6"
                },
                {
                    "item": {"material": "INK_SACK"},
                    "link": "https://hypixel.net/threads/5738722/",
                    "text": "6th August 2024",
                    "title": "SkyBlock v0.20.5"
                },
                {
                    "item": {"material": "RAW_BEEF"},
                    "link": "https://hypixel.net/threads/5713272/",
                    "text": "9th July 2024",
                    "title": "SkyBlock v0.20.4"
                },
                {
                    "item": {"material": "JUKEBOX"},
                    "link": "https://hypixel.net/threads/5692280/",
                    "text": "2nd July 2024",
                    "title": "SkyBlock v0.20.3"
                },
                {
                    "item": {"material": "RABBIT_HIDE"},
                    "link": "https://hypixel.net/threads/5673834/",
                    "text": "28th May 2024",
                    "title": "SkyBlock v0.20.2"
                },
                {
                    "item": {"material": "RABBIT_FOOT"},
                    "link": "https://hypixel.net/threads/5645591/",
                    "text": "24th April 2024",
                    "title": "SkyBlock v0.20.1"
                }
            ]
        }
        self.dummy_api_key = 'DUMMY_API_KEY'

    @patch('requests.get')
    def test_load_news(self, mock_get):
        """
        Test that news items are loaded correctly from the API.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        self.assertIsNotNone(news_manager.news_items)
        self.assertEqual(len(news_manager.news_items), 7)
        self.assertEqual(news_manager.news_items[0].title, "SkyBlock v0.20.7")
        self.assertEqual(news_manager.news_items[0].material, "GOLD_BLOCK")

    @patch('requests.get')
    def test_get_latest_news(self, mock_get):
        """
        Test retrieving the latest news item.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        latest_news = news_manager.get_latest_news()
        self.assertIsNotNone(latest_news)
        self.assertIsInstance(latest_news, SkyBlockNewsItem)
        self.assertEqual(latest_news.title, "SkyBlock v0.20.7")
        self.assertEqual(latest_news.link, "https://hypixel.net/threads/5783275/")

    @patch('requests.get')
    def test_get_all_news(self, mock_get):
        """
        Test retrieving all news items.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        all_news = news_manager.get_all_news()
        self.assertEqual(len(all_news), 7)
        titles = [news_item.title for news_item in all_news]
        expected_titles = [
            "SkyBlock v0.20.7",
            "SkyBlock v0.20.6",
            "SkyBlock v0.20.5",
            "SkyBlock v0.20.4",
            "SkyBlock v0.20.3",
            "SkyBlock v0.20.2",
            "SkyBlock v0.20.1",
        ]
        self.assertEqual(titles, expected_titles)

    @patch('requests.get')
    def test_search_news_by_title(self, mock_get):
        """
        Test searching news items by title.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        keyword = "v0.20.5"
        matching_news = news_manager.search_news_by_title(keyword)
        self.assertEqual(len(matching_news), 1)
        self.assertEqual(matching_news[0].title, "SkyBlock v0.20.5")

        keyword = "v0.20"
        matching_news = news_manager.search_news_by_title(keyword)
        self.assertEqual(len(matching_news), 7)

    @patch('requests.get')
    def test_get_news_by_date(self, mock_get):
        """
        Test retrieving news items by date.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        specific_date = date(2024, 10, 15)
        news_on_date = news_manager.get_news_by_date(specific_date)
        self.assertEqual(len(news_on_date), 1)
        self.assertEqual(news_on_date[0].title, "SkyBlock v0.20.7")

        specific_date = date(2024, 7, 9)
        news_on_date = news_manager.get_news_by_date(specific_date)
        self.assertEqual(len(news_on_date), 1)
        self.assertEqual(news_on_date[0].title, "SkyBlock v0.20.4")

    @patch('requests.get')
    def test_news_item_with_missing_fields(self, mock_get):
        """
        Test handling of news items with missing optional fields.
        """
        sample_response_with_missing_fields = {
            "success": True,
            "items": [
                {
                    "item": {}, 
                    "link": None,  
                    "text": "1st January 2024",
                    # Missing title and empty fields
                }
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response_with_missing_fields

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        self.assertEqual(len(news_manager.news_items), 1)
        news_item = news_manager.news_items[0]
        self.assertIsNone(news_item.material)
        self.assertIsNone(news_item.link)
        self.assertIsNone(news_item.title)
        self.assertEqual(news_item.date_str, "1st January 2024")
        self.assertIsNotNone(news_item.date)
        self.assertEqual(news_item.date.year, 2024)
        self.assertEqual(news_item.date.month, 1)
        self.assertEqual(news_item.date.day, 1)

    @patch('requests.get')
    def test_date_parsing(self, mock_get):
        """
        Test the date parsing functionality of SkyBlockNewsItem.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        news_item = news_manager.news_items[0]
        self.assertEqual(news_item.date.day, 15)
        self.assertEqual(news_item.date.month, 10)
        self.assertEqual(news_item.date.year, 2024)

    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """
        Test the SkyBlockNews class's handling of API errors.
        """
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")

        with self.assertRaises(ConnectionError) as context:
            SkyBlockNews(api_key=self.dummy_api_key)

        self.assertIn("An error occurred while fetching news: API error", str(context.exception))

    @patch('requests.get')
    def test_empty_news_list(self, mock_get):
        """
        Test how the SkyBlockNews class handles an empty news list.
        """
        empty_response = {
            "success": True,
            "items": []
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = empty_response

        with self.assertRaises(ValueError) as context:
            SkyBlockNews(api_key=self.dummy_api_key)

        self.assertIn("No news data available in the response", str(context.exception))

    @patch('requests.get')
    def test_invalid_api_key(self, mock_get):
        """
        Test handling of invalid API key (403 error).
        """
        mock_get.return_value.status_code = 403
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Client Error: Forbidden for url")

        with self.assertRaises(PermissionError) as context:
            SkyBlockNews(api_key=self.dummy_api_key)

        self.assertIn("Access forbidden: Invalid API key.", str(context.exception))

    @patch('requests.get')
    def test_rate_limiting(self, mock_get):
        """
        Test handling of rate limiting (429 error).
        """
        mock_get.return_value.status_code = 429
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("429 Client Error: Too Many Requests for url")

        with self.assertRaises(ConnectionError) as context:
            SkyBlockNews(api_key=self.dummy_api_key)

        self.assertIn("Request limit reached: Throttling in effect.", str(context.exception))

    @patch('requests.get')
    def test_date_parsing_invalid_date(self, mock_get):
        """
        Test handling of invalid date strings in SkyBlockNewsItem.
        """
        sample_response_invalid_date = {
            "success": True,
            "items": [
                {
                    "item": {"material": "INVALID_MATERIAL"},
                    "link": "https://hypixel.net/threads/invalid/",
                    "text": "InvalidDate",
                    "title": "Invalid News Item"
                }
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response_invalid_date

        news_manager = SkyBlockNews(api_key=self.dummy_api_key)

        self.assertEqual(len(news_manager.news_items), 1)
        news_item = news_manager.news_items[0]
        self.assertIsNone(news_item.date)
        self.assertEqual(news_item.date_str, "InvalidDate")

if __name__ == '__main__':
    unittest.main()
