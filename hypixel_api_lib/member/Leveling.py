class ExperienceData:
    def __init__(self, experience):
        self.experience = experience

    def __str__(self):
        return f"ExperienceData(Experience: {self.experience})"


class CompletionsData:
    def __init__(self, completions):
        self.completions = completions

    def __str__(self):
        return f"CompletionsData({self.completions})"


class TaskData:
    def __init__(self, completed_tasks):
        self.completed_tasks = completed_tasks

    def __str__(self):
        return f"TaskData(Completed Tasks: {len(self.completed_tasks)})"


class PetScore:
    def __init__(self, highest_pet_score):
        self.highest_pet_score = highest_pet_score

    def __str__(self):
        return f"PetScore(Highest Pet Score: {self.highest_pet_score})"


class MigrationData:
    def __init__(self, migrated, migrated_completions_2):
        self.migrated = migrated
        self.migrated_completions_2 = migrated_completions_2

    def __str__(self):
        return f"MigrationData(Migrated: {self.migrated}, Migrated Completions 2: {self.migrated_completions_2})"


class TaskViews:
    def __init__(self, last_viewed_tasks):
        self.last_viewed_tasks = last_viewed_tasks

    def __str__(self):
        return f"TaskViews(Last Viewed Tasks: {self.last_viewed_tasks})"


class EventStats:
    def __init__(self, fishing_festival_sharks_killed, mining_fiesta_ores_mined):
        self.fishing_festival_sharks_killed = fishing_festival_sharks_killed
        self.mining_fiesta_ores_mined = mining_fiesta_ores_mined

    def __str__(self):
        return (f"EventStats(Fishing Festival Sharks Killed: {self.fishing_festival_sharks_killed}, "
                f"Mining Fiesta Ores Mined: {self.mining_fiesta_ores_mined})")


class SymbolData:
    def __init__(self, selected_symbol, bop_bonus, claimed_talisman, category_expanded):
        self.selected_symbol = selected_symbol
        self.bop_bonus = bop_bonus
        self.claimed_talisman = claimed_talisman
        self.category_expanded = category_expanded

    def __str__(self):
        return (f"SymbolData(Selected Symbol: {self.selected_symbol}, Bop Bonus: {self.bop_bonus}, "
                f"Claimed Talisman: {self.claimed_talisman}, Category Expanded: {self.category_expanded})")


class LevelingData:
    """
    Represents leveling data for a SkyBlock profile member, with individual components for each aspect.

    Attributes:
        experience_data (ExperienceData): The player's experience.
        completions_data (CompletionsData): Completion milestones.
        task_data (TaskData): Data for completed tasks.
        pet_score (PetScore): The highest pet score achieved.
        migration_data (MigrationData): Migration status details.
        task_views (TaskViews): Recently viewed tasks.
        event_stats (EventStats): Statistics for events like fishing festivals.
        symbol_data (SymbolData): Selected symbol, bonuses, and other status flags.
    """

    def __init__(self, data):
        self.experience_data = ExperienceData(data.get('experience', 0))
        self.completions_data = CompletionsData(data.get('completions', {}))
        self.task_data = TaskData(data.get('completed_tasks', []))
        self.pet_score = PetScore(data.get('highest_pet_score', 0))
        self.migration_data = MigrationData(data.get('migrated', False), data.get('migrated_completions_2', False))
        self.task_views = TaskViews(data.get('last_viewed_tasks', []))
        self.event_stats = EventStats(data.get('fishing_festival_sharks_killed', 0), data.get('mining_fiesta_ores_mined', 0))
        self.symbol_data = SymbolData(data.get('selected_symbol', ''), data.get('bop_bonus', ''),
                                      data.get('claimed_talisman', False), data.get('category_expanded', False))

    def __str__(self):
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
