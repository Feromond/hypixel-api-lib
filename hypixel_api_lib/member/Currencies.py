class Essence:
    """
    Represents a type of essence and its amount.

    Attributes:
        essence_type (str): The type of essence (e.g., 'DRAGON', 'UNDEAD').
        current (int): The current amount of this essence.
    """

    def __init__(self, essence_type, data):
        self.essence_type = essence_type
        self.current = data.get('current', 0)

    def __str__(self):
        return f"{self.essence_type} Essence: {self.current}"

    def __repr__(self):
        return self.__str__()

class Currencies:
    """
    Represents the currencies data for a SkyBlock profile member.

    Attributes:
        coin_purse (float): The amount of coins the player has.
        motes_purse (float): The amount of motes the player has.
        essence (dict of str to Essence): A dictionary of essences by type.
    """

    def __init__(self, data):
        self.coin_purse = data.get('coin_purse', 0.0)
        self.motes_purse = data.get('motes_purse', 0.0)

        essence_data = data.get('essence', {})
        self.essence = {
            essence_type: Essence(essence_type, essence_info)
            for essence_type, essence_info in essence_data.items()
        }

        known_fields = ['coin_purse', 'motes_purse', 'essence']
        self.additional_currencies = {k: v for k, v in data.items() if k not in known_fields}

    def __str__(self):
        essences_str = ', '.join([str(e) for e in self.essence.values()])
        return (f"Currencies(Coin Purse: {self.coin_purse}, Motes Purse: {self.motes_purse}, "
                f"Essences: {essences_str})")

    def __repr__(self):
        return self.__str__()
