import unittest
from unittest.mock import patch
import requests

from hypixel_api_lib.Items import Items, SkyBlockItem

class TestItems(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response
        self.sample_api_response = {
            "success": True,
            "lastUpdated": 0,
            "items": [
                {
                    "id": "FARM_ARMOR_CHESTPLATE",
                    "material": "LEATHER_CHESTPLATE",
                    "color": "255,215,0",
                    "name": "Farm Armor Chestplate",
                    "category": "CHESTPLATE",
                    "tier": "RARE",
                    "stats": {
                        "DEFENSE": 75,
                        "HEALTH": 20
                    },
                    "npc_sell_price": 5200
                },
                {
                    "id": "MANDRAA",
                    "material": "SKULL_ITEM",
                    "durability": 3,
                    "skin": "ewogICJ0aW1lc3RhbXAiIDogMTY1MDAyODM2MDY3OCwKICAicHJvZmlsZUlkIiA6ICJiYzRlZGZiNWYzNmM0OGE3YWM5ZjFhMzlkYzIzZjRmOCIsCiAgInByb2ZpbGVOYW1lIiA6ICI4YWNhNjgwYjIyNDYxMzQwIiwKICAic2lnbmF0dXJlUmVxdWlyZWQiIDogdHJ1ZSwKICAidGV4dHVyZXMiIDogewogICAgIlNLSU4iIDogewogICAgICAidXJsIiA6ICJodHRwOi8vdGV4dHVyZXMubWluZWNyYWZ0Lm5ldC90ZXh0dXJlLzk0YTAyZTFhNGRjZjdhNjE1NThjNzljZGFiYjRmNzhlZDM3YWU4MmY5NjU1NDFiNjEyYWYwODhjZmNmZjJiMWIiCiAgICB9CiAgfQp9",
                    "name": "Mandraa",
                    "category": "REFORGE_STONE",
                    "tier": "RARE",
                    "npc_sell_price": 1
                },
                {
                    "id": "ASPECT_OF_THE_END",
                    "material": "DIAMOND_SWORD",
                    "name": "Aspect of the End",
                    "category": "SWORD",
                    "tier": "RARE"
                },
                {
                    "id": "SUPERIOR_DRAGON_HELMET",
                    "material": "DIAMOND_HELMET",
                    "name": "Superior Dragon Helmet",
                    "category": "HELMET",
                    "tier": "LEGENDARY",
                    "stats": {
                        "DEFENSE": 120,
                        "HEALTH": 90
                    },
                    "npc_sell_price": 10000
                },
                {
                    "id": "ITEM_WITHOUT_TIER",
                    "material": "STONE",
                    "name": "Mysterious Stone",
                    "category": "MISC"
                    # 'tier' is intentionally missing
                }
            ]
        }

    @patch('requests.get')
    def test_load_items(self, mock_get):
        """
        Test that items are loaded correctly from the API.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        self.assertIsNotNone(items_manager.items)
        self.assertEqual(len(items_manager.items), 5)
        self.assertIn("FARM_ARMOR_CHESTPLATE", items_manager.items)
        self.assertIn("MANDRAA", items_manager.items)

    @patch('requests.get')
    def test_get_item_existing(self, mock_get):
        """
        Test retrieving an existing item by ID.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        item = items_manager.get_item("FARM_ARMOR_CHESTPLATE")
        self.assertIsInstance(item, SkyBlockItem)
        self.assertEqual(item.name, "Farm Armor Chestplate")
        self.assertEqual(item.category, "CHESTPLATE")
        self.assertEqual(item.tier, "RARE")
        self.assertEqual(item.npc_sell_price, 5200)
        self.assertEqual(item.stats, {"DEFENSE": 75, "HEALTH": 20})

    @patch('requests.get')
    def test_get_item_nonexistent(self, mock_get):
        """
        Test retrieving a non-existent item by ID.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        item = items_manager.get_item("NON_EXISTENT_ITEM")
        self.assertIsInstance(item, str)
        self.assertEqual(item, "Item 'NON_EXISTENT_ITEM' not found.")

    @patch('requests.get')
    def test_get_items_by_tier(self, mock_get):
        """
        Test retrieving items by tier.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        rare_items = items_manager.get_items_by_tier("RARE")
        self.assertEqual(len(rare_items), 3)
        self.assertIn("FARM_ARMOR_CHESTPLATE", rare_items)
        self.assertIn("MANDRAA", rare_items)
        self.assertIn("ASPECT_OF_THE_END", rare_items)

        legendary_items = items_manager.get_items_by_tier("LEGENDARY")
        self.assertEqual(len(legendary_items), 1)
        self.assertIn("SUPERIOR_DRAGON_HELMET", legendary_items)

        unknown_tier_items = items_manager.get_items_by_tier("UNKNOWN")
        self.assertEqual(len(unknown_tier_items), 1)
        self.assertIn("ITEM_WITHOUT_TIER", unknown_tier_items)

    @patch('requests.get')
    def test_get_items_by_category(self, mock_get):
        """
        Test retrieving items by category.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        chestplate_items = items_manager.get_items_by_category("CHESTPLATE")
        self.assertEqual(len(chestplate_items), 1)
        self.assertIn("FARM_ARMOR_CHESTPLATE", chestplate_items)

        sword_items = items_manager.get_items_by_category("SWORD")
        self.assertEqual(len(sword_items), 1)
        self.assertIn("ASPECT_OF_THE_END", sword_items)

        misc_items = items_manager.get_items_by_category("MISC")
        self.assertEqual(len(misc_items), 1)
        self.assertIn("ITEM_WITHOUT_TIER", misc_items)

    @patch('requests.get')
    def test_list_item_names(self, mock_get):
        """
        Test listing all item names.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        item_names = items_manager.list_item_names()
        expected_names = [
            "Farm Armor Chestplate",
            "Mandraa",
            "Aspect of the End",
            "Superior Dragon Helmet",
            "Mysterious Stone"
        ]
        self.assertEqual(sorted(item_names), sorted(expected_names))

    @patch('requests.get')
    def test_list_item_categories(self, mock_get):
        """
        Test listing all unique item categories.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        categories = items_manager.list_item_categories()
        expected_categories = ["CHESTPLATE", "HELMET", "MISC", "REFORGE_STONE", "SWORD"]
        self.assertEqual(categories, sorted(expected_categories))

    @patch('requests.get')
    def test_item_with_missing_fields(self, mock_get):
        """
        Test handling of items with missing optional fields.
        """
        # Modify sample response to have an item with missing fields
        sample_response_with_missing_fields = {
            "success": True,
            "lastUpdated": 0,
            "items": [
                {
                    "id": "INCOMPLETE_ITEM",
                    "material": "DIRT",
                    "name": "Incomplete Item"
                    # Missing 'tier', 'category', 'stats', etc.
                }
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response_with_missing_fields

        items_manager = Items()

        item = items_manager.get_item("INCOMPLETE_ITEM")
        self.assertIsInstance(item, SkyBlockItem)
        self.assertEqual(item.id, "INCOMPLETE_ITEM")
        self.assertEqual(item.material, "DIRT")
        self.assertEqual(item.name, "Incomplete Item")
        self.assertEqual(item.tier, "UNKNOWN")
        self.assertIsNone(item.category)
        self.assertEqual(item.stats, {})
        self.assertIsNone(item.npc_sell_price)
        self.assertIsNone(item.color)
        self.assertIsNone(item.skin)
        self.assertIsNone(item.durability)

    @patch('requests.get')
    def test_get_formatted_stats(self, mock_get):
        """
        Test the get_formatted_stats method of SkyBlockItem.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        items_manager = Items()

        item_with_stats = items_manager.get_item("FARM_ARMOR_CHESTPLATE")
        formatted_stats = item_with_stats.get_formatted_stats()
        self.assertEqual(formatted_stats, "DEFENSE: 75, HEALTH: 20")

        item_without_stats = items_manager.get_item("ASPECT_OF_THE_END")
        formatted_stats = item_without_stats.get_formatted_stats()
        self.assertEqual(formatted_stats, "No stats available.")

    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """
        Test the Items class's handling of API errors.
        """
        # Simulate an API error
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")

        with self.assertRaises(ConnectionError) as context:
            Items()

        self.assertIn("An error occurred: API error", str(context.exception))

    @patch('requests.get')
    def test_empty_items_list(self, mock_get):
        """
        Test how the Items class handles an empty items list.
        """
        empty_response = {
            "success": True,
            "lastUpdated": 0,
            "items": []
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = empty_response

        with self.assertRaises(ValueError) as context:
            Items()

        self.assertIn("No items data available in the response", str(context.exception))

if __name__ == '__main__':
    unittest.main()
