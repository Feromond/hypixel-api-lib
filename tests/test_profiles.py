import unittest
from unittest.mock import patch
import requests
from datetime import datetime

from hypixel_api_lib.Profiles import *

class TestSkyBlockProfiles(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response
        self.sample_profile_response = {
            "success": True,
            "profile": {
                "profile_id": "1234567890abcdef",
                "members": {
                    "uuid1": {
                        "uuid": "uuid1",
                        "rift": {"rift_data": "some_data"},
                        "garden_player_data": {"some": "data"},
                        # ... other data ...
                    },
                    "uuid2": {
                        "uuid": "uuid2",
                        "rift": {"rift_data": "some_data"},
                        "garden_player_data": {"some": "data"},
                        # ... other data ...
                    }
                },
                "community_upgrades": {
                    "currently_upgrading": {
                        "upgrade": "upgrade_name",
                        "tier": 1,
                        "started_ms": 1630000000000,
                        "started_by": "uuid1",
                        "claimed_ms": 1630003600000,
                        "claimed_by": "uuid1",
                        "fasttracked": False
                    },
                    "upgrade_states": [
                        {
                            "upgrade": "upgrade_name_prev",
                            "tier": 0,
                            "started_ms": 1620000000000,
                            "started_by": "uuid2",
                            "claimed_ms": 1620003600000,
                            "claimed_by": "uuid2",
                            "fasttracked": True
                        }
                    ]
                },
                "banking": {
                    "balance": 1000.0,
                    "transactions": [
                        {
                            "timestamp": 1630000000000,
                            "action": "DEPOSIT",
                            "initiator_name": "Player1",
                            "amount": 500.0
                        },
                        {
                            "timestamp": 1630003600000,
                            "action": "WITHDRAW",
                            "initiator_name": "Player2",
                            "amount": 200.0
                        }
                    ]
                },
                "cute_name": "MyProfile",
                "game_mode": "ironman"
            }
        }
        self.dummy_api_key = 'DUMMY_API_KEY'

    def test_community_upgrade_state(self):
        """
        Test the initialization of CommunityUpgradeState.
        """
        sample_data = {
            "upgrade": "upgrade_name",
            "tier": 1,
            "started_ms": 1630000000000,
            "started_by": "uuid1",
            "claimed_ms": 1630003600000,
            "claimed_by": "uuid1",
            "fasttracked": False
        }
        upgrade_state = CommunityUpgradeState(sample_data)
        self.assertEqual(upgrade_state.upgrade, "upgrade_name")
        self.assertEqual(upgrade_state.tier, 1)
        self.assertEqual(upgrade_state.started_by, "uuid1")
        self.assertEqual(upgrade_state.claimed_by, "uuid1")
        self.assertFalse(upgrade_state.fasttracked)
        self.assertIsInstance(upgrade_state.started_ms, datetime)
        self.assertIsInstance(upgrade_state.claimed_ms, datetime)
        self.assertEqual(upgrade_state.started_ms.timestamp(), 1630000000.0)
        self.assertEqual(upgrade_state.claimed_ms.timestamp(), 1630003600.0)

    def test_community_upgrades(self):
        """
        Test the initialization of CommunityUpgrades.
        """
        sample_data = {
            "currently_upgrading": {
                "upgrade": "upgrade_name",
                "tier": 1,
                "started_ms": 1630000000000,
                "started_by": "uuid1",
                "claimed_ms": 1630003600000,
                "claimed_by": "uuid1",
                "fasttracked": False
            },
            "upgrade_states": [
                {
                    "upgrade": "upgrade_name_prev",
                    "tier": 0,
                    "started_ms": 1620000000000,
                    "started_by": "uuid2",
                    "claimed_ms": 1620003600000,
                    "claimed_by": "uuid2",
                    "fasttracked": True
                }
            ]
        }
        community_upgrades = CommunityUpgrades(sample_data)
        self.assertIsNotNone(community_upgrades.currently_upgrading)
        self.assertEqual(len(community_upgrades.upgrade_states), 1)
        self.assertIsInstance(community_upgrades.currently_upgrading, CommunityUpgradeState)
        self.assertIsInstance(community_upgrades.upgrade_states[0], CommunityUpgradeState)

    def test_bank_transaction(self):
        """
        Test the initialization of BankTransaction.
        """
        sample_data = {
            "timestamp": 1630000000000,
            "action": "DEPOSIT",
            "initiator_name": "Player1",
            "amount": 500.0
        }
        transaction = BankTransaction(sample_data)
        self.assertEqual(transaction.action, "DEPOSIT")
        self.assertEqual(transaction.initiator_name, "Player1")
        self.assertEqual(transaction.amount, 500.0)
        self.assertIsInstance(transaction.timestamp, datetime)
        self.assertEqual(transaction.timestamp.timestamp(), 1630000000.0)

    def test_banking(self):
        """
        Test the initialization of Banking.
        """
        sample_data = {
            "balance": 1000.0,
            "transactions": [
                {
                    "timestamp": 1630000000000,
                    "action": "DEPOSIT",
                    "initiator_name": "Player1",
                    "amount": 500.0
                },
                {
                    "timestamp": 1630003600000,
                    "action": "WITHDRAW",
                    "initiator_name": "Player2",
                    "amount": 200.0
                }
            ]
        }
        banking = Banking(sample_data)
        self.assertEqual(banking.balance, 1000.0)
        self.assertEqual(len(banking.transactions), 2)
        self.assertIsInstance(banking.transactions[0], BankTransaction)
        self.assertEqual(banking.transactions[0].action, "DEPOSIT")
        self.assertEqual(banking.transactions[1].action, "WITHDRAW")

    def test_deletion_notice(self):
        """
        Test the initialization of DeletionNotice.
        """
        sample_data = {
            "timestamp": 1630000000000
        }
        deletion_notice = DeletionNotice(sample_data)
        self.assertIsInstance(deletion_notice.timestamp, datetime)
        self.assertEqual(deletion_notice.timestamp.timestamp(), 1630000000.0)

    def test_skyblock_profile_member(self):
        """
        Test the initialization of SkyBlockProfileMember.
        """
        sample_data = {
            "uuid": "uuid1",
            "rift": {"rift_data": "some_data"},
            "garden_player_data": {"some": "data"},
            "profile": {},
            "player_id": "player1"
            # ... other data ...
        }
        member = SkyBlockProfileMember(uuid="uuid1", data=sample_data)
        self.assertEqual(member.uuid, "uuid1")
        self.assertEqual(member.rift, {"rift_data": "some_data"})
        self.assertEqual(member.garden_player_data, {"some": "data"})
        self.assertEqual(member.player_id, "player1")
        self.assertFalse(member.is_member_deleted())

    def test_skyblock_profile_methods(self):
        """
        Test methods in SkyBlockProfile class.
        """
        sample_profile = SkyBlockProfile(self.sample_profile_response['profile'])
        member_uuids = sample_profile.list_member_uuids()
        self.assertEqual(len(member_uuids), 2)
        self.assertIn("uuid1", member_uuids)
        member = sample_profile.get_member("uuid1")
        self.assertIsNotNone(member)
        self.assertEqual(member.uuid, "uuid1")
        # Test __str__ method
        profile_str = str(sample_profile)
        self.assertIn("SkyBlockProfile ID: 1234567890abcdef", profile_str)
        self.assertIn("Members: ['uuid1', 'uuid2']", profile_str)

    @patch('requests.get')
    def test_get_profile(self, mock_get):
        """
        Test that a profile is loaded correctly from the API.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_profile_response

        profiles_manager = SkyBlockProfiles(api_key=self.dummy_api_key)
        profile_id = "1234567890abcdef"
        profile = profiles_manager.get_profile(profile_id=profile_id)
        
        self.assertIsNotNone(profile)
        self.assertEqual(profile.profile_id, profile_id)
        self.assertEqual(len(profile.members), 2)
        self.assertIsInstance(profile.community_upgrades, CommunityUpgrades)
        self.assertIsInstance(profile.banking, Banking)
        self.assertEqual(profile.cute_name, "MyProfile")
        self.assertEqual(profile.game_mode, "ironman")

    @patch('requests.get')
    def test_get_profiles_by_player_uuid(self, mock_get):
        """
        Test fetching profiles by player UUID.
        """
        sample_profiles_response = {
            "success": True,
            "profiles": [
                {
                    "profile_id": "profile1",
                    "members": {
                        "uuid1": {"some": "data"},
                        "uuid2": {"some": "data"}
                    },
                    "cute_name": "Profile1",
                    "selected": True,
                    "game_mode": "ironman"
                },
                {
                    "profile_id": "profile2",
                    "members": {
                        "uuid1": {"some": "data"},
                        "uuid3": {"some": "data"}
                    },
                    "cute_name": "Profile2",
                    "selected": False,
                    "game_mode": "bingo"
                }
            ]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_profiles_response

        profiles_manager = SkyBlockProfiles(api_key=self.dummy_api_key)
        player_uuid = "uuid1"
        profiles = profiles_manager.get_profiles_by_player_uuid(player_uuid=player_uuid)
        self.assertEqual(len(profiles), 2)
        self.assertTrue(any(profile.selected for profile in profiles))
        selected_profile = profiles_manager.get_selected_profile_by_player_uuid(player_uuid=player_uuid)
        self.assertIsNotNone(selected_profile)
        self.assertEqual(selected_profile.cute_name, "Profile1")
        self.assertEqual(selected_profile.game_mode, "ironman")

    @patch('requests.get')
    def test_invalid_api_key(self, mock_get):
        """
        Test handling of invalid API key (403 error).
        """
        # Create a mock response object with status_code 403
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 403
        http_error = requests.exceptions.HTTPError("403 Client Error: Forbidden for url", response=mock_response)

        mock_get.return_value.raise_for_status.side_effect = http_error

        profiles_manager = SkyBlockProfiles(api_key=self.dummy_api_key)
        with self.assertRaises(PermissionError) as context:
            profile = profiles_manager.get_profile(profile_id="some_profile_id")

        self.assertIn("Access forbidden: Invalid API key.", str(context.exception))


    @patch('requests.get')
    def test_rate_limiting(self, mock_get):
        """
        Test handling of rate limiting (429 error).
        """
        # Create a mock response object with status_code 429
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 429
        http_error = requests.exceptions.HTTPError("429 Client Error: Too Many Requests for url", response=mock_response)

        mock_get.return_value.raise_for_status.side_effect = http_error

        profiles_manager = SkyBlockProfiles(api_key=self.dummy_api_key)
        with self.assertRaises(ConnectionError) as context:
            profile = profiles_manager.get_profile(profile_id="some_profile_id")

        self.assertIn("Request limit reached: Throttling in effect.", str(context.exception))


    @patch('requests.get')
    def test_no_profile_data(self, mock_get):
        """
        Test handling when no profile data is available in the response.
        """
        sample_response = {
            "success": True,
            "profile": None
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response

        profiles_manager = SkyBlockProfiles(api_key=self.dummy_api_key)
        with self.assertRaises(ValueError) as context:
            profile = profiles_manager.get_profile(profile_id="some_profile_id")

        self.assertIn("No profile data available in the response", str(context.exception))

if __name__ == '__main__':
    unittest.main()
