import unittest
from unittest.mock import patch
import requests
from datetime import datetime, timezone

from hypixel_api_lib.Bingo import BingoEvents, BingoEvent, BingoGoal

class TestBingoComponent(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response
        self.sample_api_response = {
            "success": True,
            "lastUpdated": 1728619119062,
            "id": 34,
            "name": "October 2024",
            "start": 1727755200000,
            "end": 1728360000000,
            "modifier": "NORMAL",
            "goals": [
                {
                    "id": "kill_endermen",
                    "name": "Enderman Slayer",
                    "tiers": [500000, 1000000, 1500000, 2000000, 2500000],
                    "progress": 1250000,
                    "lore": "§7Kill §a2.5M Endermen§7.",
                    "fullLore": ["§7Kill §a2.5M Endermen§7."]
                },
                {
                    "id": "GET_SKILL_farming_5",
                    "name": "Farmer",
                    "lore": "§7Obtain level §e5§7 in the §6Farming §7Skill.",
                    "fullLore": ["§7Obtain level §e5§7 in the §6Farming §7Skill."]
                },
                {
                    "id": "collect_items",
                    "name": "Item Collector",
                    "requiredAmount": 100,
                    "progress": 50,
                    "lore": "§7Collect §a100 §7items.",
                    "fullLore": ["§7Collect §a100 §7items."]
                }
            ]
        }

    @patch('requests.get')
    def test_bingo_events_initialization(self, mock_get):
        """
        Test the initialization of the BingoEvents class and loading of current event.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_events = BingoEvents()
        current_event = bingo_events.get_current_event()

        self.assertIsNotNone(current_event)
        self.assertIsInstance(current_event, BingoEvent)
        self.assertEqual(current_event.id, 34)
        self.assertEqual(current_event.name, "October 2024")
        self.assertEqual(current_event.modifier, "NORMAL")
        self.assertEqual(len(current_event.goals), 3)

    @patch('requests.get')
    def test_bingo_event_goal_retrieval(self, mock_get):
        """
        Test retrieving goals by ID and name in the BingoEvent class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_events = BingoEvents()
        current_event = bingo_events.get_current_event()

        # Test get_goal_by_id
        goal_by_id = current_event.get_goal_by_id("kill_endermen")
        self.assertIsNotNone(goal_by_id)
        self.assertEqual(goal_by_id.name, "Enderman Slayer")

        # Test get_goal_by_name
        goal_by_name = current_event.get_goal_by_name("Farmer")
        self.assertIsNotNone(goal_by_name)
        self.assertEqual(goal_by_name.id, "GET_SKILL_farming_5")

        # Test non-existent goal
        self.assertIsNone(current_event.get_goal_by_id("non_existent_goal"))
        self.assertIsNone(current_event.get_goal_by_name("Non Existent Goal"))

    def test_bingo_goal_initialization(self):
        """
        Test the initialization of the BingoGoal class with complete and missing data.
        """
        # Complete data
        goal_data_complete = {
            "id": "test_goal",
            "name": "Test Goal",
            "lore": "§7Complete the test goal.",
            "fullLore": ["§7Complete the test goal in full."],
            "tiers": [100, 200, 300],
            "progress": 150,
            "requiredAmount": 300
        }
        goal_complete = BingoGoal(goal_data_complete)
        self.assertEqual(goal_complete.id, "test_goal")
        self.assertEqual(goal_complete.name, "Test Goal")
        self.assertEqual(goal_complete.lore, "§7Complete the test goal.")
        self.assertEqual(goal_complete.full_lore, ["§7Complete the test goal in full."])
        self.assertEqual(goal_complete.tiers, [100, 200, 300])
        self.assertEqual(goal_complete.progress, 150)
        self.assertEqual(goal_complete.required_amount, 300)

        # Missing optional data
        goal_data_partial = {
            "id": "partial_goal",
            "name": "Partial Goal"
            # Missing 'lore', 'fullLore', 'tiers', 'progress', 'requiredAmount'
        }
        goal_partial = BingoGoal(goal_data_partial)
        self.assertEqual(goal_partial.id, "partial_goal")
        self.assertEqual(goal_partial.name, "Partial Goal")
        self.assertEqual(goal_partial.lore, '')
        self.assertEqual(goal_partial.full_lore, [])
        self.assertEqual(goal_partial.tiers, [])
        self.assertEqual(goal_partial.progress, 0)
        self.assertIsNone(goal_partial.required_amount)

    def test_bingo_goal_completion_percentage(self):
        """
        Test the get_completion_percentage method of the BingoGoal class.
        """
        # Goal with required_amount
        goal_data_required = {
            "id": "collect_items",
            "name": "Item Collector",
            "requiredAmount": 100,
            "progress": 50
        }
        goal_required = BingoGoal(goal_data_required)
        self.assertEqual(goal_required.get_completion_percentage(), 50.0)

        # Goal with tiers
        goal_data_tiers = {
            "id": "kill_endermen",
            "name": "Enderman Slayer",
            "tiers": [500000, 1000000, 1500000, 2000000, 2500000],
            "progress": 1250000
        }
        goal_tiers = BingoGoal(goal_data_tiers)
        self.assertEqual(goal_tiers.get_completion_percentage(), 50.0)

        # Goal without progress data
        goal_data_none = {
            "id": "no_progress_goal",
            "name": "No Progress Goal"
        }
        goal_none = BingoGoal(goal_data_none)
        self.assertIsNone(goal_none.get_completion_percentage())

    def test_bingo_goal_clean_lore(self):
        """
        Test the get_clean_lore and get_clean_full_lore methods.
        """
        goal_data = {
            "id": "test_goal",
            "name": "Test Goal",
            "lore": "§7Complete §athis §7goal.",
            "fullLore": ["§7Step 1: Do something.", "§7Step 2: Do something else."]
        }
        goal = BingoGoal(goal_data)
        clean_lore = goal.get_clean_lore()
        self.assertEqual(clean_lore, "Complete this goal.")
        clean_full_lore = goal.get_clean_full_lore()
        self.assertEqual(clean_full_lore, ["Step 1: Do something.", "Step 2: Do something else."])

    def test_bingo_goal_str(self):
        """
        Test the __str__ method of the BingoGoal class.
        """
        goal_data = {
            "id": "test_goal",
            "name": "Test Goal",
            "lore": "§7Complete the test goal."
        }
        goal = BingoGoal(goal_data)
        expected_str = "Test Goal (ID: test_goal): Complete the test goal."
        self.assertEqual(str(goal), expected_str)

    @patch('requests.get')
    def test_bingo_events_error_handling(self, mock_get):
        """
        Test error handling in the BingoEvents class when the API call fails.
        """
        # Simulate an API error
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        with self.assertRaises(ConnectionError) as context:
            BingoEvents()
        self.assertIn("An error occurred: API error", str(context.exception))

    @patch('requests.get')
    def test_bingo_events_no_current_event(self, mock_get):
        """
        Test how the BingoEvents class handles absence of current event data.
        """
        # Simulate response without 'goals' key
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": True,
            "lastUpdated": 1728619119062
            # 'goals' key is missing
        }

        with self.assertRaises(ValueError) as context:
            BingoEvents()
        self.assertIn("No current bingo event data available in the response", str(context.exception))

    @patch('requests.get')
    def test_bingo_event_str(self, mock_get):
        """
        Test the __str__ method of the BingoEvent class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_events = BingoEvents()
        current_event = bingo_events.get_current_event()

        # I believe this time would be 10pm MST which should line up with the ingame day cycle
        expected_str = "Bingo Event 'October 2024' (ID: 34) from 2024-10-01 04:00:00 UTC to 2024-10-08 04:00:00 UTC"
        self.assertEqual(str(current_event), expected_str)


    @patch('requests.get')
    def test_bingo_event_timestamp_conversion(self, mock_get):
        """
        Test that event start and end times are correctly converted to UTC datetime objects.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_events = BingoEvents()
        current_event = bingo_events.get_current_event()

        expected_start = datetime.fromtimestamp(1727755200000 / 1000, tz=timezone.utc)
        expected_end = datetime.fromtimestamp(1728360000000 / 1000, tz=timezone.utc)

        self.assertEqual(current_event.start, expected_start)
        self.assertEqual(current_event.end, expected_end)


    def test_bingo_goal_missing_fields(self):
        """
        Test how the BingoGoal handles missing optional fields.
        """
        goal_data = {
            "id": "missing_fields_goal",
            "name": "Missing Fields Goal"
            # Missing 'lore', 'fullLore', 'tiers', 'progress', 'requiredAmount'
        }
        goal = BingoGoal(goal_data)
        self.assertEqual(goal.lore, '')
        self.assertEqual(goal.full_lore, [])
        self.assertEqual(goal.tiers, [])
        self.assertEqual(goal.progress, 0)
        self.assertIsNone(goal.required_amount)

if __name__ == '__main__':
    unittest.main()
