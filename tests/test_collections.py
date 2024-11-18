import unittest
from unittest.mock import patch
import requests
from datetime import datetime
from hypixel_api_lib.Collections import (
    Collections,
    CollectionCategory,
    CollectionItem,
    CollectionTier
)

class TestCollectionsComponent(unittest.TestCase):
    def setUp(self):
        # Sample API response mimicking collections data
        self.sample_api_response = {
            "success": True,
            "lastUpdated": 1731945336382,
            "version": "1.0.0",
            "collections": {
                "FARMING": {
                    "name": "Farming",
                    "items": {
                        "WHEAT": {
                            "name": "Wheat",
                            "maxTiers": 3,
                            "tiers": [
                                {"tier": 1, "amountRequired": 50, "unlocks": ["Wheat Minion I"]},
                                {"tier": 2, "amountRequired": 100, "unlocks": ["Wheat Minion II"]},
                                {"tier": 3, "amountRequired": 250, "unlocks": ["Wheat Minion III"]}
                            ]
                        }
                    }
                },
                "MINING": {
                    "name": "Mining",
                    "items": {
                        "COAL": {
                            "name": "Coal",
                            "maxTiers": 2,
                            "tiers": [
                                {"tier": 1, "amountRequired": 10, "unlocks": ["Coal Minion I"]},
                                {"tier": 2, "amountRequired": 50, "unlocks": ["Coal Minion II"]}
                            ]
                        }
                    }
                }
            }
        }

    @patch("requests.get")
    def test_collections_initialization(self, mock_get):
        """Test initialization of Collections and loading of categories."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        collections = Collections()

        self.assertEqual(collections.version, "1.0.0")
        self.assertIsInstance(collections.last_updated, datetime)
        self.assertIn("FARMING", collections.categories)
        self.assertIn("MINING", collections.categories)

    @patch("requests.get")
    def test_category_initialization(self, mock_get):
        """Test initialization of a CollectionCategory."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        collections = Collections()
        farming_category = collections.get_category_by_key("FARMING")

        self.assertIsNotNone(farming_category)
        self.assertEqual(farming_category.name, "Farming")
        self.assertIn("WHEAT", farming_category.items)

    def test_item_initialization(self):
        """Test initialization of a CollectionItem."""
        wheat_data = {
            "name": "Wheat",
            "maxTiers": 3,
            "tiers": [
                {"tier": 1, "amountRequired": 50, "unlocks": ["Wheat Minion I"]},
                {"tier": 2, "amountRequired": 100, "unlocks": ["Wheat Minion II"]},
                {"tier": 3, "amountRequired": 250, "unlocks": ["Wheat Minion III"]}
            ]
        }

        wheat_item = CollectionItem("WHEAT", wheat_data)

        self.assertEqual(wheat_item.key, "WHEAT")
        self.assertEqual(wheat_item.name, "Wheat")
        self.assertEqual(wheat_item.max_tiers, 3)
        self.assertEqual(len(wheat_item.tiers), 3)

    def test_tier_initialization(self):
        """Test initialization of a CollectionTier."""
        tier_data = {"tier": 1, "amountRequired": 50, "unlocks": ["Wheat Minion I"]}

        tier = CollectionTier(tier_data)

        self.assertEqual(tier.tier, 1)
        self.assertEqual(tier.amount_required, 50)
        self.assertEqual(tier.unlocks, ["Wheat Minion I"])

    @patch("requests.get")
    def test_get_item_by_key(self, mock_get):
        """Test retrieving an item by its key."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        collections = Collections()
        wheat_item = collections.get_item_by_key("WHEAT")

        self.assertIsNotNone(wheat_item)
        self.assertEqual(wheat_item.name, "Wheat")

    @patch("requests.get")
    def test_get_item_by_name(self, mock_get):
        """Test retrieving an item by its name."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        collections = Collections()
        coal_item = collections.get_item_by_name("Coal")

        self.assertIsNotNone(coal_item)
        self.assertEqual(coal_item.key, "COAL")

    @patch("requests.get")
    def test_error_handling(self, mock_get):
        """Test error handling when the API call fails."""
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        with self.assertRaises(ConnectionError):
            Collections()

    @patch("requests.get")
    def test_no_success_response(self, mock_get):
        """Test handling of a response where success is False."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": False,
            "error": "Invalid API Key"
        }

        with self.assertRaises(ValueError):
            Collections()

    @patch("requests.get")
    def test_get_category_by_name(self, mock_get):
        """Test retrieving a category by its name."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        collections = Collections()
        farming_category = collections.get_category_by_name("Farming")

        self.assertIsNotNone(farming_category)
        self.assertEqual(farming_category.key, "FARMING")

    def test_item_str(self):
        """Test the __str__ method of a CollectionItem."""
        wheat_data = {
            "name": "Wheat",
            "maxTiers": 3,
            "tiers": []
        }
        wheat_item = CollectionItem("WHEAT", wheat_data)

        expected_str = "Collection Item: Wheat (Key: WHEAT), Max Tiers: 3"
        self.assertEqual(str(wheat_item), expected_str)

    def test_category_str(self):
        """Test the __str__ method of a CollectionCategory."""
        category_data = {
            "name": "Farming",
            "items": {}
        }
        farming_category = CollectionCategory("FARMING", category_data)

        expected_str = "Collection Category: Farming (Key: FARMING), Items: 0"
        self.assertEqual(str(farming_category), expected_str)

    def test_tier_str(self):
        """Test the __str__ method of a CollectionTier."""
        tier_data = {"tier": 1, "amountRequired": 50, "unlocks": ["Wheat Minion I"]}

        tier = CollectionTier(tier_data)
        expected_str = "Tier 1: Requires 50, Unlocks: Wheat Minion I"
        self.assertEqual(str(tier), expected_str)


if __name__ == "__main__":
    unittest.main()
