from datetime import datetime, timezone
import requests

FIRE_SALES_API_URL = "https://api.hypixel.net/skyblock/firesales"

class FireSaleItem:
    """
    Represents a single SkyBlock Fire Sale item.

    Attributes:
        item_id (str): The SkyBlock item ID for this sale.
        start (datetime): The start time of the sale.
        end (datetime): The end time of the sale.
        amount (int): The amount of items available for this sale.
        price (int): The price in Gems for this sale.
    """

    def __init__(self, sale_data):
        self.item_id = sale_data.get('item_id')
        self.start = self._convert_timestamp(sale_data.get('start'))
        self.end = self._convert_timestamp(sale_data.get('end'))
        self.amount = sale_data.get('amount')
        self.price = sale_data.get('price')

    def _convert_timestamp(self, timestamp):
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def is_active(self):
        """
        Check if the fire sale is currently active.

        Returns:
            bool: True if the sale is active, False otherwise.
        """
        now = datetime.now(timezone.utc)
        if self.start is None or self.end is None:
            return False
        return self.start <= now <= self.end

    def time_until_start(self):
        """
        Get the time remaining until the sale starts.

        Returns:
            timedelta or None: Time remaining until the sale starts, or None if the sale has already started.
        """
        now = datetime.now(timezone.utc)
        if self.start is None:
            return None
        if now < self.start:
            return self.start - now
        else:
            return None

    def time_until_end(self):
        """
        Get the time remaining until the sale ends.

        Returns:
            timedelta or None: Time remaining until the sale ends, or None if the sale hasn't started or has ended.
        """
        now = datetime.now(timezone.utc)
        if self.start is None or self.end is None:
            return None
        if now < self.start:
            return None
        elif now < self.end:
            return self.end - now
        else:
            return None

    def __str__(self):
        start_str = self.start.strftime("%Y-%m-%d %H:%M:%S %Z") if self.start else "N/A"
        end_str = self.end.strftime("%Y-%m-%d %H:%M:%S %Z") if self.end else "N/A"
        return (f"Fire Sale Item '{self.item_id}': Starts at {start_str}, Ends at {end_str}, "
                f"Amount: {self.amount}, Price: {self.price} Gems")

class FireSales:
    """
    Manages fetching and storing fire sale data from the Hypixel SkyBlock Fire Sales API.

    Attributes:
        api_endpoint (str): The API endpoint URL.
        sales (list of FireSaleItem): List of active or upcoming fire sales.
    """

    def __init__(self, api_endpoint=FIRE_SALES_API_URL):
        self._api_endpoint = api_endpoint
        self.sales = self._get_fire_sales()

    def _get_fire_sales(self):
        """
        Fetch the active or upcoming fire sales.

        Returns:
            list of FireSaleItem: A list of fire sale items.
        """
        try:
            response = requests.get(self._api_endpoint)
            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                sales_data = data.get('sales', [])
                sales = [FireSaleItem(sale) for sale in sales_data]
                return sales
            else:
                raise ValueError("API response was not successful")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching fire sales: {e}")

    def get_sale_by_item_id(self, item_id):
        """
        Retrieve a fire sale by its item ID.

        Args:
            item_id (str): The item ID of the fire sale.

        Returns:
            FireSaleItem or None: The fire sale item, or None if not found.
        """
        return next((sale for sale in self.sales if sale.item_id == item_id), None)

    def get_active_sales(self):
        """
        Get all currently active fire sales.

        Returns:
            list of FireSaleItem: A list of active fire sale items.
        """
        return [sale for sale in self.sales if sale.is_active()]

    def get_upcoming_sales(self):
        """
        Get all upcoming fire sales that have not started yet.

        Returns:
            list of FireSaleItem: A list of upcoming fire sale items.
        """
        now = datetime.now(timezone.utc)
        return [sale for sale in self.sales if sale.start > now]

    def __str__(self):
        return f"FireSales with {len(self.sales)} active/upcoming sales"
