from .PlayerClasses import PlayerClasses

class Dungeons():
    """
    The dungeons class to handle and store all dungeon related data for a SkyBlockProfileMember

    Attributes:
        dungeon_types (DungeonTypes): ...
    """

    def __init__(self, dungeons_data: dict) -> None:
        self.dungeons_data = dungeons_data

        self.dungeon_types: dict = dungeons_data.get("dungeon_types", {})                       # Huge
        self.player_classes: PlayerClasses = PlayerClasses(dungeons_data.get("player_classes", {})) 
        self.dungeon_journal: dict[str,list[str]] = dungeons_data.get("dungeon_journal", {}) 
        self.dungeons_blah_blah: list[str] = dungeons_data.get("dungeons_blah_blah", [])
        self.selected_dungeon_class: str | None = dungeons_data.get("selected_dungeon_class", None)
        self.daily_runs: dict[str,int] = dungeons_data.get("daily_runs", {})
        self.treasures: dict = dungeons_data.get("treasures", {})                               # Huge
        self.dungeon_hub_race_settings: dict[str,str] = dungeons_data.get("dungeon_hub_race_settings", {}) 
        self.last_dungeon_run: str | None = dungeons_data.get("last_dungeon_run", None)
        self.secrets: int = dungeons_data.get("secrets", 0)


    def __str__(self) -> str:
        return f"Dungeons Data Class containing: {self.dungeons_data.keys()}"