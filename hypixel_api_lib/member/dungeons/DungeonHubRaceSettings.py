class DungeonHubRaceSettings:
    """
    The DungeonHubRaceSettings dataclass storing data related to the dungeon hub race settings

    Attributes:
        selected_race (str or None): Currently selected race if exists, else None
        selected_setting (str or None): Current setting if exists, else None
        runback (bool): whether runback is true or set to false, Default False

    """
    def __init__(self, data: dict[str,str | bool]) -> None:
        self.selected_race: str | None = data.get("selected_race", None)
        self.selected_setting: str | None = data.get("selected_seting", None)
        self.runback: bool = data.get("runback", False)

    def __str__(self) -> str:
        return f"Selected Race: {self.selected_race}, Seleced Setting: {self.selected_setting}, Runback: {self.runback}"