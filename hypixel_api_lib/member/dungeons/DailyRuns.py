class DailyRuns:
    """
    DailyRuns data class to handle the dungeon daily runs component

    Attributes:
        current_day_stamp (int): the current day timestamp for the data (0 if none)
        completed_runs_count (int): number of runs completed for the current day
    """
    def __init__(self, data: dict[str,int]) -> None:
        self.current_day_stamp: int = data.get("current_day_stamp", 0)
        self.completed_runs_count: int = data.get("completed_runs_count", 0)
    def __str__(self) -> str:
        return f"Current Day Stamp: {self.current_day_stamp}, Completed Runs Count: {self.completed_runs_count}"