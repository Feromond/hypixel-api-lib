from datetime import datetime
import requests
from hypixel_api_lib.utils import convert_timestamp

COLLECTIONS_API_URL = r"https://api.hypixel.net/v2/resources/skyblock/collections"

class CollectionTier:
    """
    Represents a tier within a collection item.

    Attributes:
        tier (int): The tier number.
        amount_required (int): The amount required to reach this tier.
        unlocks (list of str): The unlocks provided at this tier.
    """
    def __init__(self, tier_data: dict) -> None:
        self.tier: int = tier_data.get('tier')
        self.amount_required: int = tier_data.get('amountRequired')
        self.unlocks: list[str] = tier_data.get('unlocks', [])

    def __str__(self) -> str:
        return f"Tier {self.tier}: Requires {self.amount_required}, Unlocks: {', '.join(self.unlocks)}"

class CollectionItem:
    """
    Represents an item within a collection category.

    Attributes:
        key (str): The item key.
        name (str): The item name.
        max_tiers (int): The maximum number of tiers for this item.
        tiers (list of CollectionTier): The tiers of the item.
    """
    def __init__(self, item_key: str, item_data: dict) -> None:
        self.key: str = item_key
        self.name: str = item_data.get('name', 'Unknown Item')
        self.max_tiers: int = item_data.get('maxTiers', 0)
        self.tiers: list[CollectionTier] = [CollectionTier(tier) for tier in item_data.get('tiers', [])]

    def get_tier(self, tier_number: int) -> CollectionTier | None:
        """
        Retrieve a specific tier by its number.

        Args:
            tier_number (int): The tier number.

        Returns:
            CollectionTier or None: The CollectionTier object, or None if not found.
        """
        return next((tier for tier in self.tiers if tier.tier == tier_number), None)

    def __str__(self) -> str:
        return f"Collection Item: {self.name} (Key: {self.key}), Max Tiers: {self.max_tiers}"

class CollectionCategory:
    """
    Represents a collection category, such as 'FARMING', 'MINING', etc.

    Attributes:
        key (str): The category key.
        name (str): The category name.
        items (dict of str to CollectionItem): The items in the category.
    """
    def __init__(self, category_key: str, category_data: dict) -> None:
        self.key: str = category_key
        self.name: str = category_data.get('name', 'Unknown Category')
        self.items: dict[str,CollectionItem] = {}
        items_data = category_data.get('items', {})
        for item_key, item_data in items_data.items():
            self.items[item_key] = CollectionItem(item_key, item_data)

    def get_item_by_key(self, item_key: str) -> CollectionItem | None:
        """
        Retrieve an item by its key.

        Args:
            item_key (str): The key of the item.

        Returns:
            CollectionItem or None: The CollectionItem object, or None if not found.
        """
        return self.items.get(item_key)

    def get_item_by_name(self, item_name: str) -> CollectionItem | None:
        """
        Retrieve an item by its name.

        Args:
            item_name (str): The name of the item.

        Returns:
            CollectionItem or None: The CollectionItem object, or None if not found.
        """
        return next((item for item in self.items.values() if item.name.lower() == item_name.lower()), None)

    def __str__(self) -> str:
        return f"Collection Category: {self.name} (Key: {self.key}), Items: {len(self.items)}"

class Collections:
    """
    Manages fetching and storing the collections data from the API.

    Attributes:
        last_updated (datetime): The timestamp of the last update.
        version (str): The version of the data.
        categories (dict of str to CollectionCategory): The collection categories.
    """
    def __init__(self, api_endpoint: str = COLLECTIONS_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self.last_updated: datetime | None = None
        self.version: str = ''
        self.categories: dict[str,CollectionCategory] = {}
        self._load_collections_data()

    def _load_collections_data(self) -> None:
        """Fetch the collections data from the API."""
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                self.last_updated = convert_timestamp(data.get('lastUpdated'))
                self.version = data.get('version', '')
                collections_data = data.get('collections', {})
                for category_key, category_data in collections_data.items():
                    self.categories[category_key] = CollectionCategory(category_key, category_data)
            else:
                raise ValueError("Failed to fetch collections data")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred: {e}")

    def get_category_by_key(self, category_key: str) -> CollectionCategory | None:
        """
        Retrieve a collection category by its key.

        Args:
            category_key (str): The key of the category.

        Returns:
            CollectionCategory or None: The CollectionCategory object, or None if not found.
        """
        return self.categories.get(category_key)

    def get_category_by_name(self, category_name: str) -> CollectionCategory | None:
        """
        Retrieve a collection category by its name.

        Args:
            category_name (str): The name of the category.

        Returns:
            CollectionCategory or None: The CollectionCategory object, or None if not found.
        """
        return next((category for category in self.categories.values() if category.name.lower() == category_name.lower()), None)

    def get_item_by_key(self, item_key: str) -> CollectionItem | None:
        """
        Retrieve an item across all categories by its key.

        Args:
            item_key (str): The key of the item.

        Returns:
            CollectionItem or None: The CollectionItem object, or None if not found.
        """
        for category in self.categories.values():
            item = category.get_item_by_key(item_key)
            if item:
                return item
        return None

    def get_item_by_name(self, item_name: str) -> CollectionItem | None:
        """
        Retrieve an item across all categories by its name.

        Args:
            item_name (str): The name of the item.

        Returns:
            CollectionItem or None: The CollectionItem object, or None if not found.
        """
        for category in self.categories.values():
            item = category.get_item_by_name(item_name)
            if item:
                return item
        return None

    def __str__(self) -> str:
        categories_str = ', '.join([category.name for category in self.categories.values()])
        return f"Collections Data (Version: {self.version}, Last Updated: {self.last_updated})\nCategories: {categories_str}"
