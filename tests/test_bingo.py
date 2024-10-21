import unittest
from unittest.mock import patch
import requests
from datetime import datetime

from hypixel_api_lib.Bingo import BingoEvents, BingoEvent, BingoGoal

class TestBingoEvents(unittest.TestCase):
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
                    "progress": 4367835,
                    "lore": "§7Kill §a2.5M Endermen§7.",
                    "fullLore": ["§7Kill §a2.5M Endermen§7."]
                },
                {
                    "id": "GET_SKILL_farming_5",
                    "name": "Farmer",
                    "lore": "§7Obtain level §e5§7 in the §6Farming §7Skill.",
                    "fullLore": ["§7Obtain level §e5§7 in the §6Farming §7Skill."]
                },
            ]
        }

    @patch('requests.get')
    def test_load_current_event(self, mock_get):
        """
        Test that the current bingo event is loaded correctly from the API.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_manager = BingoEvents()

        self.assertIsNotNone(bingo_manager.current_event)
        event = bingo_manager.current_event
        self.assertEqual(event.id, 34)
        self.assertEqual(event.name, "October 2024")
        self.assertEqual(event.modifier, "NORMAL")
        self.assertEqual(len(event.goals), 2)

    @patch('requests.get')
    def test_event_dates(self, mock_get):
        """
        Test that the event start and end dates are parsed correctly.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_manager = BingoEvents()
        event = bingo_manager.current_event

        expected_start = datetime.fromtimestamp(1727755200000 / 1000)
        expected_end = datetime.fromtimestamp(1728360000000 / 1000)

        self.assertEqual(event.start, expected_start)
        self.assertEqual(event.end, expected_end)

    @patch('requests.get')
    def test_get_goal_by_id(self, mock_get):
        """
        Test retrieving a goal by its ID.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_manager = BingoEvents()
        event = bingo_manager.current_event

        goal = event.get_goal_by_id("kill_endermen")
        self.assertIsNotNone(goal)
        self.assertEqual(goal.name, "Enderman Slayer")
        self.assertEqual(goal.progress, 4367835)
        self.assertEqual(goal.tiers, [500000, 1000000, 1500000, 2000000, 2500000])

        # Test a non-existent goal
        goal = event.get_goal_by_id("non_existent_goal")
        self.assertIsNone(goal)

    @patch('requests.get')
    def test_bingo_goal_methods(self, mock_get):
        """
        Test the methods in BingoGoal for handling formatting codes.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        bingo_manager = BingoEvents()
        event = bingo_manager.current_event
        goal = event.get_goal_by_id("kill_endermen")

        # Test clean_text method
        cleaned_lore = goal.get_clean_lore()
        self.assertEqual(cleaned_lore, "Kill 2.5M Endermen.")

        # Test get_clean_full_lore method
        cleaned_full_lore = goal.get_clean_full_lore()
        self.assertEqual(cleaned_full_lore, ["Kill 2.5M Endermen."])


    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """
        Test how the BingoEvents class handles API errors
        """
        # Simulate an API error
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")

        with self.assertRaises(ConnectionError) as context:
            BingoEvents()
        self.assertIn("An error occurred: API error", str(context.exception))

    @patch('requests.get')
    def test_no_current_event(self, mock_get):
        """
        Test how the BingoEvents class handles the absence of a current event.
        """
        no_event_response = {
            "success": True,
            "lastUpdated": 1728619119062,
            # 'goals' key is missing to simulate no current event
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = no_event_response

        with self.assertRaises(ValueError) as context:
            BingoEvents()
        self.assertIn("No current bingo event data available in the response", str(context.exception))

    @patch('requests.get')
    def test_invalid_response(self, mock_get):
        """
        Test how the BingoEvents class handles an invalid API response.
        """
        invalid_response = {
            "success": False,
            "cause": "Invalid API key"
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = invalid_response

        with self.assertRaises(ValueError) as context:
            BingoEvents()
        self.assertIn("No current bingo event data available in the response", str(context.exception))

    def test_get_completion_percentage(self):
        """
        Test the get_completion_percentage method of BingoGoal.
        """
        goal_data = {
            "id": "kill_endermen",
            "name": "Enderman Slayer",
            "tiers": [500000, 1000000, 1500000, 2000000, 2500000],
            "progress": 1250000,
            "lore": "§7Kill §a2.5M Endermen§7."
        }
        goal = BingoGoal(goal_data)
        percentage = goal.get_completion_percentage()
        self.assertEqual(percentage, 50.0)


if __name__ == '__main__':
    unittest.main()
