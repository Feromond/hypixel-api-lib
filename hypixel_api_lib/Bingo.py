from datetime import datetime, tzinfo
import re
import requests
from hypixel_api_lib.utils import convert_timestamp

BINGO_EVENT_API_URL = r"https://api.hypixel.net/resources/skyblock/bingo"

class BingoGoal:
    """
    Represents a single bingo goal.

    Attributes:
        id (str | optional): The unique identifier for the goal.
        name (str): The name of the goal.
        lore (str): A brief description of the goal.
        full_lore (list of str): A list containing detailed descriptions.
        tiers (list of int, optional): The tiers for goals that have multiple tiers.
        progress (int, optional): The current progress towards the goal.
        required_amount (int, optional): The amount required to complete the goal.
    """

    def __init__(self, goal_data: dict) -> None:
        self.id: str | None = goal_data.get('id')
        self.name: str = goal_data.get('name', 'Unknown Goal')
        self.lore: str = goal_data.get('lore', '')
        self.full_lore: list[str] = goal_data.get('fullLore', [])
        self.tiers: list[int] = goal_data.get('tiers', [])
        self.progress: int = goal_data.get('progress', 0)
        self.required_amount: int | None = goal_data.get('requiredAmount', None)
    
    def get_completion_percentage(self) -> float | None:
        """
        Calculate the completion percentage for goals with progress.
        (This might only be useful for global goals, not sure how to check when they are global)

        Returns:
            float or None: The completion percentage, or None if not applicable.
        """
        if self.required_amount:
            return min((self.progress / self.required_amount) * 100, 100)
        elif self.tiers:
            max_tier = max(self.tiers)
            return min((self.progress / max_tier) * 100, 100)
        return None

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Remove Minecraft formatting codes from the text.
        
        Args:
            text (str): The text to clean.
        
        Returns:
            str: The cleaned text without formatting codes.
        """
        return re.sub(r'§.', '', text)

    def get_clean_lore(self) -> str:
        """
        Get the lore with formatting codes removed.
        
        Returns:
            str: Cleaned lore text.
        """
        return self._clean_text(self.lore)

    def get_clean_full_lore(self) -> list[str]:
        """
        Get the full lore with formatting codes removed.
        
        Returns:
            list of str: List of cleaned full lore strings.
        """
        return [self._clean_text(line) for line in self.full_lore]

    def __str__(self) -> str:
        clean_lore = self.get_clean_lore()
        return f"{self.name} (ID: {self.id}): {clean_lore}"

class BingoEvent:
    """
    Represents the current bingo event.

    Attributes:
        id (int): The event ID.
        name (str): The event name.
        start (datetime): The start time of the event.
        end (datetime): The end time of the event.
        modifier (str): The event modifier.
        goals (list of BingoGoal): The list of goals for the event.
    """

    def __init__(self, event_data: dict) -> None:
        self.id: int | None = event_data.get('id')
        self.name: str = event_data.get('name')
        self.start: datetime | None = convert_timestamp(event_data.get('start'))
        self.end: datetime | None = convert_timestamp(event_data.get('end'))
        self.modifier: str | None = event_data.get('modifier')
        self.goals: list[BingoGoal] = [BingoGoal(goal) for goal in event_data.get('goals', [])]

    def get_start_time_in_timezone(self, tz: tzinfo) -> datetime | None:
        """
        Get the start time converted to the specified time zone.

        Args:
            tz (timezone): A timezone object.

        Returns:
            datetime: The start time in the specified time zone.
        """
        if self.start:
            return self.start.astimezone(tz)
        return None

    def get_end_time_in_timezone(self, tz: tzinfo) -> datetime | None:
        """
        Get the end time converted to the specified time zone.

        Args:
            tz (timezone): A timezone object.

        Returns:
            datetime: The end time in the specified time zone.
        """
        if self.end:
            return self.end.astimezone(tz)
        return None

    def get_goal_by_id(self, goal_id: str) -> BingoGoal | None:
        """
        Retrieve a goal by its ID.

        Args:
            goal_id (str): The ID of the goal.

        Returns:
            BingoGoal or None: The BingoGoal object, or None if not found.
        """
        return next((goal for goal in self.goals if goal.id == goal_id), None)
    
    def get_goal_by_name(self, goal_name: str) -> BingoGoal | None:
        """
        Retrieve a goal by its name.

        Args:
            goal_name (str): The name of the goal.

        Returns:
            BingoGoal or None: The BingoGoal object, or None if not found.
        """
        return next((goal for goal in self.goals if goal.name.lower() == goal_name.lower()), None)

    def __str__(self) -> str:
        start_str = self.start.strftime("%Y-%m-%d %H:%M:%S %Z") if self.start else "N/A"
        end_str = self.end.strftime("%Y-%m-%d %H:%M:%S %Z") if self.end else "N/A"
        return f"Bingo Event '{self.name}' (ID: {self.id}) from {start_str} to {end_str}"

class BingoEvents:
    """
    Manages fetching and storing the bingo event data from the API.

    Attributes:
        api_endpoint (str): The API endpoint URL.
        current_event (BingoEvent): The current bingo event.
    """

    def __init__(self, api_endpoint: str = BINGO_EVENT_API_URL) -> None:
        self.api_endpoint: str = api_endpoint
        self._current_event: BingoEvent | None = None
        self._load_current_event()

    def _load_current_event(self) -> None:
        """Fetch the current bingo event data from the API."""
        try:
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            data = response.json()

            if data.get('success') and data.get('goals'):
                self._current_event = BingoEvent(data)
            else:
                raise ValueError("No current bingo event data available in the response")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred: {e}")

    def get_current_event(self) -> BingoEvent | None:
        """
        Get the current bingo event.

        Returns:
            BingoEvent: The current bingo event.
        """
        return self._current_event
