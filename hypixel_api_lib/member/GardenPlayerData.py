class GardenPlayerData:
    """
    Represents garden-related data for a SkyBlock profile member.

    Attributes:
        copper (int): The amount of copper collected by the player.
        larva_consumed (int): The number of larva consumed by the player.
    """

    def __init__(self, data):
        self.copper = data.get('copper', 0)
        self.larva_consumed = data.get('larva_consumed', 0)

    def __str__(self):
        return f"GardenPlayerData(Copper: {self.copper}, Larva Consumed: {self.larva_consumed})"
