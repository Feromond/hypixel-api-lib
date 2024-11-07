class Essence:
    """
    Represents a type of essence and its amount.

    Attributes:
        essence_type (str): The type of essence (e.g., 'DRAGON', 'UNDEAD').
        current (int): The current amount of this essence.
    """

    def __init__(self, essence_type: str, data: dict) -> None:
        self.essence_type: str = essence_type
        self.current: int = data.get('current', 0)

    def __str__(self) -> str:
        return f"{self.essence_type} Essence: {self.current}"

    def __repr__(self) -> str:
        return self.__str__()

class Currencies:
    """
    Represents the currencies data for a SkyBlock profile member.

    Attributes:
        coin_purse (float): The amount of coins the player has.
        motes_purse (float): The amount of motes the player has.
        essence (dict of str to Essence): A dictionary of essences by type.
    """

    def __init__(self, data: dict) -> None:
        self.coin_purse: float = data.get('coin_purse', 0.0)
        self.motes_purse: float = data.get('motes_purse', 0.0)

        essence_data: dict = data.get('essence', {})
        self.essence: dict[str,Essence] = {
            essence_type: Essence(essence_type, essence_info)
            for essence_type, essence_info in essence_data.items()
        }

        known_fields: list[str] = ['coin_purse', 'motes_purse', 'essence']
        self.additional_currencies: dict[str,str] = {k: v for k, v in data.items() if k not in known_fields}

    def __str__(self) -> str:
        essences_str = ', '.join([str(e) for e in self.essence.values()])
        return (f"Currencies(Coin Purse: {self.coin_purse}, Motes Purse: {self.motes_purse}, "
                f"Essences: {essences_str})")

    def __repr__(self) -> str:
        return self.__str__()
