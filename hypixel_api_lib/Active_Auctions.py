from datetime import datetime, timezone
import requests

ACTIVE_AUCTIONS_API_URL = "https://api.hypixel.net/skyblock/auctions"

class Bid:
    """
    Represents a single bid in an auction.

    Attributes:
        auction_id (str): The ID of the auction.
        bidder (str): The UUID of the bidder.
        profile_id (str): The profile ID of the bidder.
        amount (int): The amount of the bid.
        timestamp (datetime): The timestamp of the bid.
    """

    def __init__(self, bid_data):
        self.auction_id = bid_data.get('auction_id')
        self.bidder = bid_data.get('bidder')
        self.profile_id = bid_data.get('profile_id')
        self.amount = bid_data.get('amount')
        self.timestamp = self._convert_timestamp(bid_data.get('timestamp'))

    def _convert_timestamp(self, timestamp):
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z") if self.timestamp else "N/A"
        return f"Bid of {self.amount} by {self.bidder} at {timestamp_str}"

class SkyBlockAuction:
    """
    Represents a single SkyBlock auction.

    Attributes:
        _id (str): The unique identifier of the auction.
        uuid (str): The UUID of the auction.
        auctioneer (str): The UUID of the auctioneer.
        profile_id (str): The profile ID of the auctioneer.
        coop (list of str): List of coop member UUIDs.
        start (datetime): The start time of the auction.
        end (datetime): The end time of the auction.
        item_name (str): The name of the item being auctioned.
        item_lore (str): The lore of the item.
        extra (str): Additional information.
        category (str): The category of the item.
        tier (str): The tier of the item.
        starting_bid (int): The starting bid amount.
        item_bytes (object): Serialized item data.
        claimed (bool): Whether the auction has been claimed.
        claimed_bidders (list): List of bidders who have claimed the item.
        highest_bid_amount (int): The highest bid amount.
        bids (list of Bid): List of bids.
    """

    def __init__(self, auction_data):
        self._id = auction_data.get('_id')
        self.uuid = auction_data.get('uuid')
        self.auctioneer = auction_data.get('auctioneer')
        self.profile_id = auction_data.get('profile_id')
        self.coop = auction_data.get('coop', [])
        self.start = self._convert_timestamp(auction_data.get('start'))
        self.end = self._convert_timestamp(auction_data.get('end'))
        self.item_name = auction_data.get('item_name')
        self.item_lore = auction_data.get('item_lore')
        self.extra = auction_data.get('extra')
        self.category = auction_data.get('category')
        self.tier = auction_data.get('tier')
        self.starting_bid = auction_data.get('starting_bid')
        self.item_bytes = auction_data.get('item_bytes')
        self.claimed = auction_data.get('claimed')
        self.claimed_bidders = auction_data.get('claimed_bidders', [])
        self.highest_bid_amount = auction_data.get('highest_bid_amount')
        self.bids = [Bid(bid) for bid in auction_data.get('bids', [])]

    def _convert_timestamp(self, timestamp):
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def get_start_time_in_timezone(self, tz):
        """
        Get the start time converted to the specified time zone.

        Args:
            tz (timezone): A timezone object.

        Returns:
            datetime: The start time in the specified time zone.
        """
        if self.start:
            return self.start.astimezone(tz)
        return None

    def get_end_time_in_timezone(self, tz):
        """
        Get the end time converted to the specified time zone.

        Args:
            tz (timezone): A timezone object.

        Returns:
            datetime: The end time in the specified time zone.
        """
        if self.end:
            return self.end.astimezone(tz)
        return None

    @property
    def current_price(self):
        """
        Get the current price of the auction.

        For BIN auctions (with no bids), this is the starting_bid.
        For regular auctions, this is the highest_bid_amount.

        Returns:
            int: The current price of the auction.
        """
        if not self.bids:
            return self.starting_bid
        else:
            return max(self.starting_bid, self.highest_bid_amount)

    @property
    def is_bin(self):
        """
        Estimate whether the auction is a BIN auction.

        Returns:
            bool: True if the auction is likely a BIN auction, False otherwise.
        """
        # Since I can't know from the API, I'm assume auctions with no bids are BIN
        return not self.bids

    def __str__(self):
        auction_type = "BIN" if self.is_bin else "Auction"
        return f"{auction_type} '{self.item_name}' by {self.auctioneer}, Price: {self.current_price}"

class AuctionsPage:
    """
    Represents a single page of auctions from the Hypixel SkyBlock Auctions API.

    Attributes:
        success (bool): Indicates whether the API request was successful.
        page (int): The current page number.
        totalPages (int): The total number of pages.
        totalAuctions (int): The total number of auctions.
        lastUpdated (datetime): The last updated timestamp.
        auctions (list of SkyBlockAuction): The list of auctions on this page.
    """

    def __init__(self, page_data):
        self.success = page_data.get('success', False)
        self.page = page_data.get('page', 0)
        self.totalPages = page_data.get('totalPages', 0)
        self.totalAuctions = page_data.get('totalAuctions', 0)
        self.lastUpdated = self._convert_timestamp(page_data.get('lastUpdated'))
        self.auctions = [SkyBlockAuction(auction) for auction in page_data.get('auctions', [])]

    def _convert_timestamp(self, timestamp):
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def get_auction_by_id(self, auction_id):
        """
        Retrieve an auction by its ID from the current page.

        Args:
            auction_id (str): The ID of the auction.

        Returns:
            SkyBlockAuction or None: The auction object, or None if not found.
        """
        return next((auction for auction in self.auctions if auction._id == auction_id), None)

    def get_auctions_by_item_name(self, item_name):
        """
        Retrieve auctions by item name from the current page.

        Args:
            item_name (str): The name of the item.

        Returns:
            list of SkyBlockAuction: A list of auctions matching the item name.
        """
        return [auction for auction in self.auctions if auction.item_name.lower() == item_name.lower()]

    def __str__(self):
        return f"Auctions Page {self.page}/{self.totalPages}, Total Auctions: {self.totalAuctions}"

class Auctions:
    """
    Manages fetching and storing auction data from the Hypixel SkyBlock Auctions API.

    Attributes:
        api_endpoint (str): The API endpoint URL.
        all_auctions (list of SkyBlockAuction): Cached list of all auctions.
        cache_pages (dict): Cached pages of auctions.
    """

    def __init__(self, api_endpoint=ACTIVE_AUCTIONS_API_URL, preload_all=False):
        self._api_endpoint = api_endpoint
        self.all_auctions = []
        self.cache_pages = {}
        if preload_all:
            self.all_auctions = self.get_all_auctions()

    def get_page(self, page_number=0):
        """
        Fetch a specific page of auctions, using cache if available.

        Args:
            page_number (int): The page number to fetch.

        Returns:
            AuctionsPage: The AuctionsPage object for the requested page.
        """
        if page_number in self.cache_pages:
            return self.cache_pages[page_number]

        params = {'page': page_number}
        try:
            response = requests.get(self._api_endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                page = AuctionsPage(data)
                self.cache_pages[page_number] = page
                return page
            else:
                raise ValueError("API response was not successful")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching page {page_number}: {e}")

    def get_all_auctions(self):
        """
        Fetch all auctions by iterating through all available pages.

        Returns:
            list of SkyBlockAuction: A list of all auctions.
        """
        if self.all_auctions:
            return self.all_auctions  # Return cached data

        all_auctions = []
        first_page = self.get_page(0)
        total_pages = first_page.totalPages
        all_auctions.extend(first_page.auctions)

        for page_number in range(1, total_pages):
            page = self.get_page(page_number)
            all_auctions.extend(page.auctions)

        self.all_auctions = all_auctions  # Cache the results
        return all_auctions

    def search_auctions(self, item_name=None, min_price=None, max_price=None, sort_by_price=False, descending=False, max_pages=None):
        """
        Search for auctions matching the specified criteria.

        Args:
            item_name (str, optional): The name of the item to search for.
            min_price (int, optional): The minimum price.
            max_price (int, optional): The maximum price.
            sort_by_price (bool, optional): Whether to sort the results by price.
            descending (bool, optional): Whether to sort in descending order.
            max_pages (int, optional): Maximum number of pages to search.

        Returns:
            list of SkyBlockAuction: A list of auctions matching the criteria.
        """
        matching_auctions = []

        # Use cached data if available
        if self.all_auctions:
            auctions_to_search = self.all_auctions
        else:
            first_page = self.get_page(0)
            total_pages = first_page.totalPages
            if max_pages:
                total_pages = min(total_pages, max_pages)

            auctions_to_search = []
            auctions_to_search.extend(first_page.auctions)

            for page_number in range(1, total_pages):
                page = self.get_page(page_number)
                auctions_to_search.extend(page.auctions)

        # Function to check if an auction matches the criteria
        def matches(auction):
            if item_name and item_name.lower() not in auction.item_name.lower():
                return False
            price = auction.current_price
            if min_price is not None and price < min_price:
                return False
            if max_price is not None and price > max_price:
                return False
            return True

        for auction in auctions_to_search:
            if matches(auction):
                matching_auctions.append(auction)

        if sort_by_price:
            matching_auctions.sort(key=lambda x: x.current_price, reverse=descending)

        return matching_auctions

    def get_auction_by_id(self, auction_id):
        """
        Fetch a specific auction by its ID.

        Args:
            auction_id (str): The ID of the auction.

        Returns:
            SkyBlockAuction: The auction with the specified ID, or None if not found.
        """
        first_page = self.get_page(0)
        total_pages = first_page.totalPages

        for page_number in range(total_pages):
            page = self.get_page(page_number)
            auction = page.get_auction_by_id(auction_id)
            if auction:
                return auction
        return None

    def __str__(self):
        return f"Auctions Manager using endpoint {self._api_endpoint}"