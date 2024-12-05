import unittest
from unittest.mock import patch
import requests
from datetime import datetime
from hypixel_api_lib.Bazaar import (
    Bazaar,
    BazaarProduct,
    BazaarProductQuickStatus,
    BazaarOrderSummaryItem
)

class TestBazaarComponent(unittest.TestCase):
    def setUp(self):
        # Sample API response mimicking bazaar data
        self.sample_api_response = {
            "success": True,
            "lastUpdated": 1731945336382,
            "products": {
                "INK_SACK:3": {
                    "product_id": "INK_SACK:3",
                    "sell_summary": [
                        {
                            "amount": 20569,
                            "pricePerUnit": 4.2,
                            "orders": 1
                        }
                    ],
                    "buy_summary": [
                        {
                            "amount": 25957,
                            "pricePerUnit": 5.0,
                            "orders": 3
                        }
                    ],
                    "quick_status": {
                        "productId": "INK_SACK:3",
                        "sellPrice": 4.2,
                        "sellVolume": 409855,
                        "sellMovingWeek": 8301075,
                        "sellOrders": 11,
                        "buyPrice": 5.0,
                        "buyVolume": 1254854,
                        "buyMovingWeek": 5830656,
                        "buyOrders": 85
                    }
                },
                "ENCHANTMENT_ULTIMATE_WISDOM_5": {
                    "product_id": "ENCHANTMENT_ULTIMATE_WISDOM_5",
                    "sell_summary": [],
                    "buy_summary": [],
                    "quick_status": {
                        "productId": "ENCHANTMENT_ULTIMATE_WISDOM_5",
                        "sellPrice": 5000000.0,
                        "sellVolume": 100,
                        "sellMovingWeek": 700,
                        "sellOrders": 5,
                        "buyPrice": 4800000.0,
                        "buyVolume": 200,
                        "buyMovingWeek": 900,
                        "buyOrders": 10
                    }
                },
                "DIAMOND": {
                    "product_id": "DIAMOND",
                    "sell_summary": [],
                    "buy_summary": [],
                    "quick_status": {
                        "productId": "DIAMOND",
                        "sellPrice": 10.0,
                        "sellVolume": 100000,
                        "sellMovingWeek": 700000,
                        "sellOrders": 50,
                        "buyPrice": 9.5,
                        "buyVolume": 120000,
                        "buyMovingWeek": 800000,
                        "buyOrders": 60
                    }
                }
            }
        }

    @patch("requests.get")
    def test_bazaar_initialization(self, mock_get):
        """Test initialization of Bazaar and loading of products."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()

        self.assertIsInstance(bazaar.last_updated, datetime)
        self.assertIn("INK_SACK:3", bazaar.products)
        self.assertIn("ENCHANTMENT_ULTIMATE_WISDOM_5", bazaar.products)
        self.assertIn("DIAMOND", bazaar.products)

    def test_bazaar_order_summary_item_initialization(self):
        """Test initialization of BazaarOrderSummaryItem."""
        summary_data = {
            "amount": 20569,
            "pricePerUnit": 4.2,
            "orders": 1
        }
        summary_item = BazaarOrderSummaryItem(summary_data)

        self.assertEqual(summary_item.amount, 20569)
        self.assertEqual(summary_item.price_per_unit, 4.2)
        self.assertEqual(summary_item.orders, 1)

    def test_bazaar_product_quick_status_initialization(self):
        """Test initialization of BazaarProductQuickStatus."""
        quick_status_data = {
            "productId": "INK_SACK:3",
            "sellPrice": 4.2,
            "sellVolume": 409855,
            "sellMovingWeek": 8301075,
            "sellOrders": 11,
            "buyPrice": 5.0,
            "buyVolume": 1254854,
            "buyMovingWeek": 5830656,
            "buyOrders": 85
        }
        quick_status = BazaarProductQuickStatus(quick_status_data)

        self.assertEqual(quick_status.product_id, "INK_SACK:3")
        self.assertEqual(quick_status.sell_price, 4.2)
        self.assertEqual(quick_status.sell_volume, 409855)
        self.assertEqual(quick_status.sell_moving_week, 8301075)
        self.assertEqual(quick_status.sell_orders, 11)
        self.assertEqual(quick_status.buy_price, 5.0)
        self.assertEqual(quick_status.buy_volume, 1254854)
        self.assertEqual(quick_status.buy_moving_week, 5830656)
        self.assertEqual(quick_status.buy_orders, 85)

    def test_bazaar_product_initialization(self):
        """Test initialization of BazaarProduct."""
        product_data = self.sample_api_response['products']['INK_SACK:3']
        product = BazaarProduct("INK_SACK:3", product_data)

        self.assertEqual(product.product_id, "INK_SACK:3")
        self.assertEqual(len(product.sell_summary), 1)
        self.assertEqual(len(product.buy_summary), 1)
        self.assertIsInstance(product.quick_status, BazaarProductQuickStatus)

    def test_bazaar_product_get_top_buy_order(self):
        """Test getting the top buy order from a BazaarProduct."""
        product_data = self.sample_api_response['products']['INK_SACK:3']
        product = BazaarProduct("INK_SACK:3", product_data)
        top_buy_order = product.get_top_buy_order()

        self.assertIsNotNone(top_buy_order)
        self.assertEqual(top_buy_order.price_per_unit, 5.0)

    def test_bazaar_product_get_top_sell_order(self):
        """Test getting the top sell order from a BazaarProduct."""
        product_data = self.sample_api_response['products']['INK_SACK:3']
        product = BazaarProduct("INK_SACK:3", product_data)
        top_sell_order = product.get_top_sell_order()

        self.assertIsNotNone(top_sell_order)
        self.assertEqual(top_sell_order.price_per_unit, 4.2)

    @patch("requests.get")
    def test_get_product_by_id(self, mock_get):
        """Test retrieving a product by its exact ID."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.get_product_by_id("INK_SACK:3")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "INK_SACK:3")

    @patch("requests.get")
    def test_search_product_exact_match(self, mock_get):
        """Test searching for a product with an exact match."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("INK_SACK:3")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "INK_SACK:3")

    @patch("requests.get")
    def test_search_product_normalized_match(self, mock_get):
        """Test searching for a product with a normalized search term."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("ink sack 3")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "INK_SACK:3")

    @patch("requests.get")
    def test_search_product_with_prefix_suffix(self, mock_get):
        """Test searching for a product that requires adding common prefixes or suffixes."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("ultimate wisdom 5")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "ENCHANTMENT_ULTIMATE_WISDOM_5")

    @patch("requests.get")
    def test_search_product_fuzzy_match(self, mock_get):
        """Test searching for a product using a fuzzy search."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("diamnd")  # Intentional typo

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "DIAMOND")

    @patch("requests.get")
    def test_search_product_not_found(self, mock_get):
        """Test searching for a product that does not exist."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("nonexistent product")

        self.assertIsNone(product)

    @patch("requests.get")
    def test_error_handling(self, mock_get):
        """Test error handling when the API call fails."""
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        with self.assertRaises(ConnectionError):
            Bazaar()

    @patch("requests.get")
    def test_no_success_response(self, mock_get):
        """Test handling of a response where success is False."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": False,
            "error": "Invalid API Key"
        }

        with self.assertRaises(ValueError):
            Bazaar()

    def test_normalize_product_id(self):
        """Test normalization of product IDs."""
        bazaar = Bazaar.__new__(Bazaar)  # Create an uninitialized instance
        bazaar.COMMON_PREFIXES = ["ENCHANTMENT_ULTIMATE_", "ENCHANTMENT_", "DUNGEON_"]
        bazaar.COMMON_SUFFIXES = ["_ITEM", "_SCROLL", "_GEM", "_ORE"]

        product_id = "ENCHANTMENT_ULTIMATE_WISDOM_5"
        normalized = bazaar._normalize_product_id(product_id)
        self.assertEqual(normalized, "WISDOM_5")

        product_id = "DIAMOND_ORE"
        normalized = bazaar._normalize_product_id(product_id)
        self.assertEqual(normalized, "DIAMOND")

    def test_normalize_search_term(self):
        """Test normalization of search terms."""
        bazaar = Bazaar.__new__(Bazaar)  # Create an uninitialized instance

        search_term = "ultimate wisdom 5"
        normalized = bazaar._normalize_search_term(search_term)
        self.assertEqual(normalized, "ULTIMATE_WISDOM_5")

        search_term = "diamond ore"
        normalized = bazaar._normalize_search_term(search_term)
        self.assertEqual(normalized, "DIAMOND_ORE")

    def test_generate_possible_product_ids(self):
        """Test generating possible product IDs from a base term."""
        bazaar = Bazaar.__new__(Bazaar)  # Create an uninitialized instance
        bazaar.COMMON_PREFIXES = ["ENCHANTMENT_ULTIMATE_", "ENCHANTMENT_", "DUNGEON_"]
        bazaar.COMMON_SUFFIXES = ["_ITEM", "_SCROLL", "_GEM", "_ORE"]

        base_term = "WISDOM_5"
        possible_ids = bazaar._generate_possible_product_ids(base_term)

        expected_ids = set([
            "WISDOM_5",
            "ENCHANTMENT_ULTIMATE_WISDOM_5",
            "ENCHANTMENT_WISDOM_5",
            "DUNGEON_WISDOM_5",
            "WISDOM_5_ITEM",
            "WISDOM_5_SCROLL",
            "WISDOM_5_GEM",
            "WISDOM_5_ORE",
            "ENCHANTMENT_ULTIMATE_WISDOM_5_ITEM",
            "ENCHANTMENT_ULTIMATE_WISDOM_5_SCROLL",
            "ENCHANTMENT_ULTIMATE_WISDOM_5_GEM",
            "ENCHANTMENT_ULTIMATE_WISDOM_5_ORE",
        ])

        self.assertTrue(set(possible_ids).issuperset(expected_ids))

    def test_bazaar_product_str(self):
        """Test the __str__ method of BazaarProduct."""
        product_data = self.sample_api_response['products']['INK_SACK:3']
        product = BazaarProduct("INK_SACK:3", product_data)

        expected_str = "Bazaar Product: INK_SACK:3"
        self.assertEqual(str(product), expected_str)

    def test_bazaar_order_summary_item_str(self):
        """Test the __str__ method of BazaarOrderSummaryItem."""
        summary_data = {
            "amount": 20569,
            "pricePerUnit": 4.2,
            "orders": 1
        }
        summary_item = BazaarOrderSummaryItem(summary_data)

        expected_str = "Amount: 20569, Price per Unit: 4.2, Orders: 1"
        self.assertEqual(str(summary_item), expected_str)

    def test_bazaar_product_quick_status_str(self):
        """Test the __str__ method of BazaarProductQuickStatus."""
        quick_status_data = {
            "productId": "INK_SACK:3",
            "sellPrice": 4.2,
            "sellVolume": 409855,
            "sellMovingWeek": 8301075,
            "sellOrders": 11,
            "buyPrice": 5.0,
            "buyVolume": 1254854,
            "buyMovingWeek": 5830656,
            "buyOrders": 85
        }
        quick_status = BazaarProductQuickStatus(quick_status_data)

        expected_str = (
            "Product ID: INK_SACK:3, Sell Price: 4.2, Sell Volume: 409855, "
            "Sell Moving Week: 8301075, Sell Orders: 11, Buy Price: 5.0, "
            "Buy Volume: 1254854, Buy Moving Week: 5830656, Buy Orders: 85"
        )
        self.assertEqual(str(quick_status), expected_str)

    @patch("requests.get")
    def test_bazaar_str(self, mock_get):
        """Test the __str__ method of Bazaar."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()

        expected_str_start = f"Bazaar Data (Last Updated: {bazaar.last_updated})\nProducts: "
        self.assertTrue(str(bazaar).startswith(expected_str_start))

    @patch("requests.get")
    def test_bazaar_normalized_product_ids(self, mock_get):
        """Test that normalized_product_ids are correctly populated."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()

        expected_normalized_ids = {
            "INK_SACK_3": "INK_SACK:3",
            "WISDOM": "ENCHANTMENT_ULTIMATE_WISDOM_5",
            "DIAMOND": "DIAMOND"
        }

        for normalized, product_id in expected_normalized_ids.items():
            self.assertEqual(bazaar.normalized_product_ids.get(normalized), product_id)

    @patch("requests.get")
    def test_fuzzy_search_multiple_matches(self, mock_get):
        """Test fuzzy search when multiple close matches are possible."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        # Assuming "diamond" and "diamon" are close enough
        product = bazaar.search_product("diamon")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "DIAMOND")

    @patch("requests.get")
    def test_search_product_with_numbers(self, mock_get):
        """Test searching for products with numerical suffixes."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("wisdom 5")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "ENCHANTMENT_ULTIMATE_WISDOM_5")

    @patch("requests.get")
    def test_search_product_with_common_suffix(self, mock_get):
        """Test searching for a product that has a common suffix in the ID."""
        self.sample_api_response['products']['MITHRIL_ORE'] = {
            "product_id": "MITHRIL_ORE",
            "sell_summary": [],
            "buy_summary": [],
            "quick_status": {}
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("mithril")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "MITHRIL_ORE")

    @patch("requests.get")
    def test_search_product_case_insensitive(self, mock_get):
        """Test that the search is case-insensitive."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("Ink Sack 3")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "INK_SACK:3")

    @patch("requests.get")
    def test_search_product_with_special_characters(self, mock_get):
        """Test searching for a product with special characters in the name."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.search_product("ink-sack:3")

        self.assertIsNotNone(product)
        self.assertEqual(product.product_id, "INK_SACK:3")

    @patch("requests.get")
    def test_get_top_buy_order_none(self, mock_get):
        """Test get_top_buy_order when there are no buy orders."""
        self.sample_api_response['products']['DIAMOND']['buy_summary'] = []
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.get_product_by_id("DIAMOND")
        top_buy_order = product.get_top_buy_order()

        self.assertIsNone(top_buy_order)

    @patch("requests.get")
    def test_get_top_sell_order_none(self, mock_get):
        """Test get_top_sell_order when there are no sell orders."""
        self.sample_api_response['products']['DIAMOND']['sell_summary'] = []
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bazaar = Bazaar()
        product = bazaar.get_product_by_id("DIAMOND")
        top_sell_order = product.get_top_sell_order()

        self.assertIsNone(top_sell_order)

if __name__ == "__main__":
    unittest.main()
