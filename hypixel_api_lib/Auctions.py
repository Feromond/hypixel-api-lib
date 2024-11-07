from datetime import datetime, timezone
import requests

ACTIVE_AUCTIONS_API_URL = r"https://api.hypixel.net/skyblock/auctions"
RECENTLY_ENDED_AUCTIONS_API_URL = r"https://api.hypixel.net/skyblock/auctions_ended"
PLAYER_AUCTION_API_URL = r"https://api.hypixel.net/skyblock/auction"
MOJANG_API_URL = r"https://api.mojang.com/users/profiles/minecraft/"

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

    def __init__(self, bid_data : dict | None) -> None:
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

class ActiveAuctions:
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

class RecentlyEndedAuction:
    """
    Represents a recently ended SkyBlock auction.
    The skyblock auction representation of an auction 
    is not sufficent for these recently ended versions.
    That is why I create this extra class to handle it specifically.

    Attributes:
        auction_id (str): The unique identifier of the auction.
        seller (str): The UUID of the seller.
        seller_profile (str): The profile ID of the seller.
        buyer (str): The UUID of the buyer.
        buyer_profile (str): The profile ID of the buyer.
        timestamp (datetime): The timestamp when the auction ended.
        price (int): The final price of the auction.
        bin (bool): Whether the auction was a Buy It Now (BIN) auction.
        item_bytes (str): Serialized item data.
    """

    def __init__(self, auction_data):
        self.auction_id = auction_data.get('auction_id')
        self.seller = auction_data.get('seller')
        self.seller_profile = auction_data.get('seller_profile')
        self.buyer = auction_data.get('buyer')
        self.buyer_profile = auction_data.get('buyer_profile')
        self.timestamp = self._convert_timestamp(auction_data.get('timestamp'))
        self.price = auction_data.get('price')
        self.bin = auction_data.get('bin', False)
        self.item_bytes = auction_data.get('item_bytes')

    def _convert_timestamp(self, timestamp):
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        auction_type = "BIN" if self.bin else "Auction"
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z") if self.timestamp else "N/A"
        return f"{auction_type} '{self.auction_id}' sold by {self.seller} to {self.buyer} at {timestamp_str} for {self.price}"

class RecentlyEndedAuctions:
    """
    Manages fetching recently ended auctions from the Hypixel SkyBlock Auctions API.

    Attributes:
        last_updated (datetime): The last updated timestamp.
        auctions (list of RecentlyEndedAuction): The list of recently ended auctions.
    """

    def __init__(self, api_endpoint=RECENTLY_ENDED_AUCTIONS_API_URL):
        self._api_endpoint = api_endpoint
        self.last_updated = None
        self.auctions = []
        self._load_ended_auctions()

    def _load_ended_auctions(self):
        """
        Fetch recently ended auctions from the API.
        """
        try:
            response = requests.get(self._api_endpoint)
            response.raise_for_status()
            data = response.json()
            if data.get('success'):
                self.last_updated = self._convert_timestamp(data.get('lastUpdated'))
                auctions_data = data.get('auctions', [])
                self.auctions = [RecentlyEndedAuction(auction_data) for auction_data in auctions_data]
            else:
                raise ValueError("API response was not successful")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching recently ended auctions: {e}")

    def _convert_timestamp(self, timestamp):
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def get_auction_by_id(self, auction_id):
        """
        Retrieve an auction by its ID.

        Args:
            auction_id (str): The ID of the auction.

        Returns:
            RecentlyEndedAuction or None: The auction object, or None if not found.
        """
        return next((auction for auction in self.auctions if auction.auction_id == auction_id), None)

    def search_auctions(self, seller=None, buyer=None, min_price=None, max_price=None, bin_only=None):
        """
        Search for auctions matching the specified criteria.

        Args:
            seller (str, optional): The UUID of the seller.
            buyer (str, optional): The UUID of the buyer.
            min_price (int, optional): The minimum price.
            max_price (int, optional): The maximum price.
            bin_only (bool, optional): If True, only include BIN auctions; if False, exclude BIN auctions; if None, include all.

        Returns:
            list of RecentlyEndedAuction: A list of auctions matching the criteria.
        """
        matching_auctions = []

        for auction in self.auctions:
            if seller and auction.seller != seller:
                continue
            if buyer and auction.buyer != buyer:
                continue
            if min_price is not None and auction.price < min_price:
                continue
            if max_price is not None and auction.price > max_price:
                continue
            if bin_only is True and not auction.bin:
                continue
            if bin_only is False and auction.bin:
                continue
            matching_auctions.append(auction)

        return matching_auctions

    def __str__(self):
        last_updated_str = self.last_updated.strftime("%Y-%m-%d %H:%M:%S %Z") if self.last_updated else "N/A"
        return f"RecentlyEndedAuctions with {len(self.auctions)} auctions as of {last_updated_str}"

class PlayerAuctions:
    """
    Manages fetching player-specific auctions from the Hypixel SkyBlock Auctions API.

    Attributes:
        api_key (str): The API key for accessing the Hypixel API.
        api_endpoint (str): The API endpoint URL.
    """

    def __init__(self, api_key: str, api_endpoint: str = PLAYER_AUCTION_API_URL) -> None:
        self._api_endpoint: str = api_endpoint
        self.api_key: str = api_key

    def _convert_timestamp(self, timestamp: int | None) -> datetime | None:
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def _get_uuid_from_username(self, username: str) -> str:
        """
        Fetch the UUID of a player from their username using the Mojang API.
        TODO:(This method may eventually need to migrate to some more general spot. 
            Not sure how often we may reuse something like this yet)

        Args:
            username (str): The username of the player.

        Returns:
            str: The UUID of the player without dashes.

        Raises:
            ValueError: If the username does not exist.
            ConnectionError: If there's an error contacting the Mojang API.
        """
        try:
            response = requests.get(MOJANG_API_URL + username)
            if response.status_code == 204:
                raise ValueError(f"Username '{username}' does not exist.")
            response.raise_for_status()
            data = response.json()
            uuid = data.get('id')
            if uuid:
                return uuid
            else:
                raise ValueError(f"UUID not found for username '{username}'.")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"HTTP Error while fetching UUID for username '{username}': {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching UUID for username '{username}': {e}")

    def get_auction_by_uuid(self, auction_uuid: str) -> SkyBlockAuction | None:
        """
        Fetch an auction by its auction UUID.

        Args:
            auction_uuid (str): The UUID of the auction.

        Returns:
            SkyBlockAuction | None: The auction object, or None if not found.

        Raises:
            ValueError: If the API response indicates an error.
            ConnectionError: If there's a network-related error.
        """
        params = {
            'uuid': auction_uuid,
            'key': self.api_key
        }
        try:
            response = requests.get(self._api_endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('success'):
                auctions_data = data.get('auctions', [])
                if auctions_data:
                    # There should only be one auction in this case
                    auction_data = auctions_data[0]
                    return SkyBlockAuction(auction_data)
                else:
                    return None
            else:
                cause = data.get('cause', 'Unknown error')
                raise ValueError(f"API response was not successful: {cause}")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_data = e.response.json()
            cause = error_data.get('cause', 'Unknown error')
            if status_code == 400:
                raise ValueError(f"Bad Request (400): {cause}")
            elif status_code == 403:
                raise PermissionError(f"Forbidden (403): {cause}")
            elif status_code == 422:
                raise ValueError(f"Unprocessable Entity (422): {cause}")
            elif status_code == 429:
                throttle = error_data.get('throttle', False)
                global_throttle = error_data.get('global', False)
                if global_throttle:
                    raise ConnectionError(f"Global Throttle (429): {cause}")
                else:
                    raise ConnectionError(f"Rate Limit Exceeded (429): {cause}")
            else:
                raise ConnectionError(f"HTTP Error {status_code}: {cause}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching auction {auction_uuid}: {e}")

    def get_auctions_by_player_uuid(self, player_uuid: str) -> list[SkyBlockAuction]:
        """
        Fetch auctions by player UUID.

        Args:
            player_uuid (str): The UUID of the player.

        Returns:
            list[SkyBlockAuction]: List of auctions created by the player.

        Raises:
            ValueError: If the API response indicates an error.
            ConnectionError: If there's a network-related error.
        """
        params = {
            'player': player_uuid,
            'key': self.api_key
        }
        try:
            response = requests.get(self._api_endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('success'):
                auctions_data = data.get('auctions', [])
                return [SkyBlockAuction(auction_data) for auction_data in auctions_data]
            else:
                cause = data.get('cause', 'Unknown error')
                raise ValueError(f"API response was not successful: {cause}")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_data = e.response.json()
            cause = error_data.get('cause', 'Unknown error')
            if status_code == 400:
                raise ValueError(f"Bad Request (400): {cause}")
            elif status_code == 403:
                raise PermissionError(f"Forbidden (403): {cause}")
            elif status_code == 422:
                raise ValueError(f"Unprocessable Entity (422): {cause}")
            elif status_code == 429:
                throttle = error_data.get('throttle', False)
                global_throttle = error_data.get('global', False)
                if global_throttle:
                    raise ConnectionError(f"Global Throttle (429): {cause}")
                else:
                    raise ConnectionError(f"Rate Limit Exceeded (429): {cause}")
            else:
                raise ConnectionError(f"HTTP Error {status_code}: {cause}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching auctions for player {player_uuid}: {e}")

    def get_auctions_by_profile_uuid(self, profile_uuid: str) -> list[SkyBlockAuction]:
        """
        Fetch auctions by profile UUID.

        Args:
            profile_uuid (str): The UUID of the profile.

        Returns:
            list[SkyBlockAuction]: List of auctions associated with the profile.

        Raises:
            ValueError: If the API response indicates an error.
            ConnectionError: If there's a network-related error.
        """
        params = {
            'profile': profile_uuid,
            'key': self.api_key
        }
        try:
            response = requests.get(self._api_endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('success'):
                auctions_data = data.get('auctions', [])
                return [SkyBlockAuction(auction_data) for auction_data in auctions_data]
            else:
                cause = data.get('cause', 'Unknown error')
                raise ValueError(f"API response was not successful: {cause}")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_data = e.response.json()
            cause = error_data.get('cause', 'Unknown error')
            if status_code == 400:
                raise ValueError(f"Bad Request (400): {cause}")
            elif status_code == 403:
                raise PermissionError(f"Forbidden (403): {cause}")
            elif status_code == 422:
                raise ValueError(f"Unprocessable Entity (422): {cause}")
            elif status_code == 429:
                throttle = error_data.get('throttle', False)
                global_throttle = error_data.get('global', False)
                if global_throttle:
                    raise ConnectionError(f"Global Throttle (429): {cause}")
                else:
                    raise ConnectionError(f"Rate Limit Exceeded (429): {cause}")
            else:
                raise ConnectionError(f"HTTP Error {status_code}: {cause}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching auctions for profile {profile_uuid}: {e}")

    def get_auctions_by_username(self, username: str) -> list[SkyBlockAuction]:
        """
        Fetch auctions by player's username.

        Args:
            username (str): The username of the player.

        Returns:
            list[SkyBlockAuction]: List of auctions created by the player.

        Raises:
            ValueError: If the username does not exist or the API response indicates an error.
            ConnectionError: If there's a network-related error.
        """
        try:
            player_uuid = self._get_uuid_from_username(username)
            return self.get_auctions_by_player_uuid(player_uuid)
        except ValueError as ve:
            raise ve
        except ConnectionError as ce:
            raise ce

    def __str__(self) -> str:
        """Return a string representation of the PlayerAuctions manager."""
        return f"PlayerAuctions Manager using endpoint {self._api_endpoint}"
