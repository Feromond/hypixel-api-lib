class ItemData:
    """
    Represents the item data for a SkyBlock profile member.

    Attributes:
        soulflow (int): The amount of soulflow the player has.
        favorite_arrow (str): The player's favorite arrow type.
    """

    def __init__(self, data):
        self.soulflow = data.get('soulflow', 0)
        self.favorite_arrow = data.get('favorite_arrow', None)
        self.additional_data = {k: v for k, v in data.items() if k not in ['soulflow', 'favorite_arrow']}

    def __str__(self):
        return f"ItemData(Soulflow: {self.soulflow}, Favorite Arrow: {self.favorite_arrow})"