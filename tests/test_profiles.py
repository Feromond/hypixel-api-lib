import unittest
from unittest.mock import patch
import requests
from datetime import datetime
import base64
import zlib
from io import BytesIO
import gzip

from hypixel_api_lib.Profiles import *
from hypixel_api_lib.member.ProfileMember import *
from hypixel_api_lib.member.PlayerData import *
from hypixel_api_lib.member.GlacitePlayerData import *
from hypixel_api_lib.member.Events import *
from hypixel_api_lib.member.GardenPlayerData import *
from hypixel_api_lib.member.PetsData import *
from hypixel_api_lib.member.Rift import *


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

class TestSkyBlockProfileMember(unittest.TestCase):
    
    """
    TODO: This test needs to be fully remade eventually 
    to properly test the member once all the sub components are completed
    but for now it just exists to test deletion and some other small basic details.
    """

    def setUp(self):
        self.sample_member_data = {
            "uuid": "uuid1",
            "rift": {"rift_data": "some_data"},
            "profile": {
                "deletion_notice": {"timestamp": 1630000000000}
            },
            "player_id": "player1"
        }

    def test_skyblock_profile_member_initialization(self):
        """
        Test the initialization of SkyBlockProfileMember.
        """
        member = SkyBlockProfileMember(uuid="uuid1", data=self.sample_member_data)
        self.assertEqual(member.uuid, "uuid1")
        self.assertEqual(member.player_id, "player1")

    def test_deletion_notice(self):
        """
        Test the initialization of DeletionNotice in SkyBlockProfileMember.
        """
        member = SkyBlockProfileMember(uuid="uuid1", data=self.sample_member_data)
        self.assertIsInstance(member.deleted_timestamp, DeletionNotice)
        self.assertIsInstance(member.deleted_timestamp.timestamp, datetime)
        self.assertEqual(member.deleted_timestamp.timestamp.timestamp(), 1630000000.0)

    def test_is_member_deleted(self):
        """
        Test the is_member_deleted method in SkyBlockProfileMember.
        """
        member = SkyBlockProfileMember(uuid="uuid1", data=self.sample_member_data)
        self.assertTrue(member.is_member_deleted())

    def test_str_representation(self):
        """
        Test the string representation of SkyBlockProfileMember.
        """
        member = SkyBlockProfileMember(uuid="uuid1", data=self.sample_member_data)
        self.assertIn("SkyBlockProfileMember UUID: uuid1", str(member))

class TestPlayerData(unittest.TestCase):

    def setUp(self):
        self.sample_player_data = {
            "visited_zones": ["zone1", "zone2", "zone3"],
            "last_death": 1630000000000,
            "perks": {
                "strength": 5,
                "agility": 3
            },
            "active_effects": ["speed", "strength"],
            "paused_effects": ["regeneration"],
            "temp_stat_buffs": ["extra_damage"],
            "death_count": 10,
            "disabled_potion_effects": ["poison"],
            "achievement_spawned_island_types": ["main", "island"],
            "visited_modes": ["hardcore", "normal"],
            "unlocked_coll_tiers": ["tier1", "tier2"],
            "crafted_generators": ["gen1", "gen2"],
            "fastest_target_practice": 12.34,
            "fishing_treasure_caught": 5,
            "experience": {
                "combat": 12345.67,
                "mining": 9876.54
            }
        }

    def test_player_data_initialization(self):
        """
        Test the initialization of PlayerData and its attributes.
        """
        player_data = PlayerData(self.sample_player_data)
        
        # Test basic attributes
        self.assertEqual(player_data.visited_zones, ["zone1", "zone2", "zone3"])
        self.assertEqual(player_data.death_count, 10)
        self.assertEqual(player_data.active_effects, ["speed", "strength"])
        self.assertEqual(player_data.paused_effects, ["regeneration"])
        self.assertEqual(player_data.temp_stat_buffs, ["extra_damage"])
        self.assertEqual(player_data.disabled_potion_effects, ["poison"])
        self.assertEqual(player_data.achievement_spawned_island_types, ["main", "island"])
        self.assertEqual(player_data.visited_modes, ["hardcore", "normal"])
        self.assertEqual(player_data.unlocked_coll_tiers, ["tier1", "tier2"])
        self.assertEqual(player_data.crafted_generators, ["gen1", "gen2"])
        self.assertEqual(player_data.fastest_target_practice, 12.34)
        self.assertEqual(player_data.fishing_treasure_caught, 5)

    def test_last_death_timestamp_conversion(self):
        """
        Test conversion of last_death timestamp to datetime.
        """
        player_data = PlayerData(self.sample_player_data)
        self.assertIsInstance(player_data.last_death, datetime)
        self.assertEqual(player_data.last_death.timestamp(), 1630000000.0)

    def test_perks_parsing(self):
        """
        Test parsing of perks into Perk objects.
        """
        player_data = PlayerData(self.sample_player_data)
        self.assertEqual(len(player_data.perks), 2)
        self.assertIsInstance(player_data.perks[0], Perk)
        self.assertEqual(player_data.perks[0].name, "strength")
        self.assertEqual(player_data.perks[0].level, 5)
        self.assertEqual(player_data.perks[1].name, "agility")
        self.assertEqual(player_data.perks[1].level, 3)

    def test_experience_parsing(self):
        """
        Test parsing of experience into SkillExperience objects.
        """
        player_data = PlayerData(self.sample_player_data)
        self.assertEqual(len(player_data.experience), 2)
        self.assertIsInstance(player_data.experience[0], SkillExperience)
        self.assertEqual(player_data.experience[0].skill_name, "combat")
        self.assertEqual(player_data.experience[0].experience, 12345.67)
        self.assertEqual(player_data.experience[1].skill_name, "mining")
        self.assertEqual(player_data.experience[1].experience, 9876.54)

    def test_str_representation(self):
        """
        Test the string representation of PlayerData.
        """
        player_data = PlayerData(self.sample_player_data)
        player_data_str = str(player_data)
        self.assertIn("PlayerData(Deaths: 10", player_data_str)
        self.assertIn("Visited Zones: 3", player_data_str)
        self.assertIn("Experience: [combat: 12345.67 XP", player_data_str)

class TestGlacitePlayerData(unittest.TestCase):

    def setUp(self):
        self.sample_glacite_data = {
            "fossils_donated": ["fossil1", "fossil2"],
            "fossil_dust": 150.75,
            "corpses_looted": {"zombie": 5, "skeleton": 3},
            "mineshafts_entered": 12
        }

    def test_glacite_player_data_initialization(self):
        """
        Test the initialization of GlacitePlayerData and its attributes.
        """
        glacite_data = GlacitePlayerData(self.sample_glacite_data)
        
        self.assertEqual(glacite_data.fossils_donated, ["fossil1", "fossil2"])
        self.assertEqual(glacite_data.fossil_dust, 150.75)
        self.assertEqual(glacite_data.corpses_looted, {"zombie": 5, "skeleton": 3})
        self.assertEqual(glacite_data.mineshafts_entered, 12)

    def test_default_values(self):
        """
        Test that GlacitePlayerData uses default values when data is missing.
        """
        glacite_data = GlacitePlayerData({})
        self.assertEqual(glacite_data.fossils_donated, [])
        self.assertEqual(glacite_data.fossil_dust, 0.0)
        self.assertEqual(glacite_data.corpses_looted, {})
        self.assertEqual(glacite_data.mineshafts_entered, 0)

    def test_str_representation(self):
        """
        Test the string representation of GlacitePlayerData.
        """
        glacite_data = GlacitePlayerData(self.sample_glacite_data)
        glacite_data_str = str(glacite_data)
        self.assertIn("Fossils Donated: ['fossil1', 'fossil2']", glacite_data_str)
        self.assertIn("Fossil Dust: 150.75", glacite_data_str)
        self.assertIn("Corpses Looted: {'zombie': 5, 'skeleton': 3}", glacite_data_str)
        self.assertIn("Mineshafts Entered: 12", glacite_data_str)

class TestEasterEvent(unittest.TestCase):

    def setUp(self):
        self.sample_easter_data = {
            "chocolate": 100,
            "chocolate_since_prestige": 50,
            "total_chocolate": 150,
            "rabbits": {
                "collected_eggs": {"breakfast": 10, "lunch": 5},
                "collected_locations": {"location1": 2, "location2": 3},
                "rabbit1": 3,
                "rabbit2": 5
            },
            "shop": {
                "year": 2021,
                "rabbits": ["rabbit1", "rabbit2"],
                "rabbits_purchased": ["rabbit1"],
                "chocolate_spent": 25,
                "cocoa_fortune_upgrades": 2
            },
            "employees": {
                "employee1": 3,
                "employee2": 5
            },
            "last_viewed_chocolate_factory": 1630000000000,
            "rabbit_barn_capacity_level": 4,
            "chocolate_level": 10,
            "time_tower": {
                "charges": 3,
                "activation_time": 1630000000000,
                "level": 5,
                "last_charge_time": 1630003600000
            },
            "rabbit_sort": "name",
            "rabbit_filter": "active",
            "el_dorado_progress": 80,
            "chocolate_multiplier_upgrades": 3,
            "click_upgrades": 4,
            "rabbit_rarity_upgrades": 2
        }

    def test_easter_event_initialization(self):
        """
        Test initialization of EasterEvent and its attributes.
        """
        easter_event = EasterEvent(self.sample_easter_data)
        
        # Test basic attributes
        self.assertEqual(easter_event.chocolate, 100)
        self.assertEqual(easter_event.chocolate_since_prestige, 50)
        self.assertEqual(easter_event.total_chocolate, 150)
        self.assertEqual(easter_event.rabbit_barn_capacity_level, 4)
        self.assertEqual(easter_event.chocolate_level, 10)
        self.assertEqual(easter_event.rabbit_sort, "name")
        self.assertEqual(easter_event.rabbit_filter, "active")
        self.assertEqual(easter_event.el_dorado_progress, 80)
        self.assertEqual(easter_event.chocolate_multiplier_upgrades, 3)
        self.assertEqual(easter_event.click_upgrades, 4)
        self.assertEqual(easter_event.rabbit_rarity_upgrades, 2)

    def test_easter_time_tower_initialization(self):
        """
        Test initialization of EasterTimeTower within EasterEvent.
        """
        easter_event = EasterEvent(self.sample_easter_data)
        time_tower = easter_event.time_tower
        self.assertIsInstance(time_tower, EasterTimeTower)
        self.assertEqual(time_tower.charges, 3)
        self.assertEqual(time_tower.level, 5)
        self.assertIsInstance(time_tower.activation_time, datetime)
        self.assertEqual(time_tower.activation_time.timestamp(), 1630000000.0)
        self.assertIsInstance(time_tower.last_charge_time, datetime)
        self.assertEqual(time_tower.last_charge_time.timestamp(), 1630003600.0)

    def test_easter_employees_initialization(self):
        """
        Test initialization of EasterEmployees within EasterEvent.
        """
        easter_event = EasterEvent(self.sample_easter_data)
        employees = easter_event.employees
        self.assertIsInstance(employees, EasterEmployees)
        self.assertEqual(employees.employee_levels, {"employee1": 3, "employee2": 5})

    def test_easter_shop_initialization(self):
        """
        Test initialization of EasterShop within EasterEvent.
        """
        easter_event = EasterEvent(self.sample_easter_data)
        shop = easter_event.shop
        self.assertIsInstance(shop, EasterShop)
        self.assertEqual(shop.year, 2021)
        self.assertEqual(shop.rabbits, ["rabbit1", "rabbit2"])
        self.assertEqual(shop.rabbits_purchased, ["rabbit1"])
        self.assertEqual(shop.chocolate_spent, 25)
        self.assertEqual(shop.cocoa_fortune_upgrades, 2)

    def test_easter_rabbits_data_initialization(self):
        """
        Test initialization of EasterRabbitsData within EasterEvent.
        """
        easter_event = EasterEvent(self.sample_easter_data)
        rabbits_data = easter_event.rabbits_data
        self.assertIsInstance(rabbits_data, EasterRabbitsData)
        self.assertEqual(rabbits_data.collected_eggs, {"breakfast": 10, "lunch": 5})
        self.assertEqual(rabbits_data.collected_locations, {"location1": 2, "location2": 3})
        self.assertEqual(rabbits_data.rabbit_counts, {"rabbit1": 3, "rabbit2": 5})

    def test_str_representation(self):
        """
        Test the string representation of the main components.
        """
        easter_event = EasterEvent(self.sample_easter_data)
        event_str = str(easter_event)
        self.assertIn("Chocolate: 100", event_str)
        self.assertIn("Total Chocolate: 150", event_str)
        self.assertIn("TimeTower:", event_str)
        self.assertIn("RabbitsData:", event_str)
        self.assertIn("Shop:", event_str)
        self.assertIn("Employees:", event_str)

class TestGardenPlayerData(unittest.TestCase):

    def setUp(self):
        self.sample_garden_data = {
            "copper": 7961,
            "larva_consumed": 5
        }

    def test_garden_player_data_initialization(self):
        """
        Test the initialization of GardenPlayerData and its attributes.
        """
        garden_data = GardenPlayerData(self.sample_garden_data)
        
        self.assertEqual(garden_data.copper, 7961)
        self.assertEqual(garden_data.larva_consumed, 5)

    def test_default_values(self):
        """
        Test that GardenPlayerData uses default values when data is missing.
        """
        garden_data = GardenPlayerData({})
        self.assertEqual(garden_data.copper, 0)
        self.assertEqual(garden_data.larva_consumed, 0)

    def test_str_representation(self):
        """
        Test the string representation of GardenPlayerData.
        """
        garden_data = GardenPlayerData(self.sample_garden_data)
        garden_data_str = str(garden_data)
        self.assertIn("Copper: 7961", garden_data_str)
        self.assertIn("Larva Consumed: 5", garden_data_str)

class TestPetsData(unittest.TestCase):

    def setUp(self):
        self.sample_pets_data = {
            "pet_care": {
                "coins_spent": 89614810.07,
                "pet_types_sacrificed": ["ENDERMAN", "BLACK_CAT"]
            },
            "autopet": {
                "rules_limit": 16,
                "rules": [
                    {
                        "uuid": "rule1",
                        "id": "EQUIP_WARDROBE_SLOT",
                        "name": "Equip Golden Dragon",
                        "uniqueId": "unique_rule_id1",
                        "exceptions": [{"id": "IS_IN_ISLAND", "data": {"island": "mining_3"}}],
                        "disabled": False,
                        "data": {"slot": "4"}
                    }
                ],
                "migrated": True,
                "migrated_2": False
            },
            "pets": [
                {
                    "uuid": "pet1",
                    "uniqueId": "unique_pet_id1",
                    "type": "SILVERFISH",
                    "exp": 45163824.71,
                    "active": False,
                    "tier": "LEGENDARY",
                    "heldItem": "PET_ITEM_MINING_SKILL_BOOST_RARE",
                    "candyUsed": 0,
                    "skin": None
                },
                {
                    "uuid": "pet2",
                    "uniqueId": "unique_pet_id2",
                    "type": "BEE",
                    "exp": 5297.31,
                    "active": True,
                    "tier": "RARE",
                    "heldItem": None,
                    "candyUsed": 2,
                    "skin": "BEE_SKIN"
                }
            ]
        }

    def test_pet_care_data_initialization(self):
        """
        Test initialization of PetCareData.
        """
        pet_care_data = PetCareData(self.sample_pets_data["pet_care"])
        self.assertEqual(pet_care_data.coins_spent, 89614810.07)
        self.assertEqual(pet_care_data.pet_types_sacrificed, ["ENDERMAN", "BLACK_CAT"])

    def test_auto_pet_data_initialization(self):
        """
        Test initialization of AutoPetData.
        """
        autopet_data = AutoPetData(self.sample_pets_data["autopet"])
        self.assertEqual(autopet_data.rules_limit, 16)
        self.assertEqual(len(autopet_data.rules), 1)
        self.assertTrue(autopet_data.migrated)
        self.assertFalse(autopet_data.migrated_2)

        # Test the single rule within AutoPetData
        rule = autopet_data.rules[0]
        self.assertIsInstance(rule, AutoPetRule)
        self.assertEqual(rule.uuid, "rule1")
        self.assertEqual(rule.rule_id, "EQUIP_WARDROBE_SLOT")
        self.assertEqual(rule.name, "Equip Golden Dragon")
        self.assertEqual(rule.data, {"slot": "4"})
        self.assertFalse(rule.disabled)
        self.assertEqual(rule.exceptions[0]["id"], "IS_IN_ISLAND")

    def test_pet_data_initialization(self):
        """
        Test initialization of individual PetData objects.
        """
        pets = [PetData(pet) for pet in self.sample_pets_data["pets"]]
        self.assertEqual(len(pets), 2)

        pet1 = pets[0]
        self.assertEqual(pet1.uuid, "pet1")
        self.assertEqual(pet1.type, "SILVERFISH")
        self.assertEqual(pet1.experience, 45163824.71)
        self.assertFalse(pet1.active)
        self.assertEqual(pet1.tier, "LEGENDARY")
        self.assertEqual(pet1.held_item, "PET_ITEM_MINING_SKILL_BOOST_RARE")
        self.assertEqual(pet1.candy_used, 0)
        self.assertIsNone(pet1.skin)

        pet2 = pets[1]
        self.assertEqual(pet2.uuid, "pet2")
        self.assertEqual(pet2.type, "BEE")
        self.assertEqual(pet2.experience, 5297.31)
        self.assertTrue(pet2.active)
        self.assertEqual(pet2.tier, "RARE")
        self.assertEqual(pet2.candy_used, 2)
        self.assertEqual(pet2.skin, "BEE_SKIN")

    def test_pets_data_initialization(self):
        """
        Test initialization of PetsData and its components.
        """
        pets_data = PetsData(self.sample_pets_data)
        
        self.assertIsInstance(pets_data.pet_care, PetCareData)
        self.assertEqual(pets_data.pet_care.coins_spent, 89614810.07)
        
        self.assertIsInstance(pets_data.autopet, AutoPetData)
        self.assertEqual(pets_data.autopet.rules_limit, 16)
        self.assertTrue(pets_data.autopet.migrated)

        self.assertEqual(len(pets_data.pets), 2)
        self.assertIsInstance(pets_data.pets[0], PetData)
        self.assertEqual(pets_data.pets[0].type, "SILVERFISH")
        self.assertEqual(pets_data.pets[1].type, "BEE")

    def test_str_representation(self):
        """
        Test the string representation of PetsData.
        """
        pets_data = PetsData(self.sample_pets_data)
        pets_data_str = str(pets_data)
        self.assertIn("Pet Care:", pets_data_str)
        self.assertIn("AutoPet Rules: 1", pets_data_str)
        self.assertIn("Total Pets: 2", pets_data_str)

class TestRiftData(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            'type': 0,
            'data': base64.b64encode(zlib.compress(b'This is a test of the inventory data handling.')).decode('utf-8')
        }
        self.sample_gzip_data = {
            'type': 0,
            'data': base64.b64encode(gzip.compress(b'This is a gzip compressed test')).decode('utf-8')
        }
        self.invalid_data = {
            'type': 0,
            'data': "InvalidData!"
        }
        self.empty_data = {
            'type': 0,
            'data': ""
        }
        self.sample_rift_data = {
            'village_plaza': {'murder': {}, 'cowboy': {}},
            'wither_cage': {'killed_eyes': ['wizard_tower']},
            'black_lagoon': {'talked_to_edwin': True},
            'dead_cats': {'found_cats': ['first', 'second'], 'unlocked_pet': True},
            'wizard_tower': {'wizard_quest_step': 3},
            'enigma': {'bought_cloak': True, 'found_souls': ['RIFT_1']},
            'gallery': {'elise_step': 5, 'sent_trophy_dialogues': ['dialogue_1']},
            'west_village': {'crazy_kloon': {'talked': True}},
            'wyld_woods': {'talked_threebrothers': ['brother_1']},
            'inventory': {'inv_contents': self.sample_data},
            'ender_chest_contents': self.invalid_data,
            'ender_chest_page_icons': [],
            'equipment_contents': self.sample_gzip_data,
        }
    
    def test_valid_zlib_data(self):
        """Test InventoryData with valid zlib-compressed, base64-encoded data."""
        inventory_data = InventoryData(self.sample_data)
        self.assertEqual(inventory_data.data, "This is a test of the inventory data handling.")

    def test_valid_gzip_data(self):
        """Test InventoryData with valid gzip-compressed, base64-encoded data."""
        inventory_data = InventoryData(self.sample_gzip_data)
        self.assertEqual(inventory_data.data, "This is a gzip compressed test")

    def test_invalid_data(self):
        """Test InventoryData with invalid base64 data."""
        inventory_data = InventoryData(self.invalid_data)
        self.assertIn("Error decoding inventory", inventory_data.data)

    def test_empty_data(self):
        """Test InventoryData with no data."""
        inventory_data = InventoryData(self.empty_data)
        self.assertEqual(inventory_data.data, "No data available")

    def test_str_representation(self):
        """Test string representation of InventoryData for valid and error cases."""
        inventory_data = InventoryData(self.sample_data)
        self.assertIn("InventoryData(Type: 0, Data Preview: This is a test", str(inventory_data))

        error_inventory_data = InventoryData(self.invalid_data)
        self.assertIn("Error decoding inventory", str(error_inventory_data))

    def test_riftdata_initialization(self):
        """Test that RiftData and its components initialize correctly."""
        rift_data = RiftData(self.sample_rift_data)
        self.assertIsInstance(rift_data.village_plaza, VillagePlaza)
        self.assertIsInstance(rift_data.wither_cage, WitherCage)
        self.assertIsInstance(rift_data.inventory, InventoryData)
        self.assertIsInstance(rift_data.ender_chest_contents, InventoryData)
        self.assertEqual(rift_data.wither_cage.killed_eyes, ['wizard_tower'])
        self.assertTrue(rift_data.black_lagoon.talked_to_edwin)

    def test_inventory_data_in_rift(self):
        """Test that RiftData processes inventory data within nested InventoryData instances."""
        rift_data = RiftData(self.sample_rift_data)
        self.assertEqual(rift_data.inventory.data, "This is a test of the inventory data handling.")
        self.assertIn("Error decoding inventory", rift_data.ender_chest_contents.data)
        self.assertEqual(rift_data.equipment_contents.data, "This is a gzip compressed test")

    def test_riftdata_str_representation(self):
        """Test string representation of RiftData."""
        rift_data = RiftData(self.sample_rift_data)
        output = str(rift_data)
        self.assertIn("Village Plaza: VillagePlaza(Murder:", output)
        self.assertIn("Inventory: InventoryData(Type: 0,", output)
        self.assertIn("Ender Chest Page Icons: []", output)



if __name__ == '__main__':
    unittest.main()
