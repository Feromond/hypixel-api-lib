from .PlayerClasses import PlayerClasses
from .DungeonJournal import DungeonJournal
from .DailyRuns import DailyRuns
from .DungeonHubRaceSettings import DungeonHubRaceSettings
from .DungeonTypes import DungeonTypes
from .Treasures import Treasures

class Dungeons:
    """
    Handles and stores all dungeon-related data for a SkyBlock profile member.

    Attributes:
        dungeon_types (DungeonTypes): Represents the types of dungeons and their respective data.
        player_classes (PlayerClasses): Contains information about the player's dungeon classes.
        dungeon_journal (DungeonJournal): Holds the player's dungeon journal entries.
        dungeons_blah_blah (list of str): List NPC's the member has talked to.
        selected_dungeon_class (str or None): The class selected by the player for dungeons (e.g., 'Mage', 'Healer').
        daily_runs (DailyRuns): Contains data about the player's daily dungeon runs.
        treasures (Treasures): Represents the treasures (runs and chests) acquired in dungeons.
        dungeon_hub_race_settings (DungeonHubRaceSettings): Settings related to the Dungeon Hub races.
        last_dungeon_run (str or None): Timestamp or identifier of the player's last dungeon run.
        secrets (int): The total number of secrets found by the player in dungeons.
    """
    def __init__(self, dungeons_data: dict) -> None:
        self.dungeons_data: dict = dungeons_data

        self.dungeon_types: DungeonTypes = DungeonTypes(dungeons_data.get("dungeon_types", {}))
        self.player_classes: PlayerClasses = PlayerClasses(dungeons_data.get("player_classes", {})) 
        self.dungeon_journal: DungeonJournal = DungeonJournal(dungeons_data.get("dungeon_journal", {}))
        self.dungeons_blah_blah: list[str] = dungeons_data.get("dungeons_blah_blah", [])
        self.selected_dungeon_class: str | None = dungeons_data.get("selected_dungeon_class", None)
        self.daily_runs: DailyRuns = DailyRuns(dungeons_data.get("daily_runs", {}))
        self.treasures: Treasures = Treasures(dungeons_data.get("treasures", {}))
        self.dungeon_hub_race_settings: DungeonHubRaceSettings =  DungeonHubRaceSettings(dungeons_data.get("dungeon_hub_race_settings", {}))
        self.last_dungeon_run: str | None = dungeons_data.get("last_dungeon_run", None)
        self.secrets: int = dungeons_data.get("secrets", 0)


    def __str__(self) -> str:
        return f"Dungeons Data Class containing: {self.dungeons_data.keys()}"