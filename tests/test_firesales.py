import unittest
from unittest.mock import patch
import requests
from datetime import datetime, timezone, timedelta

from hypixel_api_lib.FireSales import FireSales, FireSaleItem

class TestFireSales(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response
        self.sample_api_response = {
            "success": True,
            "sales": [
                {
                    "item_id": "DYE_LAVA",
                    "start": int((datetime.now(timezone.utc) - timedelta(days=1)).timestamp() * 1000),
                    "end": int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp() * 1000),
                    "amount": 60000,
                    "price": 375
                },
                {
                    "item_id": "DYE_WATER",
                    "start": int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp() * 1000),
                    "end": int((datetime.now(timezone.utc) + timedelta(days=2)).timestamp() * 1000),
                    "amount": 50000,
                    "price": 350
                },
                {
                    "item_id": "DYE_EARTH",
                    "start": int((datetime.now(timezone.utc) - timedelta(days=3)).timestamp() * 1000),
                    "end": int((datetime.now(timezone.utc) - timedelta(days=2)).timestamp() * 1000),
                    "amount": 45000,
                    "price": 300
                }
            ]
        }

    @patch('requests.get')
    def test_load_fire_sales(self, mock_get):
        """
        Test that fire sales are loaded correctly from the API.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()

        self.assertIsNotNone(fire_sales.sales)
        self.assertEqual(len(fire_sales.sales), 3)
        item_ids = [sale.item_id for sale in fire_sales.sales]
        self.assertIn("DYE_LAVA", item_ids)
        self.assertIn("DYE_WATER", item_ids)
        self.assertIn("DYE_EARTH", item_ids)

    @patch('requests.get')
    def test_get_sale_by_item_id_existing(self, mock_get):
        """
        Test retrieving an existing fire sale by item ID.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()

        sale = fire_sales.get_sale_by_item_id("DYE_LAVA")
        self.assertIsInstance(sale, FireSaleItem)
        self.assertEqual(sale.item_id, "DYE_LAVA")
        self.assertEqual(sale.amount, 60000)
        self.assertEqual(sale.price, 375)

    @patch('requests.get')
    def test_get_sale_by_item_id_nonexistent(self, mock_get):
        """
        Test retrieving a non-existent fire sale by item ID.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()

        sale = fire_sales.get_sale_by_item_id("NON_EXISTENT_ITEM")
        self.assertIsNone(sale)

    @patch('requests.get')
    def test_get_active_sales(self, mock_get):
        """
        Test retrieving currently active fire sales.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()

        active_sales = fire_sales.get_active_sales()
        self.assertEqual(len(active_sales), 1)
        self.assertEqual(active_sales[0].item_id, "DYE_LAVA")

    @patch('requests.get')
    def test_get_upcoming_sales(self, mock_get):
        """
        Test retrieving upcoming fire sales.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()

        upcoming_sales = fire_sales.get_upcoming_sales()
        self.assertEqual(len(upcoming_sales), 1)
        self.assertEqual(upcoming_sales[0].item_id, "DYE_WATER")

    @patch('requests.get')
    def test_fire_sale_item_is_active(self, mock_get):
        """
        Test the is_active method of FireSaleItem.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()
        sale_active = fire_sales.get_sale_by_item_id("DYE_LAVA")
        sale_upcoming = fire_sales.get_sale_by_item_id("DYE_WATER")
        sale_past = fire_sales.get_sale_by_item_id("DYE_EARTH")

        self.assertTrue(sale_active.is_active())
        self.assertFalse(sale_upcoming.is_active())
        self.assertFalse(sale_past.is_active())

    @patch('requests.get')
    def test_time_until_start_and_end(self, mock_get):
        """
        Test the time_until_start and time_until_end methods.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()
        sale_active = fire_sales.get_sale_by_item_id("DYE_LAVA")
        sale_upcoming = fire_sales.get_sale_by_item_id("DYE_WATER")
        sale_past = fire_sales.get_sale_by_item_id("DYE_EARTH")

        # For active sale
        time_until_start_active = sale_active.time_until_start()
        time_until_end_active = sale_active.time_until_end()
        self.assertIsNone(time_until_start_active)
        self.assertTrue(isinstance(time_until_end_active, timedelta))
        self.assertGreater(time_until_end_active.total_seconds(), 0)

        # For upcoming sale
        time_until_start_upcoming = sale_upcoming.time_until_start()
        time_until_end_upcoming = sale_upcoming.time_until_end()
        self.assertTrue(isinstance(time_until_start_upcoming, timedelta))
        self.assertGreater(time_until_start_upcoming.total_seconds(), 0)
        self.assertIsNone(time_until_end_upcoming)

        # For past sale
        time_until_start_past = sale_past.time_until_start()
        time_until_end_past = sale_past.time_until_end()
        self.assertIsNone(time_until_start_past)
        self.assertIsNone(time_until_end_past)

    @patch('requests.get')
    def test_fire_sale_item_str_representation(self, mock_get):
        """
        Test the string representation of FireSaleItem.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()
        sale = fire_sales.get_sale_by_item_id("DYE_LAVA")

        sale_str = str(sale)
        self.assertIn("Fire Sale Item 'DYE_LAVA'", sale_str)
        self.assertIn("Amount: 60000", sale_str)
        self.assertIn("Price: 375 Gems", sale_str)

    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """
        Test the FireSales class's handling of API errors.
        """
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")

        with self.assertRaises(ConnectionError) as context:
            FireSales()

        self.assertIn("An error occurred while fetching fire sales: API error", str(context.exception))

    @patch('requests.get')
    def test_empty_sales_list(self, mock_get):
        """
        Test how the FireSales class handles an empty sales list.
        """
        empty_response = {
            "success": True,
            "sales": []
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = empty_response

        fire_sales = FireSales()
        self.assertEqual(len(fire_sales.sales), 0)

    @patch('requests.get')
    def test_sale_with_missing_fields(self, mock_get):
        """
        Test handling of fire sales with missing optional fields.
        """
        sample_response_with_missing_fields = {
            "success": True,
            "sales": [
                {
                    "item_id": "INCOMPLETE_SALE"
                    # 'start', 'end', 'amount', 'price' are intentionally missing
                }
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response_with_missing_fields

        fire_sales = FireSales()

        sale = fire_sales.get_sale_by_item_id("INCOMPLETE_SALE")
        self.assertIsInstance(sale, FireSaleItem)
        self.assertEqual(sale.item_id, "INCOMPLETE_SALE")
        self.assertIsNone(sale.start)
        self.assertIsNone(sale.end)
        self.assertIsNone(sale.amount)
        self.assertIsNone(sale.price)

    @patch('requests.get')
    def test_sale_with_null_timestamps(self, mock_get):
        """
        Test handling of fire sales with null 'start' and 'end' timestamps.
        """
        sample_response_with_null_timestamps = {
            "success": True,
            "sales": [
                {
                    "item_id": "NULL_TIMESTAMP_SALE",
                    "start": None,
                    "end": None,
                    "amount": 10000,
                    "price": 200
                }
            ]
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response_with_null_timestamps

        fire_sales = FireSales()

        sale = fire_sales.get_sale_by_item_id("NULL_TIMESTAMP_SALE")
        self.assertIsInstance(sale, FireSaleItem)
        self.assertIsNone(sale.start)
        self.assertIsNone(sale.end)
        self.assertEqual(sale.amount, 10000)
        self.assertEqual(sale.price, 200)

        # Check methods that rely on timestamps
        self.assertFalse(sale.is_active())
        self.assertIsNone(sale.time_until_start())
        self.assertIsNone(sale.time_until_end())

    @patch('requests.get')
    def test_sales_str_representation(self, mock_get):
        """
        Test the string representation of the FireSales class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        fire_sales = FireSales()
        self.assertEqual(str(fire_sales), "FireSales with 3 active/upcoming sales")

if __name__ == '__main__':
    unittest.main()
