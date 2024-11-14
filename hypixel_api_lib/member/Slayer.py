from hypixel_api_lib.utils import convert_timestamp
from datetime import datetime

class SlayerBoss:
    """
    Represents a generic slayer boss with common attributes.

    Attributes:
        claimed_levels (dict[str,bool]): Dictionary of claimed levels.
        boss_kills (dict[int,int]): Dictionary of boss kills per tier.
        boss_attempts (dict[int,int]): Dictionary of boss attempts per tier.
        xp (int): Total experience gained from this slayer boss.
    """

    def __init__(self, data: dict) -> None:
        self.claimed_levels: dict[str, bool] = data.get('claimed_levels', {})
        self.xp: int = data.get('xp', 0)
        self.boss_kills: dict[int,int] = self._extract_tier_data(data, 'boss_kills_tier_')
        self.boss_attempts: dict[int,int] = self._extract_tier_data(data, 'boss_attempts_tier_')

    @staticmethod
    def _extract_tier_data(data: dict, prefix: str) -> dict[int,int]:
        """
        Extracts boss kills or attempts per tier.

        Args:
            data (dict): The data dictionary.
            prefix (str): The prefix to look for in keys.

        Returns:
            dict[int,int]: A dictionary with tier as key and count as value.
        """
        result = {}
        for key, value in data.items():
            if key.startswith(prefix):
                tier = int(key[len(prefix):])
                result[tier] = value
        return result

    def total_boss_kills(self) -> int:
        """
        Calculates the total number of boss kills.

        Returns:
            int: Total boss kills.
        """
        return sum(self.boss_kills.values())

    def __str__(self) -> str:
        return (
            f"SlayerBoss(claimed_levels={self.claimed_levels}, xp={self.xp}, "
            f"boss_kills={self.boss_kills}, boss_attempts={self.boss_attempts})"
        )


class SlayerQuest:
    """
    Represents the current active slayer quest.

    Attributes:
        type (str): Type of the slayer quest.
        tier (int): Tier level of the quest.
        start_timestamp (datetime): When the quest was started.
        completion_state (int): Completion state of the quest.
        used_armor (bool): Whether special armor was used.
        solo (bool): Whether the quest is solo.
        combat_xp (int): Combat XP gained.
        recent_mob_kills (list[dict[str,any]]): Recent mob kills with details.
        last_killed_mob_island (str): The island where the last mob was killed.
    """

    def __init__(self, data: dict) -> None:
        self.type: str = data.get('type', '')
        self.tier: int = data.get('tier', 0)
        self.start_timestamp: datetime | None = convert_timestamp(data.get('start_timestamp'))
        self.completion_state: int = data.get('completion_state', 0)
        self.used_armor: bool = data.get('used_armor', False)
        self.solo: bool = data.get('solo', True)
        self.combat_xp: int = data.get('combat_xp', 0)
        self.recent_mob_kills: list[dict[str,any]] = data.get('recent_mob_kills', [])
        self.last_killed_mob_island: str = data.get('last_killed_mob_island', '')


    def __str__(self) -> str:
        return (
            f"SlayerQuest(type={self.type}, tier={self.tier}, start_timestamp={self.start_timestamp}, "
            f"completion_state={self.completion_state}, used_armor={self.used_armor}, solo={self.solo}, "
            f"combat_xp={self.combat_xp}, recent_mob_kills={self.recent_mob_kills}, "
            f"last_killed_mob_island={self.last_killed_mob_island})"
        )


class Slayer:
    """
    Represents the player's slayer statistics.

    Attributes:
        slayer_quest (SlayerQuest | None): The current active slayer quest.
        slayer_bosses (dict[str,SlayerBoss]): Dictionary of slayer bosses.
    """

    def __init__(self, data: dict) -> None:
        self.slayer_quest: SlayerQuest | None = None
        if 'slayer_quest' in data:
            self.slayer_quest = SlayerQuest(data['slayer_quest'])

        self.slayer_bosses: dict[str,SlayerBoss] = {}
        slayer_bosses_data = data.get('slayer_bosses', {})
        for boss_type, boss_data in slayer_bosses_data.items():
            self.slayer_bosses[boss_type] = SlayerBoss(boss_data)

    def total_xp(self) -> int:
        """
        Calculates the total slayer XP across all bosses.

        Returns:
            int: Total slayer XP.
        """
        return sum(boss.xp for boss in self.slayer_bosses.values())

    def __str__(self) -> str:
        bosses_str = ', '.join(f"{k}: {v}" for k, v in self.slayer_bosses.items())
        return (
            f"SlayerStats(slayer_quest={self.slayer_quest}, slayer_bosses={{ {bosses_str} }})"
        )
