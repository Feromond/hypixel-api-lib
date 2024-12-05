from datetime import datetime
import requests
from hypixel_api_lib.utils import convert_timestamp
import re
from difflib import get_close_matches

BAZAAR_API_URL = "https://api.hypixel.net/skyblock/bazaar"

class BazaarOrderSummaryItem:
    """
    Represents an order summary item in the bazaar.

    Attributes:
        amount (int): The total amount of items in the order.
        price_per_unit (float): The price per unit of the item.
        orders (int): The number of orders at this price.
    """

    def __init__(self, data: dict) -> None:
        self.amount: int = data.get('amount', 0)
        self.price_per_unit: float = data.get('pricePerUnit', 0.0)
        self.orders: int = data.get('orders', 0)

    def __str__(self) -> str:
        return f"Amount: {self.amount}, Price per Unit: {self.price_per_unit}, Orders: {self.orders}"

class BazaarProductQuickStatus:
    """
    Represents the quick status of a bazaar product.

    Attributes:
        product_id (str): The product ID.
        sell_price (float): The weighted average sell price.
        sell_volume (int): The total sell volume.
        sell_moving_week (int): The sell volume over the moving week.
        sell_orders (int): The number of sell orders.
        buy_price (float): The weighted average buy price.
        buy_volume (int): The total buy volume.
        buy_moving_week (int): The buy volume over the moving week.
        buy_orders (int): The number of buy orders.
    """

    def __init__(self, data: dict) -> None:
        self.product_id: str = data.get('productId', '')
        self.sell_price: float = data.get('sellPrice', 0.0)
        self.sell_volume: int = data.get('sellVolume', 0)
        self.sell_moving_week: int = data.get('sellMovingWeek', 0)
        self.sell_orders: int = data.get('sellOrders', 0)
        self.buy_price: float = data.get('buyPrice', 0.0)
        self.buy_volume: int = data.get('buyVolume', 0)
        self.buy_moving_week: int = data.get('buyMovingWeek', 0)
        self.buy_orders: int = data.get('buyOrders', 0)

    def __str__(self) -> str:
        return (f"Product ID: {self.product_id}, Sell Price: {self.sell_price}, Sell Volume: {self.sell_volume}, "
                f"Sell Moving Week: {self.sell_moving_week}, Sell Orders: {self.sell_orders}, "
                f"Buy Price: {self.buy_price}, Buy Volume: {self.buy_volume}, "
                f"Buy Moving Week: {self.buy_moving_week}, Buy Orders: {self.buy_orders}")

class BazaarProduct:
    """
    Represents a bazaar product.

    Attributes:
        product_id (str): The product ID.
        sell_summary (list of BazaarOrderSummaryItem): The sell order summaries.
        buy_summary (list of BazaarOrderSummaryItem): The buy order summaries.
        quick_status (BazaarProductQuickStatus): The quick status of the product.
    """

    def __init__(self, product_id: str, data: dict) -> None:
        self.product_id: str = product_id
        self.sell_summary: list[BazaarOrderSummaryItem] = [BazaarOrderSummaryItem(item) for item in data.get('sell_summary', [])]
        self.buy_summary: list[BazaarOrderSummaryItem] = [BazaarOrderSummaryItem(item) for item in data.get('buy_summary', [])]
        self.quick_status: BazaarProductQuickStatus = BazaarProductQuickStatus(data.get('quick_status', {}))

    def get_top_buy_order(self) -> BazaarOrderSummaryItem | None:
        """
        Returns the top buy order summary item.

        Returns:
            BazaarOrderSummaryItem or None: The top buy order summary item, or None if not available.
        """
        return self.buy_summary[0] if self.buy_summary else None

    def get_top_sell_order(self) -> BazaarOrderSummaryItem | None:
        """
        Returns the top sell order summary item.

        Returns:
            BazaarOrderSummaryItem or None: The top sell order summary item, or None if not available.
        """
        return self.sell_summary[0] if self.sell_summary else None

    def __str__(self) -> str:
        return f"Bazaar Product: {self.product_id}"

class Bazaar:
    """
    Manages fetching and storing the bazaar data from the API.

    Attributes:
        last_updated (datetime): The timestamp of the last update.
        products (dict of str to BazaarProduct): The bazaar products.
        normalized_product_ids (dict of str to str): Mapping of normalized product names to actual product IDs.
    """

    COMMON_PREFIXES = [
        "ENCHANTMENT_ULTIMATE_",
        "ENCHANTMENT_",
        "DUNGEON_",
    ]

    COMMON_SUFFIXES = [
        "_ITEM",
        "_SCROLL",
        "_GEM",
        "_ORE",
        "_1",
        "_2",
        "_3",
        "_4",
        "_5",
        "_6",
        "_7",
        "_8",
        "_9",
        "_10",
    ]

    def __init__(self, api_endpoint: str = BAZAAR_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self.last_updated: datetime | None = None
        self.products: dict[str, BazaarProduct] = {}
        self.normalized_product_ids: dict[str, str] = {}
        self._load_bazaar_data()

    def _load_bazaar_data(self) -> None:
        """Fetch the bazaar data from the API."""
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                self.last_updated = convert_timestamp(data.get('lastUpdated'))
                products_data = data.get('products', {})
                for product_id, product_data in products_data.items():
                    self.products[product_id] = BazaarProduct(product_id, product_data)
                    normalized_id = self._normalize_product_id(product_id)
                    self.normalized_product_ids[normalized_id] = product_id
            else:
                raise ValueError("Failed to fetch bazaar data")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred: {e}")

    def _normalize_product_id(self, product_id: str) -> str:
        """Normalize the product ID for easier searching."""
        normalized = product_id.upper()
        for prefix in self.COMMON_PREFIXES:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):]
                break
        for suffix in self.COMMON_SUFFIXES:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]
                break
        normalized = re.sub(r'[^A-Z0-9]', '_', normalized)
        return normalized

    def search_product(self, search_term: str) -> BazaarProduct | None:
        """
        Search for a product using a search term.

        Args:
            search_term (str): The search term provided by the user.

        Returns:
            BazaarProduct or None: The matching BazaarProduct object, or None if not found.
        """
        normalized_search = self._normalize_search_term(search_term)
        product_id = self.normalized_product_ids.get(normalized_search)
        if product_id and product_id in self.products:
            return self.products[product_id]
        possible_ids = self._generate_possible_product_ids(normalized_search)
        for pid in possible_ids:
            if pid in self.products:
                return self.products[pid]
        return self._fuzzy_search(normalized_search)

    def _normalize_search_term(self, search_term: str) -> str:
        """Normalize the search term to match normalized product IDs."""
        normalized = search_term.upper().replace(' ', '_')
        normalized = re.sub(r'[^A-Z0-9]', '_', normalized)
        return normalized

    def _generate_possible_product_ids(self, base_term: str) -> list[str]:
        """Generate possible product IDs by adding common prefixes and suffixes."""
        possible_ids = []
        for prefix in [''] + self.COMMON_PREFIXES:
            term_with_prefix = prefix + base_term
            for suffix in [''] + self.COMMON_SUFFIXES:
                possible_id = term_with_prefix + suffix
                possible_ids.append(possible_id)
        possible_ids = list(set(possible_ids))
        return possible_ids

    # TODO: Potentially consider changing some of this class to be able to search and pass back multiple products
    #   if a search is not clear enough. (e.x. ENCHANTMENT_ULTIMATE_WISDOM_1, ENCHANTMENT_ULTIMATE_WISDOM_2, 
    #   ENCHANTMENT_ULTIMATE_WISDOM_3, etc..)
    def _fuzzy_search(self, normalized_search: str) -> BazaarProduct | None:
        """Perform a simple fuzzy search to find the closest matching product."""
        possible_matches = get_close_matches(
            normalized_search,
            self.normalized_product_ids.keys(),
            n=1,
            cutoff=0.6
        )
        if possible_matches:
            matched_id = self.normalized_product_ids[possible_matches[0]]
            return self.products.get(matched_id)
        return None

    def get_product_by_id(self, product_id: str) -> BazaarProduct | None:
        """
        Retrieve a product by its exact ID.

        Args:
            product_id (str): The exact ID of the product.

        Returns:
            BazaarProduct or None: The BazaarProduct object, or None if not found.
        """
        return self.products.get(product_id)

    def __str__(self) -> str:
        product_ids = ', '.join(self.products.keys())
        return f"Bazaar Data (Last Updated: {self.last_updated})\nProducts: {product_ids}"