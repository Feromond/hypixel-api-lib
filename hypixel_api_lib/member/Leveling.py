class ExperienceData:
    """
    Represents the experience points of the player.

    Attributes:
        experience (int): The player's total experience points.
    """
    def __init__(self, experience: int) -> None:
        self.experience: int = experience

    def __str__(self) -> str:
        return f"ExperienceData(Experience: {self.experience})"


class CompletionsData:
    """
    Represents completion milestones achieved by the player.

    Attributes:
        completions (dict): Dictionary mapping completion types to their values.
    """
    def __init__(self, completions: dict) -> None:
        self.completions = completions

    def __str__(self) -> str:
        return f"CompletionsData({self.completions})"


class TaskData:
    """
    Represents the list of tasks the player has completed.

    Attributes:
        completed_tasks (list): List of strings representing completed tasks.
    """
    def __init__(self, completed_tasks: list[str]) -> None:
        self.completed_tasks: list[str] = completed_tasks

    def __str__(self) -> str:
        return f"TaskData(Completed Tasks: {len(self.completed_tasks)})"


class PetScore:
    """
    Represents the player's highest pet score.

    Attributes:
        highest_pet_score (int): The highest score the player has achieved with pets.
    """
    def __init__(self, highest_pet_score: int) -> None:
        self.highest_pet_score: int = highest_pet_score

    def __str__(self) -> str:
        return f"PetScore(Highest Pet Score: {self.highest_pet_score})"


class MigrationData:
    """
    Represents migration details, tracking data transitions.

    Attributes:
        migrated (bool): Indicates if the player data was migrated.
        migrated_completions_2 (bool): Indicates if the second phase of migration is complete.
    """
    def __init__(self, migrated: bool, migrated_completions_2: bool) -> None:
        self.migrated: bool = migrated
        self.migrated_completions_2: bool = migrated_completions_2

    def __str__(self) -> None:
        return f"MigrationData(Migrated: {self.migrated}, Migrated Completions 2: {self.migrated_completions_2})"


class TaskViews:
    """
    Represents the list of tasks recently viewed by the player.

    Attributes:
        last_viewed_tasks (list): List of strings representing recently viewed tasks.
    """
    def __init__(self, last_viewed_tasks: list[str]) -> None:
        self.last_viewed_tasks: list[str] = last_viewed_tasks

    def __str__(self) -> str:
        return f"TaskViews(Last Viewed Tasks: {self.last_viewed_tasks})"


class EventStats:
    """
    Represents statistics related to special in-game events.

    Attributes:
        fishing_festival_sharks_killed (int): Number of sharks killed during the fishing festival.
        mining_fiesta_ores_mined (int): Number of ores mined during the mining fiesta.
    """
    def __init__(self, fishing_festival_sharks_killed: int, mining_fiesta_ores_mined: int) -> None:
        self.fishing_festival_sharks_killed: int = fishing_festival_sharks_killed
        self.mining_fiesta_ores_mined: int = mining_fiesta_ores_mined

    def __str__(self) -> str:
        return (f"EventStats(Fishing Festival Sharks Killed: {self.fishing_festival_sharks_killed}, "
                f"Mining Fiesta Ores Mined: {self.mining_fiesta_ores_mined})")


class SymbolData:
    """
    Represents data related to player's selected symbol, bonuses, and additional status flags.

    Attributes:
        selected_symbol (str): The currently selected symbol for the player.
        bop_bonus (str): The bonus effect currently active for the player.
        claimed_talisman (bool): Indicates if the player has claimed the talisman.
        category_expanded (bool): Indicates if the player's category is expanded.
    """
    def __init__(self, selected_symbol: str, bop_bonus: str, claimed_talisman: bool, category_expanded: bool) -> None:
        self.selected_symbol: str = selected_symbol
        self.bop_bonus: str = bop_bonus
        self.claimed_talisman: bool = claimed_talisman
        self.category_expanded: bool = category_expanded

    def __str__(self) -> str:
        return (f"SymbolData(Selected Symbol: {self.selected_symbol}, Bop Bonus: {self.bop_bonus}, "
                f"Claimed Talisman: {self.claimed_talisman}, Category Expanded: {self.category_expanded})")


class LevelingData:
    """
    Represents the leveling data for a SkyBlock profile member, broken down into specific components.

    Attributes:
        experience_data (ExperienceData): Tracks total experience points.
        completions_data (CompletionsData): Holds details about completion milestones.
        task_data (TaskData): Manages completed tasks.
        pet_score (PetScore): Stores the player's highest pet score.
        migration_data (MigrationData): Holds migration-related data.
        task_views (TaskViews): Tracks tasks recently viewed by the player.
        event_stats (EventStats): Holds statistics related to special events.
        symbol_data (SymbolData): Stores selected symbol, bonus, and other related attributes.
    """

    def __init__(self, data: dict) -> None:
        self.experience_data: ExperienceData = ExperienceData(data.get('experience', 0))
        self.completions_data: CompletionsData = CompletionsData(data.get('completions', {}))
        self.task_data: TaskData = TaskData(data.get('completed_tasks', []))
        self.pet_score: PetScore = PetScore(data.get('highest_pet_score', 0))
        self.migration_data: MigrationData = MigrationData(data.get('migrated', False), data.get('migrated_completions_2', False))
        self.task_views: TaskViews = TaskViews(data.get('last_viewed_tasks', []))
        self.event_stats: EventStats = EventStats(data.get('fishing_festival_sharks_killed', 0), data.get('mining_fiesta_ores_mined', 0))
        self.symbol_data: SymbolData = SymbolData(data.get('selected_symbol', ''), data.get('bop_bonus', ''),
                                      data.get('claimed_talisman', False), data.get('category_expanded', False))

    def __str__(self) -> str:
        return (f"LevelingData(\n"
                f"  {self.experience_data},\n"
                f"  {self.completions_data},\n"
                f"  {self.task_data},\n"
                f"  {self.pet_score},\n"
                f"  {self.migration_data},\n"
                f"  {self.task_views},\n"
                f"  {self.event_stats},\n"
                f"  {self.symbol_data}\n"
                f")")
