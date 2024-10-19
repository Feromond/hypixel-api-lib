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
        color (str, optional): The color metadata to be applied to the item.
        skin (str, optional): The skin value for a skull-based item.
    """
    
    def __init__(self, id, material, name, tier, color=None, skin=None):
        self.id = id
        self.material = material
        self.name = name
        self.tier = tier if tier is not None else 'UNKNOWN'
        self.color = color
        self.skin = skin

    def __str__(self):
        return f"{self.name} ({self.tier}): ID={self.id}, Material={self.material}"

class Items:
    """
    Handles fetching and managing all the items from the API.
    
    Attributes:
        api_endpoint (str): The endpoint URL to fetch the items data.
        items (dict of str: SkyBlockItem): A dictionary of item IDs to SkyBlockItem objects.
    """
    
    def __init__(self, api_endpoint=ITEMS_API_URL):
        self.api_endpoint = api_endpoint
        self.items = None   # Will be dict
        self._load_items()

    def _load_items(self):
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
                        color=item_data.get('color'),
                        skin=item_data.get('skin')
                    )
                    self.items[item.id] = item
            else:
                raise ValueError("No items data available in the response")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_item(self, item_id):
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

    def get_items_by_tier(self, tier):
        """
        Retrieve all items that have a specific tier.
        
        Args:
            tier (str): The tier to filter items by.

        Returns:
            dict of str: SkyBlockItem: A dictionary of item IDs to SkyBlockItem objects where the tier matches.
        """
        return {item_id: item for item_id, item in self.items.items() if item.tier.upper() == tier.upper()}

    def list_item_names(self):
        """
        List all available item names.
        
        Returns:
            list of str: A list of all item names.
        """
        return [item.name for item in self.items.values()]
