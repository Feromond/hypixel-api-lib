import unittest
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
import requests

from hypixel_api_lib.Auctions import Bid, SkyBlockAuction, AuctionsPage, ActiveAuctions

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

if __name__ == '__main__':
    unittest.main()
