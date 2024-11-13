class DungeonJournal:
    """
    DungeonJournal data class to handle the data within the dungeon journals.

    Attributes:
        unlocked_journals (list[str]): list of unlocked journals
    """
    def __init__(self, data: dict[str,list[str]]) -> None:
        self.unlocked_journals: list[str] = data.get("unlocked_journals", {})

    def __str__(self) -> str:
        return f"Unlocked Journals: {self.unlocked_journals}"