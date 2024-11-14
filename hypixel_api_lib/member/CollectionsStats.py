class CollectionItem:
    """
    Represents a single collection item.

    Attributes:
        name (str): The name of the collection item.
        amount (int): The amount collected.
    """
    def __init__(self, name: str, amount: int) -> None:
        self.name: str = name
        self.amount: int = amount

    def __str__(self) -> str:
        return f"CollectionItem(name={self.name}, amount={self.amount})"

    def __repr__(self) -> str:
        return f"CollectionItem(name={self.name}, amount={self.amount})"

class CollectionsStats:
    """
    Represents a collection of collection items.

    Attributes:
        items (dict[str,CollectionItem]): Dictionary of collection items by name.
    """
    def __init__(self, data: dict) -> None:
        self.items: dict[str, CollectionItem] = {}
        self._parse_collections(data)

    def _parse_collections(self, data: dict) -> None:
        """
        Parses the collections data and populates the items dictionary.

        Args:
            data (dict): The data dictionary.
        """
        for name, amount in data.items():
            self.items[name] = CollectionItem(name, amount)

    def get_item(self, name: str) -> CollectionItem | None:
        """
        Retrieves a CollectionItem by name.

        Args:
            name (str): The name of the collection item.

        Returns:
            CollectionItem | None: The CollectionItem instance or None if not found.
        """
        return self.items.get(name)

    def get_total_collections(self) -> int:
        """
        Calculates the total number of collections.

        Returns:
            int: Total number of collections.
        """
        return len(self.items)

    def get_total_amount_collected(self) -> int:
        """
        Calculates the total amount collected across all items.

        Returns:
            int: Total amount collected.
        """
        return sum(item.amount for item in self.items.values())

    def get_top_collections(self, n: int = 5) -> list[CollectionItem]:
        """
        Retrieves the top n collections by amount.

        Args:
            n (int): Number of top collections to retrieve.

        Returns:
            list[CollectionItem]: List of top collection items.
        """
        return sorted(self.items.values(), key=lambda x: x.amount, reverse=True)[:n]

    def __str__(self) -> str:
        items_str = '\n'.join(str(item) for item in self.items.values())
        return f"Collections:\n{items_str}"
