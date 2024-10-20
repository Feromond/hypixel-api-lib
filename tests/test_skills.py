import unittest
from unittest.mock import patch
import requests

from hypixel_api_lib.Skills import Skills, Skill, SkillLevel

class TestSkills(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response
        self.sample_api_response = {
            "success": True,
            "lastUpdated": 0,
            "skills": {
                "FARMING": {
                    "name": "Farming",
                    "description": "Increases your farming abilities.",
                    "maxLevel": 60,
                    "levels": [
                        {"level": 1, "totalExpRequired": 50.0, "unlocks": ["Unlocks the Wheat Minion I recipe"]},
                        {"level": 2, "totalExpRequired": 125.0, "unlocks": ["+2 Health"]},
                    ]
                },
                "MINING": {
                    "name": "Mining",
                    "description": "Increases your mining abilities.",
                    "maxLevel": 60,
                    "levels": [
                        {"level": 1, "totalExpRequired": 50.0, "unlocks": ["Unlocks the Coal Minion I recipe"]},
                        {"level": 2, "totalExpRequired": 175.0, "unlocks": ["+1 Defense"]},
                    ]
                },
                "COMBAT": {
                    "name": "Combat",
                    "description": "Increases your combat abilities.",
                    "maxLevel": 50,
                    "levels": [
                        {"level": 1, "totalExpRequired": 50.0, "unlocks": ["Unlocks the Zombie Minion I recipe"]},
                        {"level": 2, "totalExpRequired": 150.0, "unlocks": ["+1% Crit Chance"]},
                    ]
                }
            }
        }

    @patch('requests.get')
    def test_load_skills(self, mock_get):
        """
        Test that skills are loaded correctly from the API.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        skills_manager = Skills()

        self.assertIsNotNone(skills_manager.skills)
        self.assertEqual(len(skills_manager.skills), 3)
        self.assertIn("FARMING", skills_manager.skills)
        self.assertIn("MINING", skills_manager.skills)

    @patch('requests.get')
    def test_get_skill_existing(self, mock_get):
        """
        Test retrieving an existing skill by name.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        skills_manager = Skills()

        skill = skills_manager.get_skill("Farming")
        self.assertIsInstance(skill, Skill)
        self.assertEqual(skill.name, "Farming")
        self.assertEqual(skill.description, "Increases your farming abilities.")
        self.assertEqual(skill.max_level, 60)
        self.assertEqual(len(skill.levels), 2)  # Adjust based on sample data

    @patch('requests.get')
    def test_get_skill_nonexistent(self, mock_get):
        """
        Test retrieving a skill that does not exist (in the mock data).
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        skills_manager = Skills()

        skill = skills_manager.get_skill("Fishing")
        self.assertIsInstance(skill, str)
        self.assertEqual(skill, "Skill 'Fishing' not found.")

    @patch('requests.get')
    def test_get_skills_by_max_level(self, mock_get):
        """
        Test retrieving skills by their maximum level.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        skills_manager = Skills()

        skills_max_60 = skills_manager.get_skills_by_max_level(60)
        self.assertEqual(len(skills_max_60), 2)
        self.assertIn("FARMING", skills_max_60)
        self.assertIn("MINING", skills_max_60)

        skills_max_50 = skills_manager.get_skills_by_max_level(50)
        self.assertEqual(len(skills_max_50), 1)
        self.assertIn("COMBAT", skills_max_50)

    @patch('requests.get')
    def test_list_skill_names(self, mock_get):
        """
        Test listing all skill names.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        skills_manager = Skills()

        skill_names = skills_manager.list_skill_names()
        expected_names = ["Farming", "Mining", "Combat"]
        self.assertEqual(sorted(skill_names), sorted(expected_names))

    @patch('requests.get')
    def test_get_level_existing(self, mock_get):
        """
        Test retrieving a specific level of a skill.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        skills_manager = Skills()

        skill = skills_manager.get_skill("Farming")
        level = skill.get_level(1)
        self.assertIsInstance(level, SkillLevel)
        self.assertEqual(level.level, 1)
        self.assertEqual(level.total_exp_required, 50.0)
        self.assertEqual(level.unlocks, ["Unlocks the Wheat Minion I recipe"])

    @patch('requests.get')
    def test_get_level_nonexistent(self, mock_get):
        """
        Test retrieving a level that does not exist in a skill.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        skills_manager = Skills()

        skill = skills_manager.get_skill("Mining")
        level = skill.get_level(100)  # level 100 does not exist
        self.assertIsNone(level)

    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """
        Test the Skills class's handling of API errors.
        """
        # Simulate an API error
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("API error")

        with self.assertRaises(ConnectionError) as context:
            Skills()
        self.assertIn("An error occurred: API error", str(context.exception))


    @patch('requests.get')
    def test_empty_skills_list(self, mock_get):
        """
        Test how the Skills class handles an empty skills list.
        """
        empty_response = {
            "success": True,
            "lastUpdated": 0,
            "skills": {}
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = empty_response

        with self.assertRaises(ValueError) as context:
            Skills()

        self.assertIn("No skills data available in the response", str(context.exception))

    @patch('requests.get')
    def test_skill_with_missing_fields(self, mock_get):
        """
        Test handling of skills with missing optional fields.
        """
        sample_response_with_missing_fields = {
            "success": True,
            "lastUpdated": 0,
            "skills": {
                "MAGIC": {
                    # 'name' is intentionally missing
                    "description": "Increases your magic abilities.",
                    "maxLevel": 50,
                    "levels": [
                        {"level": 1, "totalExpRequired": 50.0, "unlocks": ["+5 Mana"]},
                        {"level": 2, "totalExpRequired": 150.0, "unlocks": ["+5 Mana"]},
                    ]
                }
            }
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response_with_missing_fields

        with self.assertRaises(KeyError):
            Skills()

if __name__ == '__main__':
    unittest.main()
