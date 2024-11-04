import unittest
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
import requests

from hypixel_api_lib.Auctions import (
    Bid,
    SkyBlockAuction,
    AuctionsPage,
    ActiveAuctions,
    PlayerAuctions,
    RecentlyEndedAuctions,
    RecentlyEndedAuction
)

class TestAuctionsComponent(unittest.TestCase):
    def setUp(self):
        # Sample data to mimic the API response for an auction page
        self.sample_auction_page_response = {
            "success": True,
            "page": 0,
            "totalPages": 1,
            "totalAuctions": 2,
            "lastUpdated": 1728619119062,
            "auctions": [
                {
                    "_id": "auction1",
                    "uuid": "uuid1",
                    "auctioneer": "player1_uuid",
                    "profile_id": "profile1_id",
                    "coop": ["coop_member1_uuid", "coop_member2_uuid"],
                    "start": 1727755200000,
                    "end": 1728360000000,
                    "item_name": "Aspect of the Dragons",
                    "item_lore": "§7A powerful sword.",
                    "extra": "Extra info",
                    "category": "weapon",
                    "tier": "legendary",
                    "starting_bid": 1000000,
                    "item_bytes": None,
                    "claimed": False,
                    "claimed_bidders": [],
                    "highest_bid_amount": 1500000,
                    "bids": [
                        {
                            "auction_id": "auction1",
                            "bidder": "bidder1_uuid",
                            "profile_id": "bidder1_profile_id",
                            "amount": 1100000,
                            "timestamp": 1727755300000
                        },
                        {
                            "auction_id": "auction1",
                            "bidder": "bidder2_uuid",
                            "profile_id": "bidder2_profile_id",
                            "amount": 1500000,
                            "timestamp": 1727755400000
                        }
                    ]
                },
                {
                    "_id": "auction2",
                    "uuid": "uuid2",
                    "auctioneer": "player2_uuid",
                    "profile_id": "profile2_id",
                    "coop": [],
                    "start": 1727755200000,
                    "end": 1728360000000,
                    "item_name": "Hyperion",
                    "item_lore": "§7An even more powerful sword.",
                    "extra": "Extra info",
                    "category": "weapon",
                    "tier": "mythic",
                    "starting_bid": 500000000,
                    "item_bytes": None,
                    "claimed": False,
                    "claimed_bidders": [],
                    "highest_bid_amount": 500000000,
                    "bids": []
                }
            ]
        }
        # Sample data for recently ended auctions
        self.sample_recently_ended_response = {
            "success": True,
            "lastUpdated": 1728619119062,
            "auctions": [
                {
                    "auction_id": "ended_auction1",
                    "seller": "seller1_uuid",
                    "seller_profile": "seller1_profile",
                    "buyer": "buyer1_uuid",
                    "buyer_profile": "buyer1_profile",
                    "timestamp": 1728619000000,
                    "price": 2000000,
                    "bin": True,
                    "item_bytes": "..."
                },
                {
                    "auction_id": "ended_auction2",
                    "seller": "seller2_uuid",
                    "seller_profile": "seller2_profile",
                    "buyer": "buyer2_uuid",
                    "buyer_profile": "buyer2_profile",
                    "timestamp": 1728619050000,
                    "price": 1500000,
                    "bin": False,
                    "item_bytes": "..."
                }
            ]
        }
        # Sample data for player auctions
        self.sample_player_auctions_response = {
            "success": True,
            "auctions": [
                {
                    "_id": "auction_player1",
                    "uuid": "uuid_player1",
                    "auctioneer": "player1_uuid",
                    "profile_id": "profile1_id",
                    "coop": ["coop_member1_uuid", "coop_member2_uuid"],
                    "start": 1727755200000,
                    "end": 1728360000000,
                    "item_name": "Player's Item",
                    "item_lore": "§7A special item.",
                    "extra": "Extra info",
                    "category": "misc",
                    "tier": "rare",
                    "starting_bid": 500000,
                    "item_bytes": None,
                    "claimed": False,
                    "claimed_bidders": [],
                    "highest_bid_amount": 750000,
                    "bids": [
                        {
                            "auction_id": "auction_player1",
                            "bidder": "bidder3_uuid",
                            "profile_id": "bidder3_profile_id",
                            "amount": 750000,
                            "timestamp": 1727755500000
                        }
                    ]
                }
            ]
        }

        # Sample data for Mojang API response
        self.sample_mojang_response = {
            "id": "player1_uuid",
            "name": "PlayerOne"
        }

    @patch('requests.get')
    def test_auctions_page_initialization(self, mock_get):
        """
        Test the initialization of the AuctionsPage class and loading of auctions.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_auction_page_response

        auctions = ActiveAuctions()
        page = auctions.get_page(0)

        self.assertIsNotNone(page)
        self.assertTrue(page.success)
        self.assertEqual(page.page, 0)
        self.assertEqual(page.totalPages, 1)
        self.assertEqual(page.totalAuctions, 2)
        self.assertEqual(len(page.auctions), 2)
        self.assertIsInstance(page.auctions[0], SkyBlockAuction)

    def test_skyblock_auction_initialization(self):
        """
        Test the initialization of the SkyBlockAuction class with complete data.
        """
        auction_data = self.sample_auction_page_response['auctions'][0]
        auction = SkyBlockAuction(auction_data)

        self.assertEqual(auction._id, "auction1")
        self.assertEqual(auction.uuid, "uuid1")
        self.assertEqual(auction.auctioneer, "player1_uuid")
        self.assertEqual(auction.profile_id, "profile1_id")
        self.assertEqual(auction.coop, ["coop_member1_uuid", "coop_member2_uuid"])
        expected_start = datetime.fromtimestamp(1727755200000 / 1000, tz=timezone.utc)
        expected_end = datetime.fromtimestamp(1728360000000 / 1000, tz=timezone.utc)
        self.assertEqual(auction.start, expected_start)
        self.assertEqual(auction.end, expected_end)
        self.assertEqual(auction.item_name, "Aspect of the Dragons")
        self.assertEqual(auction.item_lore, "§7A powerful sword.")
        self.assertEqual(auction.extra, "Extra info")
        self.assertEqual(auction.category, "weapon")
        self.assertEqual(auction.tier, "legendary")
        self.assertEqual(auction.starting_bid, 1000000)
        self.assertEqual(auction.item_bytes, None)
        self.assertFalse(auction.claimed)
        self.assertEqual(auction.claimed_bidders, [])
        self.assertEqual(auction.highest_bid_amount, 1500000)
        self.assertEqual(len(auction.bids), 2)
        self.assertIsInstance(auction.bids[0], Bid)

    def test_bid_initialization(self):
        """
        Test the initialization of the Bid class.
        """
        bid_data = self.sample_auction_page_response['auctions'][0]['bids'][0]
        bid = Bid(bid_data)

        self.assertEqual(bid.auction_id, "auction1")
        self.assertEqual(bid.bidder, "bidder1_uuid")
        self.assertEqual(bid.profile_id, "bidder1_profile_id")
        self.assertEqual(bid.amount, 1100000)
        expected_timestamp = datetime.fromtimestamp(1727755300000 / 1000, tz=timezone.utc)
        self.assertEqual(bid.timestamp, expected_timestamp)

    def test_skyblock_auction_properties(self):
        """
        Test the properties of the SkyBlockAuction class.
        """
        # Test auction with bids (not BIN)
        auction_data = self.sample_auction_page_response['auctions'][0]
        auction = SkyBlockAuction(auction_data)

        self.assertEqual(auction.current_price, 1500000)
        self.assertFalse(auction.is_bin)

        # Test auction without bids (BIN)
        auction_data_bin = self.sample_auction_page_response['auctions'][1]
        auction_bin = SkyBlockAuction(auction_data_bin)

        self.assertEqual(auction_bin.current_price, 500000000)
        self.assertTrue(auction_bin.is_bin)

    def test_skyblock_auction_str(self):
        """
        Test the __str__ method of the SkyBlockAuction class.
        """
        auction_data = self.sample_auction_page_response['auctions'][0]
        auction = SkyBlockAuction(auction_data)

        expected_str = "Auction 'Aspect of the Dragons' by player1_uuid, Price: 1500000"
        self.assertEqual(str(auction), expected_str)

        # Test BIN auction
        auction_data_bin = self.sample_auction_page_response['auctions'][1]
        auction_bin = SkyBlockAuction(auction_data_bin)

        expected_str_bin = "BIN 'Hyperion' by player2_uuid, Price: 500000000"
        self.assertEqual(str(auction_bin), expected_str_bin)

    def test_bid_str(self):
        """
        Test the __str__ method of the Bid class.
        """
        bid_data = self.sample_auction_page_response['auctions'][0]['bids'][0]
        bid = Bid(bid_data)

        expected_timestamp_str = bid.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
        expected_str = f"Bid of {bid.amount} by {bid.bidder} at {expected_timestamp_str}"
        self.assertEqual(str(bid), expected_str)

    def test_auctions_page_methods(self):
        """
        Test the methods of the AuctionsPage class.
        """
        page_data = self.sample_auction_page_response
        page = AuctionsPage(page_data)

        # Test get_auction_by_id
        auction = page.get_auction_by_id("auction1")
        self.assertIsNotNone(auction)
        self.assertEqual(auction._id, "auction1")

        # Test get_auctions_by_item_name
        auctions = page.get_auctions_by_item_name("Hyperion")
        self.assertEqual(len(auctions), 1)
        self.assertEqual(auctions[0].item_name, "Hyperion")

        # Test non-existent auction
        auction_none = page.get_auction_by_id("non_existent_auction")
        self.assertIsNone(auction_none)

    @patch('requests.get')
    def test_auctions_search_auctions(self, mock_get):
        """
        Test the search_auctions method of the Auctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_auction_page_response

        auctions = ActiveAuctions()
        matching_auctions = auctions.search_auctions(item_name="aspect of the dragons", min_price=1000000, max_price=2000000)

        self.assertEqual(len(matching_auctions), 1)
        self.assertEqual(matching_auctions[0].item_name, "Aspect of the Dragons")

        # Test sorting by price
        matching_auctions = auctions.search_auctions(sort_by_price=True, descending=True)
        self.assertEqual(matching_auctions[0].current_price, 500000000)

    @patch('requests.get')
    def test_auctions_get_auction_by_id(self, mock_get):
        """
        Test the get_auction_by_id method of the Auctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_auction_page_response

        auctions = ActiveAuctions()
        auction = auctions.get_auction_by_id("auction1")

        self.assertIsNotNone(auction)
        self.assertEqual(auction._id, "auction1")

        # Test non-existent auction
        auction_none = auctions.get_auction_by_id("non_existent_auction")
        self.assertIsNone(auction_none)

    @patch('requests.get')
    def test_auctions_error_handling(self, mock_get):
        """
        Test error handling in the Auctions class when the API call fails.
        """
        # Simulate an API error
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        auctions = ActiveAuctions()
        with self.assertRaises(ConnectionError) as context:
            auctions.get_page(0)
        self.assertIn("An error occurred while fetching page 0: API error", str(context.exception))

    def test_auctions_page_str(self):
        """
        Test the __str__ method of the AuctionsPage class.
        """
        page_data = self.sample_auction_page_response
        page = AuctionsPage(page_data)

        expected_str = "Auctions Page 0/1, Total Auctions: 2"
        self.assertEqual(str(page), expected_str)

    def test_auctions_str(self):
        """
        Test the __str__ method of the Auctions class.
        """
        auctions = ActiveAuctions()
        expected_str = f"Auctions Manager using endpoint {auctions._api_endpoint}"
        self.assertEqual(str(auctions), expected_str)

    def test_skyblock_auction_timezone_conversion(self):
        """
        Test the timezone conversion methods of the SkyBlockAuction class.
        """
        auction_data = self.sample_auction_page_response['auctions'][0]
        auction = SkyBlockAuction(auction_data)

        # Use a different timezone (e.g., MST)
        tz = timezone(timedelta(hours=-7))  # MST is UTC-7
        start_time_tz = auction.get_start_time_in_timezone(tz)
        end_time_tz = auction.get_end_time_in_timezone(tz)

        expected_start_tz = auction.start.astimezone(tz)
        expected_end_tz = auction.end.astimezone(tz)

        self.assertEqual(start_time_tz, expected_start_tz)
        self.assertEqual(end_time_tz, expected_end_tz)

    def test_skyblock_auction_missing_fields(self):
        """
        Test handling of missing optional fields in SkyBlockAuction initialization.
        """
        auction_data = {
            "_id": "auction_missing",
            "uuid": "uuid_missing",
            "auctioneer": "player_missing_uuid",
            # Missing 'profile_id', 'coop', 'start', 'end', etc.
            "item_name": "Missing Fields Item",
            "starting_bid": 500000,
            "bids": []
        }
        auction = SkyBlockAuction(auction_data)

        self.assertEqual(auction._id, "auction_missing")
        self.assertEqual(auction.uuid, "uuid_missing")
        self.assertEqual(auction.auctioneer, "player_missing_uuid")
        self.assertIsNone(auction.profile_id)
        self.assertEqual(auction.coop, [])
        self.assertIsNone(auction.start)
        self.assertIsNone(auction.end)
        self.assertEqual(auction.item_name, "Missing Fields Item")
        self.assertEqual(auction.starting_bid, 500000)
        self.assertEqual(auction.bids, [])
        self.assertTrue(auction.is_bin)
        self.assertEqual(auction.current_price, 500000)

    def test_bid_missing_fields(self):
        """
        Test handling of missing optional fields in Bid initialization.
        """
        bid_data = {
            "auction_id": "auction_missing",
            "bidder": "bidder_missing_uuid",
            "amount": 750000
            # Missing 'profile_id', 'timestamp'
        }
        bid = Bid(bid_data)

        self.assertEqual(bid.auction_id, "auction_missing")
        self.assertEqual(bid.bidder, "bidder_missing_uuid")
        self.assertIsNone(bid.profile_id)
        self.assertEqual(bid.amount, 750000)
        self.assertIsNone(bid.timestamp)

    def test_auctions_page_missing_fields(self):
        """
        Test handling of missing optional fields in AuctionsPage initialization.
        """
        page_data = {
            "success": True,
            "auctions": []
            # Missing 'page', 'totalPages', 'totalAuctions', 'lastUpdated'
        }
        page = AuctionsPage(page_data)

        self.assertTrue(page.success)
        self.assertEqual(page.page, 0)
        self.assertEqual(page.totalPages, 0)
        self.assertEqual(page.totalAuctions, 0)
        self.assertIsNone(page.lastUpdated)
        self.assertEqual(page.auctions, [])

    @patch('requests.get')
    def test_recently_ended_auctions_initialization(self, mock_get):
        """
        Test the initialization of the RecentlyEndedAuctions class and loading of auctions.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_recently_ended_response

        recently_ended_auctions = RecentlyEndedAuctions()
        self.assertIsNotNone(recently_ended_auctions)
        self.assertEqual(len(recently_ended_auctions.auctions), 2)
        self.assertIsInstance(recently_ended_auctions.auctions[0], RecentlyEndedAuction)
        expected_last_updated = datetime.fromtimestamp(1728619119062 / 1000, tz=timezone.utc)
        self.assertEqual(recently_ended_auctions.last_updated, expected_last_updated)

    def test_recently_ended_auction_initialization(self):
        """
        Test the initialization of the RecentlyEndedAuction class with sample data.
        """
        auction_data = self.sample_recently_ended_response['auctions'][0]
        auction = RecentlyEndedAuction(auction_data)

        self.assertEqual(auction.auction_id, "ended_auction1")
        self.assertEqual(auction.seller, "seller1_uuid")
        self.assertEqual(auction.seller_profile, "seller1_profile")
        self.assertEqual(auction.buyer, "buyer1_uuid")
        self.assertEqual(auction.buyer_profile, "buyer1_profile")
        expected_timestamp = datetime.fromtimestamp(1728619000000 / 1000, tz=timezone.utc)
        self.assertEqual(auction.timestamp, expected_timestamp)
        self.assertEqual(auction.price, 2000000)
        self.assertTrue(auction.bin)
        self.assertEqual(auction.item_bytes, "...")

    @patch('requests.get')
    def test_recently_ended_auctions_get_auction_by_id(self, mock_get):
        """
        Test the get_auction_by_id method of RecentlyEndedAuctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_recently_ended_response

        recently_ended_auctions = RecentlyEndedAuctions()
        auction = recently_ended_auctions.get_auction_by_id("ended_auction1")

        self.assertIsNotNone(auction)
        self.assertEqual(auction.auction_id, "ended_auction1")

        # Test non-existent auction
        auction_none = recently_ended_auctions.get_auction_by_id("non_existent_auction")
        self.assertIsNone(auction_none)

    @patch('requests.get')
    def test_recently_ended_auctions_search_auctions(self, mock_get):
        """
        Test the search_auctions method of RecentlyEndedAuctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_recently_ended_response

        recently_ended_auctions = RecentlyEndedAuctions()
        # Search by seller
        auctions_by_seller = recently_ended_auctions.search_auctions(seller="seller1_uuid")
        self.assertEqual(len(auctions_by_seller), 1)
        self.assertEqual(auctions_by_seller[0].seller, "seller1_uuid")

        # Search by buyer
        auctions_by_buyer = recently_ended_auctions.search_auctions(buyer="buyer2_uuid")
        self.assertEqual(len(auctions_by_buyer), 1)
        self.assertEqual(auctions_by_buyer[0].buyer, "buyer2_uuid")

        # Search by price range
        auctions_by_price = recently_ended_auctions.search_auctions(min_price=1000000, max_price=1800000)
        self.assertEqual(len(auctions_by_price), 1)
        self.assertEqual(auctions_by_price[0].price, 1500000)

        # Search BIN auctions only
        bin_auctions = recently_ended_auctions.search_auctions(bin_only=True)
        self.assertEqual(len(bin_auctions), 1)
        self.assertTrue(bin_auctions[0].bin)

        # Search non-BIN auctions only
        non_bin_auctions = recently_ended_auctions.search_auctions(bin_only=False)
        self.assertEqual(len(non_bin_auctions), 1)
        self.assertFalse(non_bin_auctions[0].bin)

    @patch('requests.get')
    def test_recently_ended_auctions_error_handling(self, mock_get):
        """
        Test handling of network errors in RecentlyEndedAuctions class.
        """
        # Simulate a network error
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        with self.assertRaises(ConnectionError) as context:
            RecentlyEndedAuctions()
        self.assertIn("An error occurred while fetching recently ended auctions: Network error", str(context.exception))

    @patch('requests.get')
    def test_recently_ended_auctions_unsuccessful_response(self, mock_get):
        """
        Test handling of unsuccessful API response in RecentlyEndedAuctions class.
        """
        # Mock an unsuccessful API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": False,
            "cause": "Invalid request"
        }

        with self.assertRaises(ValueError) as context:
            RecentlyEndedAuctions()
        self.assertIn("API response was not successful", str(context.exception))

    def test_recently_ended_auction_str(self):
        """
        Test the __str__ method of RecentlyEndedAuction class.
        """
        auction_data = self.sample_recently_ended_response['auctions'][0]
        auction = RecentlyEndedAuction(auction_data)
        timestamp_str = auction.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
        expected_str = f"BIN 'ended_auction1' sold by seller1_uuid to buyer1_uuid at {timestamp_str} for 2000000"
        self.assertEqual(str(auction), expected_str)

        # Test non-BIN auction
        auction_data_non_bin = self.sample_recently_ended_response['auctions'][1]
        auction_non_bin = RecentlyEndedAuction(auction_data_non_bin)
        timestamp_str_non_bin = auction_non_bin.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")
        expected_str_non_bin = f"Auction 'ended_auction2' sold by seller2_uuid to buyer2_uuid at {timestamp_str_non_bin} for 1500000"
        self.assertEqual(str(auction_non_bin), expected_str_non_bin)

    @patch('requests.get')
    def test_recently_ended_auctions_str(self, mock_get):
        """
        Test the __str__ method of RecentlyEndedAuctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_recently_ended_response

        recently_ended_auctions = RecentlyEndedAuctions()
        last_updated_str = recently_ended_auctions.last_updated.strftime("%Y-%m-%d %H:%M:%S %Z")
        expected_str = f"RecentlyEndedAuctions with 2 auctions as of {last_updated_str}"
        self.assertEqual(str(recently_ended_auctions), expected_str)

    def test_recently_ended_auction_missing_fields(self):
        """
        Test handling of missing optional fields in RecentlyEndedAuction initialization.
        """
        auction_data = {
            "auction_id": "ended_auction_missing",
            "seller": "seller_missing_uuid",
            "price": 1000000
            # Missing 'seller_profile', 'buyer', 'buyer_profile', 'timestamp', 'bin', 'item_bytes'
        }
        auction = RecentlyEndedAuction(auction_data)

        self.assertEqual(auction.auction_id, "ended_auction_missing")
        self.assertEqual(auction.seller, "seller_missing_uuid")
        self.assertIsNone(auction.seller_profile)
        self.assertIsNone(auction.buyer)
        self.assertIsNone(auction.buyer_profile)
        self.assertIsNone(auction.timestamp)
        self.assertEqual(auction.price, 1000000)
        self.assertFalse(auction.bin)  # Default to False
        self.assertIsNone(auction.item_bytes)

    @patch('requests.get')
    def test_recently_ended_auctions_empty_response(self, mock_get):
        """
        Test handling when the API returns an empty list of auctions.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": True,
            "lastUpdated": 1728619119062,
            "auctions": []
        }

        recently_ended_auctions = RecentlyEndedAuctions()
        self.assertEqual(len(recently_ended_auctions.auctions), 0)

    @patch('requests.get')
    def test_player_auctions_get_auction_by_uuid(self, mock_get):
        """
        Test fetching an auction by its UUID using the PlayerAuctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_player_auctions_response

        player_auctions = PlayerAuctions(api_key="test_api_key")
        auction = player_auctions.get_auction_by_uuid("uuid_player1")

        self.assertIsNotNone(auction)
        self.assertEqual(auction.uuid, "uuid_player1")
        self.assertEqual(auction.auctioneer, "player1_uuid")

    @patch('requests.get')
    def test_player_auctions_get_auctions_by_player_uuid(self, mock_get):
        """
        Test fetching auctions by player UUID using the PlayerAuctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_player_auctions_response

        player_auctions = PlayerAuctions(api_key="test_api_key")
        auctions = player_auctions.get_auctions_by_player_uuid("player1_uuid")

        self.assertEqual(len(auctions), 1)
        self.assertEqual(auctions[0].auctioneer, "player1_uuid")

    @patch('requests.get')
    def test_player_auctions_get_auctions_by_profile_uuid(self, mock_get):
        """
        Test fetching auctions by profile UUID using the PlayerAuctions class.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_player_auctions_response

        player_auctions = PlayerAuctions(api_key="test_api_key")
        auctions = player_auctions.get_auctions_by_profile_uuid("profile1_id")

        self.assertEqual(len(auctions), 1)
        self.assertEqual(auctions[0].profile_id, "profile1_id")

    @patch('requests.get')
    def test_player_auctions_get_auctions_by_username(self, mock_get):
        """
        Test fetching auctions by username using the PlayerAuctions class.
        """
        # Mock the Mojang API call
        def mock_mojang_api(url, *args, **kwargs):
            if "mojang.com" in url:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = self.sample_mojang_response
                return mock_response
            else:
                # Hypixel API call
                mock_response = unittest.mock.Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = self.sample_player_auctions_response
                return mock_response

        mock_get.side_effect = mock_mojang_api

        player_auctions = PlayerAuctions(api_key="test_api_key")
        auctions = player_auctions.get_auctions_by_username("PlayerOne")

        self.assertEqual(len(auctions), 1)
        self.assertEqual(auctions[0].auctioneer, "player1_uuid")

    @patch('requests.get')
    def test_player_auctions_mojang_api_username_not_found(self, mock_get):
        """
        Test handling of non-existent username in the Mojang API.
        """
        # Mock the Mojang API call to return 204 No Content
        def mock_mojang_api(url, *args, **kwargs):
            if "mojang.com" in url:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = 204
                return mock_response
            else:
                mock_response = unittest.mock.Mock()
                return mock_response

        mock_get.side_effect = mock_mojang_api

        player_auctions = PlayerAuctions(api_key="test_api_key")

        with self.assertRaises(ValueError) as context:
            player_auctions.get_auctions_by_username("NonExistentUser")

        self.assertIn("Username 'NonExistentUser' does not exist.", str(context.exception))

    @patch('requests.get')
    def test_player_auctions_hypixel_api_error(self, mock_get):
        """
        Test handling of errors from the Hypixel API in the PlayerAuctions class.
        """
        # Mock the Hypixel API call to return 403 Forbidden
        def mock_hypixel_api(url, *args, **kwargs):
            if "hypixel.net" in url:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = 403
                mock_response.json.return_value = {
                    "success": False,
                    "cause": "Invalid API key"
                }
                raise requests.exceptions.HTTPError(response=mock_response)
            else:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = self.sample_mojang_response
                return mock_response

        mock_get.side_effect = mock_hypixel_api

        player_auctions = PlayerAuctions(api_key="invalid_api_key")

        with self.assertRaises(PermissionError) as context:
            player_auctions.get_auctions_by_username("PlayerOne")

        self.assertIn("Forbidden (403): Invalid API key", str(context.exception))

    @patch('requests.get')
    def test_player_auctions_network_error(self, mock_get):
        """
        Test handling of network errors in the PlayerAuctions class.
        """
        # Mock the network error
        def mock_network_error(url, *args, **kwargs):
            raise requests.exceptions.RequestException("Network error")

        mock_get.side_effect = mock_network_error

        player_auctions = PlayerAuctions(api_key="test_api_key")

        with self.assertRaises(ConnectionError) as context:
            player_auctions.get_auctions_by_player_uuid("player1_uuid")

        self.assertIn("An error occurred while fetching auctions for player player1_uuid: Network error", str(context.exception))

    @patch('requests.get')
    def test_player_auctions_invalid_auction_uuid(self, mock_get):
        """
        Test fetching an auction with an invalid auction UUID.
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": True,
            "auctions": []
        }

        player_auctions = PlayerAuctions(api_key="test_api_key")
        auction = player_auctions.get_auction_by_uuid("invalid_uuid")

        self.assertIsNone(auction)

    @patch('requests.get')
    def test_player_auctions_invalid_profile_uuid(self, mock_get):
        """
        Test fetching auctions with an invalid profile UUID.
        """
        # Mock the Hypixel API call to return an error
        mock_get.return_value.status_code = 422
        mock_get.return_value.json.return_value = {
            "success": False,
            "cause": "Invalid profile UUID"
        }
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_get.return_value)

        player_auctions = PlayerAuctions(api_key="test_api_key")

        with self.assertRaises(ValueError) as context:
            player_auctions.get_auctions_by_profile_uuid("invalid_profile_uuid")

        self.assertIn("Unprocessable Entity (422): Invalid profile UUID", str(context.exception))

    @patch('requests.get')
    def test_player_auctions_rate_limit(self, mock_get):
        """
        Test handling of rate limit exceeded in the PlayerAuctions class.
        """
        # Mock the Hypixel API call to return 429 - Too Many Requests
        mock_get.return_value.status_code = 429
        mock_get.return_value.json.return_value = {
            "success": False,
            "cause": "You have exceeded your rate limit",
            "throttle": True,
            "global": False
        }
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_get.return_value)

        player_auctions = PlayerAuctions(api_key="test_api_key")

        with self.assertRaises(ConnectionError) as context:
            player_auctions.get_auctions_by_player_uuid("player1_uuid")

        self.assertIn("Rate Limit Exceeded (429): You have exceeded your rate limit", str(context.exception))

    @patch('requests.get')
    def test_player_auctions_global_throttle(self, mock_get):
        """
        Test handling of global throttle in the PlayerAuctions class.
        """
        # Mock the Hypixel API call to return 429 - Too Many Requests with global throttle
        mock_get.return_value.status_code = 429
        mock_get.return_value.json.return_value = {
            "success": False,
            "cause": "Global throttle in effect",
            "throttle": True,
            "global": True
        }
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_get.return_value)

        player_auctions = PlayerAuctions(api_key="test_api_key")

        with self.assertRaises(ConnectionError) as context:
            player_auctions.get_auctions_by_player_uuid("player1_uuid")

        self.assertIn("Global Throttle (429): Global throttle in effect", str(context.exception))

    @patch('requests.get')
    def test_player_auctions_mojang_api_error(self, mock_get):
        """
        Test handling of errors from the Mojang API.
        """
        # Mock the Mojang API call to return an error
        def mock_mojang_api(url, *args, **kwargs):
            if "mojang.com" in url:
                mock_response = unittest.mock.Mock()
                mock_response.status_code = 500
                mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
                return mock_response
            else:
                mock_response = unittest.mock.Mock()
                return mock_response

        mock_get.side_effect = mock_mojang_api

        player_auctions = PlayerAuctions(api_key="test_api_key")

        with self.assertRaises(ConnectionError) as context:
            player_auctions.get_auctions_by_username("PlayerOne")

        self.assertIn("HTTP Error while fetching UUID for username 'PlayerOne'", str(context.exception))

    @patch('requests.get')
    def test_player_auctions_mojang_api_network_error(self, mock_get):
        """
        Test handling of network errors when calling the Mojang API.
        """
        # Mock the network error for Mojang API
        def mock_network_error(url, *args, **kwargs):
            if "mojang.com" in url:
                raise requests.exceptions.RequestException("Network error")
            else:
                mock_response = unittest.mock.Mock()
                return mock_response

        mock_get.side_effect = mock_network_error

        player_auctions = PlayerAuctions(api_key="test_api_key")

        with self.assertRaises(ConnectionError) as context:
            player_auctions.get_auctions_by_username("PlayerOne")

        self.assertIn("An error occurred while fetching UUID for username 'PlayerOne': Network error", str(context.exception))

    def test_player_auctions_str(self):
        """
        Test the __str__ method of the PlayerAuctions class.
        """
        player_auctions = PlayerAuctions(api_key="test_api_key")
        expected_str = f"PlayerAuctions Manager using endpoint {player_auctions._api_endpoint}"
        self.assertEqual(str(player_auctions), expected_str)


if __name__ == '__main__':
    unittest.main()
