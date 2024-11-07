from datetime import datetime, timezone

class Perk:
    """
    Represents a perk and its level.

    Attributes:
        name (str): The name of the perk.
        level (int): The level of the perk.
    """

    def __init__(self, name: str, level: int) -> None:
        self.name: str = name
        self.level: int = level

    def __str__(self) -> str:
        return f"{self.name}: Level {self.level}"

class SkillExperience:
    """
    Represents experience in a specific skill.

    Attributes:
        skill_name (str): The name of the skill.
        experience (float): The amount of experience in the skill.
    """

    def __init__(self, skill_name: str, experience: float) -> None:
        self.skill_name: str = skill_name
        self.experience: float = experience

    def __str__(self) -> str:
        return f"{self.skill_name}: {self.experience} XP"
    
    def __repr__(self) -> str:
        return f"{self.skill_name}: {self.experience} XP"


class PlayerData:
    """
    Represents the player data for a SkyBlock profile member.

    Attributes:
        visited_zones (list of str): List of zones the player has visited.
        last_death (datetime): Datetime of the player's last death.
        perks (dict of str to int): Perks and their levels.
        active_effects (list): List of active effects.
        paused_effects (list): List of paused effects.
        temp_stat_buffs (list): List of temporary stat buffs.
        death_count (int): Total number of deaths.
        disabled_potion_effects (list of str): List of disabled potion effects.
        achievement_spawned_island_types (list of str): List of spawned island types for achievements.
        visited_modes (list of str): List of game modes the player has visited.
        unlocked_coll_tiers (list of str): List of unlocked collection tiers.
        crafted_generators (list of str): List of crafted generators.
        fastest_target_practice (float): Fastest time in target practice.
        fishing_treasure_caught (int): Number of fishing treasures caught.
        experience (dict of str to float): Experience in various skills.
    """

    def __init__(self, data: dict) -> None:
        self.visited_zones: list = data.get('visited_zones', [])
        self.last_death: datetime | None = self._convert_timestamp(data.get('last_death'))
        self.perks: dict[str,int] = self._parse_perks(data.get('perks', {}))
        self.active_effects: list = data.get('active_effects', [])
        self.paused_effects: list = data.get('paused_effects', [])
        self.temp_stat_buffs: list = data.get('temp_stat_buffs', [])
        self.death_count: int = data.get('death_count', 0)
        self.disabled_potion_effects: list[str] = data.get('disabled_potion_effects', [])
        self.achievement_spawned_island_types: list[str] = data.get('achievement_spawned_island_types', [])
        self.visited_modes: list[str] = data.get('visited_modes', [])
        self.unlocked_coll_tiers: list[str] = data.get('unlocked_coll_tiers', [])
        self.crafted_generators: list[str] = data.get('crafted_generators', [])
        self.fastest_target_practice: float | None = data.get('fastest_target_practice', None)
        self.fishing_treasure_caught: int = data.get('fishing_treasure_caught', 0)
        self.experience: dict[str,float] = self._parse_experience(data.get('experience', {}))

    @staticmethod
    def _convert_timestamp(timestamp: int | None) -> datetime | None:
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None
    
    def _parse_perks(self, perks_dict:dict) -> list[Perk]:
        """Convert the perks dictionary into a list of Perk objects."""
        return [Perk(name, level) for name, level in perks_dict.items()]

    def _parse_experience(self, experience_dict: dict) -> list[SkillExperience]:
        """Convert the experience dictionary into a list of SkillExperience objects."""
        return [SkillExperience(skill, xp) for skill, xp in experience_dict.items()]

    def __str__(self) -> str:
        last_death_str = self.last_death.strftime('%Y-%m-%d %H:%M:%S') if self.last_death else 'N/A'
        return (f"PlayerData(Deaths: {self.death_count}, Last Death: {last_death_str}, "
                f"Visited Zones: {len(self.visited_zones)}, Experience: {self.experience})")