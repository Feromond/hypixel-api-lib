from datetime import datetime
from hypixel_api_lib.utils import convert_timestamp

class Crystal:
    """
    Represents a crystal in the Mining Core.

    Attributes:
        state (str): The state of the crystal (e.g., 'FOUND', 'NOT_FOUND').
        total_found (int): The total number of times the crystal was found.
        total_placed (int): The total number of times the crystal was placed.
    """

    def __init__(self, data: dict) -> None:
        self.state: str = data.get('state', '')
        self.total_found: int = data.get('total_found', 0)
        self.total_placed: int = data.get('total_placed', 0)

    def __str__(self) -> str:
        return f"Crystal(state={self.state}, total_found={self.total_found}, total_placed={self.total_placed})"
    
    def __repr__(self) -> str:
        return f"Crystal(state={self.state}, total_found={self.total_found}, total_placed={self.total_placed})"

class Biome:
    """
    Represents a biome in the Mining Core.

    Attributes:
        king_quest_active (bool): Whether the king quest is active.
        king_quests_completed (int): Number of king quests completed.
        jungle_temple_open (bool): Whether the jungle temple is open.
        jungle_temple_chest_uses (int): Number of times the jungle temple chest was used.
    """

    def __init__(self, data: dict) -> None:
        self.king_quest_active: bool = data.get('king_quest_active', False)
        self.king_quests_completed: int = data.get('king_quests_completed', 0)
        self.jungle_temple_open: bool = data.get('jungle_temple_open', False)
        self.jungle_temple_chest_uses: int = data.get('jungle_temple_chest_uses', 0)

    def __str__(self) -> str:
        return (
            f"Biome(king_quest_active={self.king_quest_active}, "
            f"king_quests_completed={self.king_quests_completed}, "
            f"jungle_temple_open={self.jungle_temple_open}, "
            f"jungle_temple_chest_uses={self.jungle_temple_chest_uses})"
        )

class MiningCore:
    """
    Represents the Mining Core data.

    Attributes:
        nodes (dict[str,int]): Nodes and their levels.
        received_free_tier (bool): Whether the free tier was received.
        tokens (int): Number of tokens available.
        powder_mithril (int): Amount of Mithril powder.
        powder_mithril_total (int): Total amount of Mithril powder collected.
        crystals (dict[str,Crystal]): Crystals data.
        experience (float): Experience points.
        tokens_spent (int): Number of tokens spent.
        powder_spent_mithril (int): Amount of Mithril powder spent.
        retroactive_tier2_token (bool): Whether the retroactive tier 2 token was received.
        daily_ores_mined_day_mithril_ore (int): The day count for daily Mithril ore mining.
        daily_ores_mined_mithril_ore (int): Daily Mithril ore mined.
        greater_mines_last_access (datetime): Last access time to Greater Mines.
        biomes (dict[str,Biome]): Biome data.
        powder_gemstone (int): Amount of Gemstone powder.
        powder_gemstone_total (int): Total amount of Gemstone powder collected.
        daily_ores_mined_day_gemstone (int): The day count for daily Gemstone mining.
        daily_ores_mined_gemstone (int): Daily Gemstone mined.
        powder_spent_gemstone (int): Amount of Gemstone powder spent.
        daily_ores_mined_day_glacite (int): The day count for daily Glacite mining.
        daily_ores_mined_glacite (int): Daily Glacite mined.
        powder_glacite (int): Amount of Glacite powder.
        powder_glacite_total (int): Total amount of Glacite powder collected.
        powder_spent_glacite (int): Amount of Glacite powder spent.
        daily_ores_mined (int): Total daily ores mined.
        daily_ores_mined_day (int): The day count for daily ore mining.
    """

    def __init__(self, data: dict) -> None:
        self.nodes: dict[str,int] = data.get('nodes', {})
        self.received_free_tier: bool = data.get('received_free_tier', False)
        self.tokens: int = data.get('tokens', 0)
        self.powder_mithril: int = data.get('powder_mithril', 0)
        self.powder_mithril_total: int = data.get('powder_mithril_total', 0)
        self.crystals: dict[str,Crystal] = {name: Crystal(crystal_data) for name, crystal_data in data.get('crystals', {}).items()}
        self.experience: float = data.get('experience', 0.0)
        self.tokens_spent: int = data.get('tokens_spent', 0)
        self.powder_spent_mithril: int = data.get('powder_spent_mithril', 0)
        self.retroactive_tier2_token: bool = data.get('retroactive_tier2_token', False)
        self.daily_ores_mined_day_mithril_ore: int = data.get('daily_ores_mined_day_mithril_ore', 0)
        self.daily_ores_mined_mithril_ore: int = data.get('daily_ores_mined_mithril_ore', 0)
        self.greater_mines_last_access: datetime | None = convert_timestamp(data.get('greater_mines_last_access'))
        self.biomes: dict[str,Biome] = {name: Biome(biome_data) for name, biome_data in data.get('biomes', {}).items()}
        self.powder_gemstone: int = data.get('powder_gemstone', 0)
        self.powder_gemstone_total: int = data.get('powder_gemstone_total', 0)
        self.daily_ores_mined_day_gemstone: int = data.get('daily_ores_mined_day_gemstone', 0)
        self.daily_ores_mined_gemstone: int = data.get('daily_ores_mined_gemstone', 0)
        self.powder_spent_gemstone: int = data.get('powder_spent_gemstone', 0)
        self.daily_ores_mined_day_glacite: int = data.get('daily_ores_mined_day_glacite', 0)
        self.daily_ores_mined_glacite: int = data.get('daily_ores_mined_glacite', 0)
        self.powder_glacite: int = data.get('powder_glacite', 0)
        self.powder_glacite_total: int = data.get('powder_glacite_total', 0)
        self.powder_spent_glacite: int = data.get('powder_spent_glacite', 0)
        self.daily_ores_mined: int = data.get('daily_ores_mined', 0)
        self.daily_ores_mined_day: int = data.get('daily_ores_mined_day', 0)

    def __str__(self) -> str:
        return (
            f"MiningCore(tokens={self.tokens}, powder_mithril={self.powder_mithril}, "
            f"powder_gemstone={self.powder_gemstone}, experience={self.experience})"
        )
