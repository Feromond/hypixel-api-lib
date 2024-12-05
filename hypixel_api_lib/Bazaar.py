from datetime import datetime
import requests
from hypixel_api_lib.utils import convert_timestamp

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
    """

    def __init__(self, api_endpoint: str = BAZAAR_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self.last_updated: datetime | None = None
        self.products: dict[str, BazaarProduct] = {}
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
            else:
                raise ValueError("Failed to fetch bazaar data")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred: {e}")

    def get_product_by_id(self, product_id: str) -> BazaarProduct | None:
        """
        Retrieve a product by its ID.

        Args:
            product_id (str): The ID of the product.

        Returns:
            BazaarProduct or None: The BazaarProduct object, or None if not found.
        """
        return self.products.get(product_id)

    def __str__(self) -> str:
        product_ids = ', '.join(self.products.keys())
        return f"Bazaar Data (Last Updated: {self.last_updated})\nProducts: {product_ids}"
