import unittest
from unittest.mock import patch
import requests

from hypixel_api_lib.Elections import Elections, Election, Candidate, Perk, Mayor

class TestElectionsComponent(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response
        self.sample_api_response = {
            'success': True,
            'lastUpdated': 1731945336382,
            'mayor': {
                'key': 'shady',
                'name': 'Scorpius',
                'perks': [
                    {'name': 'Bribe', 'description': 'If Scorpius wins and you voted for him, Mayor Scorpius will offer you coins as a token of gratitude.'},
                    {'name': 'Darker Auctions', 'description': 'Scorpius will intrude in Dark Auctions, increasing the amount of rounds to 7 and offering special items.'}
                ],
                'election': {
                    'year': 384,
                    'candidates': [
                        {
                            'key': 'events',
                            'name': 'Foxy',
                            'perks': [
                                {'name': 'Sweet Benevolence', 'description': 'Earn §a+30% §7more §dCandy§7, §cGifts §7and §6Chocolate §7from duplicate rabbits during their respective events.', 'minister': False},
                                {'name': 'A Time for Giving', 'description': "Spawn §dParty Chests §7by killing mobs during the §6Spooky Festival §7and collect §bParty Gifts §7from §cJerry's Workshop§7.", 'minister': True},
                                {'name': 'Chivalrous Carnival', 'description': 'Schedules a §eCarnival §7in the hub, active throughout the §bentire year§7.', 'minister': False},
                                {'name': 'Extra Event', 'description': 'Schedules an extra §6Spooky Festival §7event during the year.', 'minister': False}
                            ],
                            'votes': 76458
                        },
                        # ... other candidates ...
                        {
                            'key': 'shady',
                            'name': 'Scorpius',
                            'perks': [
                                {'name': 'Bribe', 'description': 'If Scorpius wins and you voted for him, Mayor Scorpius will offer you coins as a token of gratitude.', 'minister': False},
                                {'name': 'Darker Auctions', 'description': 'Scorpius will intrude in Dark Auctions, increasing the amount of rounds to 7 and offering special items.', 'minister': False}
                            ],
                            'votes': 1000534
                        }
                    ]
                }
            },
            'current': {
                'year': 385,
                'candidates': [
                    {
                        'key': 'pets',
                        'name': 'Diana',
                        'perks': [
                            {'name': 'Mythological Ritual', 'description': 'Minister Diana will sell the Griffin pet, which lets you find §2Mythological Creatures §7and tons of §eunique items§7.', 'minister': True}
                        ],
                        'votes': 65723
                    },
                    # ... other candidates ...
                    {
                        'key': 'mining',
                        'name': 'Cole',
                        'perks': [
                            {'name': 'Prospection', 'description': 'Mining minions work §a25% §7faster.', 'minister': True},
                            {'name': 'Molten Forge', 'description': 'Decrease the time it takes to §6forge §7items by §d25%§7.', 'minister': False}
                        ],
                        'votes': 11551
                    }
                ]
            }
        }

    @patch('requests.get')
    def test_elections_initialization(self, mock_get):
        """
        Test the initialization of the Elections class and loading of current election data.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        mayor = elections.get_mayor()
        current_election = elections.get_current_election()

        self.assertIsNotNone(elections.last_updated)
        self.assertIsInstance(mayor, Mayor)
        self.assertIsInstance(current_election, Election)
        self.assertEqual(mayor.name, "Scorpius")
        self.assertEqual(current_election.year, 385)
        self.assertEqual(len(current_election.candidates), len(self.sample_api_response['current']['candidates']))

    def test_perk_initialization(self):
        """
        Test the initialization of the Perk class with complete and missing data.
        """
        perk_data_complete = {
            'name': 'Test Perk',
            'description': 'This is a test perk.',
            'minister': True
        }
        perk_complete = Perk(perk_data_complete)
        self.assertEqual(perk_complete.name, 'Test Perk')
        self.assertEqual(perk_complete.description, 'This is a test perk.')
        self.assertTrue(perk_complete.minister)

        perk_data_partial = {
            'name': 'Partial Perk'
            # Missing 'description' and 'minister'
        }
        perk_partial = Perk(perk_data_partial)
        self.assertEqual(perk_partial.name, 'Partial Perk')
        self.assertEqual(perk_partial.description, '')
        self.assertIsNone(perk_partial.minister)

    def test_candidate_initialization(self):
        """
        Test the initialization of the Candidate class with complete and missing data.
        """
        candidate_data = {
            'key': 'test_candidate',
            'name': 'Test Candidate',
            'perks': [
                {'name': 'Perk 1', 'description': 'Description 1', 'minister': False},
                {'name': 'Perk 2', 'description': 'Description 2', 'minister': True}
            ],
            'votes': 12345
        }
        candidate = Candidate(candidate_data)
        self.assertEqual(candidate.key, 'test_candidate')
        self.assertEqual(candidate.name, 'Test Candidate')
        self.assertEqual(len(candidate.perks), 2)
        self.assertEqual(candidate.votes, 12345)

    @patch('requests.get')
    def test_election_candidate_retrieval(self, mock_get):
        """
        Test retrieving candidates by key and name in the Election class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        current_election = elections.get_current_election()

        # Test get_candidate_by_key
        candidate_by_key = current_election.get_candidate_by_key('pets')
        self.assertIsNotNone(candidate_by_key)
        self.assertEqual(candidate_by_key.name, 'Diana')

        # Test get_candidate_by_name
        candidate_by_name = current_election.get_candidate_by_name('Cole')
        self.assertIsNotNone(candidate_by_name)
        self.assertEqual(candidate_by_name.key, 'mining')

        # Test non-existent candidate
        self.assertIsNone(current_election.get_candidate_by_key('non_existent_key'))
        self.assertIsNone(current_election.get_candidate_by_name('Non Existent Name'))

    @patch('requests.get')
    def test_election_candidates_by_votes(self, mock_get):
        """
        Test the get_candidates_by_votes method of the Election class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        current_election = elections.get_current_election()

        sorted_candidates = current_election.get_candidates_by_votes()
        votes_list = [candidate.votes for candidate in sorted_candidates]

        # Check if the votes_list is sorted in descending order
        self.assertEqual(votes_list, sorted(votes_list, reverse=True))

    @patch('requests.get')
    def test_mayor_ministers(self, mock_get):
        """
        Test retrieving ministers from the Mayor class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        mayor = elections.get_mayor()
        ministers = mayor.get_ministers()

        self.assertIsNotNone(ministers)
        # In this sample data, there are ministers
        self.assertGreater(len(ministers), 0)

        # Verify that ministers are not the mayor and have minister perks
        for candidate, perks in ministers:
            self.assertNotEqual(candidate.key, mayor.key)
            self.assertTrue(any(perk.minister for perk in perks))

    def test_perk_str(self):
        """
        Test the __str__ method of the Perk class.
        """
        perk_data = {
            'name': 'Test Perk',
            'description': 'This is a test perk.',
            'minister': True
        }
        perk = Perk(perk_data)
        expected_str = 'Test Perk: This is a test perk. (Minister: True)'
        self.assertEqual(str(perk), expected_str)

    def test_candidate_str(self):
        """
        Test the __str__ method of the Candidate class.
        """
        candidate_data = {
            'key': 'test_candidate',
            'name': 'Test Candidate',
            'votes': 12345
        }
        candidate = Candidate(candidate_data)
        expected_str = 'Candidate Test Candidate (Key: test_candidate): 12345 votes'
        self.assertEqual(str(candidate), expected_str)

    @patch('requests.get')
    def test_elections_error_handling(self, mock_get):
        """
        Test error handling in the Elections class when the API call fails.
        """
        # Simulate an API error
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        with self.assertRaises(ConnectionError) as context:
            Elections()
        self.assertIn("An error occurred: API error", str(context.exception))

    @patch('requests.get')
    def test_elections_no_success(self, mock_get):
        """
        Test how the Elections class handles a response where 'success' is False.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'success': False,
            'error': 'Invalid API Key'
        }

        with self.assertRaises(ValueError) as context:
            Elections()
        self.assertIn("Failed to fetch elections data", str(context.exception))

    @patch('requests.get')
    def test_election_get_ministers(self, mock_get):
        """
        Test the get_ministers method of the Election class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        mayor = elections.get_mayor()
        election = mayor.election

        ministers = election.get_ministers(mayor.key)
        self.assertIsNotNone(ministers)
        self.assertGreater(len(ministers), 0)

        for candidate, perks in ministers:
            self.assertNotEqual(candidate.key, mayor.key)
            self.assertTrue(any(perk.minister for perk in perks))

    @patch('requests.get')
    def test_elections_str(self, mock_get):
        """
        Test the __str__ method of the Elections class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        expected_str = f"{str(elections.get_mayor())}\n{str(elections.get_current_election())}"
        self.assertEqual(str(elections), expected_str)

    @patch('requests.get')
    def test_mayor_str(self, mock_get):
        """
        Test the __str__ method of the Mayor class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        mayor = elections.get_mayor()
        expected_str = 'Mayor Scorpius (Key: shady)'
        self.assertEqual(str(mayor), expected_str)

    @patch('requests.get')
    def test_election_str(self, mock_get):
        """
        Test the __str__ method of the Election class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_api_response

        elections = Elections()
        election = elections.get_current_election()
        expected_str = f"Election Year 385 with {len(election.candidates)} candidates"
        self.assertEqual(str(election), expected_str)

    @patch('requests.get')
    def test_candidate_missing_fields(self, mock_get):
        """
        Test how the Candidate class handles missing optional fields.
        """
        candidate_data = {
            'key': 'missing_fields_candidate',
            'name': 'Missing Fields Candidate'
            # Missing 'perks' and 'votes'
        }
        candidate = Candidate(candidate_data)
        self.assertEqual(candidate.key, 'missing_fields_candidate')
        self.assertEqual(candidate.name, 'Missing Fields Candidate')
        self.assertEqual(candidate.perks, [])
        self.assertEqual(candidate.votes, 0)

    @patch('requests.get')
    def test_perk_missing_fields(self, mock_get):
        """
        Test how the Perk class handles missing optional fields.
        """
        perk_data = {
            'name': 'Missing Fields Perk'
            # Missing 'description' and 'minister'
        }
        perk = Perk(perk_data)
        self.assertEqual(perk.name, 'Missing Fields Perk')
        self.assertEqual(perk.description, '')
        self.assertIsNone(perk.minister)

    @patch('requests.get')
    def test_election_no_candidates(self, mock_get):
        """
        Test how the Election class handles when there are no candidates.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'success': True,
            'lastUpdated': 1731945336382,
            'current': {
                'year': 385,
                'candidates': []
            }
        }

        elections = Elections()
        current_election = elections.get_current_election()
        self.assertIsNotNone(current_election)
        self.assertEqual(current_election.year, 385)
        self.assertEqual(len(current_election.candidates), 0)

    @patch('requests.get')
    def test_mayor_no_election(self, mock_get):
        """
        Test how the Mayor class handles when there is no election data.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'success': True,
            'lastUpdated': 1731945336382,
            'mayor': {
                'key': 'shady',
                'name': 'Scorpius',
                'perks': [
                    {'name': 'Bribe', 'description': 'If Scorpius wins and you voted for him, Mayor Scorpius will offer you coins as a token of gratitude.'},
                    {'name': 'Darker Auctions', 'description': 'Scorpius will intrude in Dark Auctions, increasing the amount of rounds to 7 and offering special items.'}
                ]
                # 'election' key is missing
            }
        }

        elections = Elections()
        mayor = elections.get_mayor()
        self.assertIsNotNone(mayor)
        self.assertIsNone(mayor.election)
        ministers = mayor.get_ministers()
        self.assertEqual(ministers, [])

if __name__ == '__main__':
    unittest.main()
