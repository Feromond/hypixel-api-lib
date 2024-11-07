import requests

ITEMS_API_URL = r"https://api.hypixel.net/v2/resources/skyblock/items"

class SkyBlockItem:
    """
    Represents an item in SkyBlock.

    Attributes:
        id (str): The unique identifier for the item.
        material (str): The Bukkit material enum value for the item.
        name (str): The name of the item.
        tier (str): The rarity tier of the item.
        category (str, optional): The category of the item.
        stats (dict, optional): The stats of the item (e.g., DEFENSE, HEALTH).
        npc_sell_price (int, optional): The NPC sell price of the item.
        color (str, optional): The color metadata to be applied to the item.
        skin (str, optional): The skin value for a skull-based item.
        durability (int, optional): The durability of the item.
    """

    def __init__(
        self,
        id: str,
        material: str,
        name: str,
        tier: str | None = None,
        category: str | None = None,
        stats: dict | None = None,
        npc_sell_price: int | None = None,
        color: str | None = None,
        skin: str | None = None,
        durability: int | None = None,
    ) -> None:
        self.id: str = id
        self.material: str = material
        self.name: str = name
        self.tier: str = tier if tier is not None else 'UNKNOWN'
        self.category: str | None = category
        self.stats: dict = stats or {}
        self.npc_sell_price: int | None = npc_sell_price
        self.color: str | None = color
        self.skin: str | None = skin
        self.durability: int | None = durability

    def __str__(self) -> str:
        return f"{self.name} ({self.tier}): ID={self.id}, Material={self.material}"
    
    def get_formatted_stats(self) -> str:
        if not self.stats:
            return "No stats available."
        return ', '.join(f"{key}: {value}" for key, value in self.stats.items())

class Items:
    """
    Handles fetching and managing all the items from the API.
    
    Attributes:
        api_endpoint (str): The endpoint URL to fetch the items data.
        items (dict of [str: SkyBlockItem]): A dictionary of item IDs to SkyBlockItem objects.
    """
    
    def __init__(self, api_endpoint: str = ITEMS_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self.items: dict[str,SkyBlockItem] | None = None
        self._load_items()

    def _load_items(self) -> None:
        """Fetch items data from the API and initialize SkyBlockItem objects."""
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            data = response.json()
            
            if "items" in data and data["items"]:
                self.items = {}
                for item_data in data["items"]:
                    item = SkyBlockItem(
                        id=item_data.get('id'),
                        material=item_data.get('material'),
                        name=item_data.get('name'),
                        tier=item_data.get('tier'),
                        category=item_data.get('category'),
                        stats=item_data.get('stats'),
                        npc_sell_price=item_data.get('npc_sell_price'),
                        color=item_data.get('color'),
                        skin=item_data.get('skin'),
                        durability=item_data.get('durability'),
                    )
                    self.items[item.id] = item
            else:
                raise ValueError("No items data available in the response")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred: {e}")

    def get_item(self, item_id: str) -> SkyBlockItem | str:
        """
        Retrieve an item by its ID.
        
        Args:
            item_id (str): The ID of the item to retrieve.

        Returns:
            SkyBlockItem or str: The SkyBlockItem object, or an error message if the item is not found.
        """
        item = self.items.get(item_id)
        if item:
            return item
        else:
            return f"Item '{item_id}' not found."

    def get_items_by_tier(self, tier: str) -> dict[str,SkyBlockItem]:
        """
        Retrieve all items that have a specific tier.
        
        Args:
            tier (str): The tier to filter items by.

        Returns:
            dict of str: SkyBlockItem: A dictionary of item IDs to SkyBlockItem objects where the tier matches.
        """
        return {
            item_id: item
            for item_id, item in self.items.items()
            if item.tier is not None and item.tier.upper() == tier.upper()
        }

    def get_items_by_category(self, category: str) -> dict[str,SkyBlockItem]:
        """
        Retrieve all items that belong to a specific category.
        
        Args:
            category (str): The category to filter items by.

        Returns:
            dict of str: SkyBlockItem: A dictionary of item IDs to SkyBlockItem objects where the category matches.
        """
        return {
            item_id: item
            for item_id, item in self.items.items()
            if item.category is not None and item.category.upper() == category.upper()
        }


    def list_item_names(self) -> list[str]:
        """
        List all available item names.

        Returns:
            list of str: A list of all item names.
        """
        return [item.name for item in self.items.values()]


    def list_item_categories(self) -> list[str]:
        """
        List all unique item categories.

        Returns:
            list of str: A sorted list of all unique item categories.
        """
        categories = {item.category for item in self.items.values() if item.category}
        return sorted(categories)
