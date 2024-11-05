class GlacitePlayerData:
    """
    Represents the glacite player data for a SkyBlock profile member.

    Attributes:
        fossils_donated (list of str): List of fossils donated.
        fossil_dust (float): Amount of fossil dust.
        corpses_looted (dict of str to int): Mapping of corpse types to the number looted.
        mineshafts_entered (int): Number of mineshafts entered.
    """

    def __init__(self, data):
        self.fossils_donated = data.get('fossils_donated', [])
        self.fossil_dust = data.get('fossil_dust', 0.0)
        self.corpses_looted = data.get('corpses_looted', {})
        self.mineshafts_entered = data.get('mineshafts_entered', 0)

    def __str__(self):
        return (f"GlacitePlayerData(Fossils Donated: {self.fossils_donated}, "
                f"Fossil Dust: {self.fossil_dust}, Corpses Looted: {self.corpses_looted}, "
                f"Mineshafts Entered: {self.mineshafts_entered})")
