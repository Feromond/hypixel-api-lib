class GardenPlayerData:
    """
    Represents garden-related data for a SkyBlock profile member.

    Attributes:
        copper (int): The amount of copper collected by the player.
        larva_consumed (int): The number of larva consumed by the player.
    """

    def __init__(self, data: dict) -> None:
        self.copper: int = data.get('copper', 0)
        self.larva_consumed: int = data.get('larva_consumed', 0)

    def __str__(self) -> str:
        return f"GardenPlayerData(Copper: {self.copper}, Larva Consumed: {self.larva_consumed})"
