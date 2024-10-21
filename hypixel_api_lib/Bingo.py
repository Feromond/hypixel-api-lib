from datetime import datetime, timezone
import re
import requests

BINGO_EVENT_API_URL = r"https://api.hypixel.net/resources/skyblock/bingo"

class BingoGoal:
    """
    Represents a single bingo goal.

    Attributes:
        id (str): The unique identifier for the goal.
        name (str): The name of the goal.
        lore (str): A brief description of the goal.
        full_lore (list of str): A list containing detailed descriptions.
        tiers (list of int, optional): The tiers for goals that have multiple tiers.
        progress (int, optional): The current progress towards the goal.
        required_amount (int, optional): The amount required to complete the goal.
    """

    def __init__(self, goal_data):
        self.id = goal_data.get('id')
        self.name = goal_data.get('name', 'Unknown Goal')
        self.lore = goal_data.get('lore', '')
        self.full_lore = goal_data.get('fullLore', [])
        self.tiers = goal_data.get('tiers', [])
        self.progress = goal_data.get('progress', 0)
        self.required_amount = goal_data.get('requiredAmount', None)
    
    def get_completion_percentage(self):
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
        else:
            return None

    def _clean_text(self, text):
        """
        Remove Minecraft formatting codes from the text.
        
        Args:
            text (str): The text to clean.
        
        Returns:
            str: The cleaned text without formatting codes.
        """
        return re.sub(r'§.', '', text)

    def get_clean_lore(self):
        """
        Get the lore with formatting codes removed.
        
        Returns:
            str: Cleaned lore text.
        """
        return self._clean_text(self.lore)

    def get_clean_full_lore(self):
        """
        Get the full lore with formatting codes removed.
        
        Returns:
            list of str: List of cleaned full lore strings.
        """
        return [self._clean_text(line) for line in self.full_lore]

    def __str__(self):
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

    def __init__(self, event_data):
        self.id = event_data.get('id')
        self.name = event_data.get('name')
        self.start = self._convert_timestamp(event_data.get('start'))
        self.end = self._convert_timestamp(event_data.get('end'))
        self.modifier = event_data.get('modifier')
        self.goals = [BingoGoal(goal) for goal in event_data.get('goals', [])]

    def _convert_timestamp(self, timestamp):
        """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None
    
    def get_start_time_in_timezone(self, tz):
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

    def get_end_time_in_timezone(self, tz):
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

    def get_goal_by_id(self, goal_id):
        """
        Retrieve a goal by its ID.

        Args:
            goal_id (str): The ID of the goal.

        Returns:
            BingoGoal or None: The BingoGoal object, or None if not found.
        """
        return next((goal for goal in self.goals if goal.id == goal_id), None)
    
    def get_goal_by_name(self, goal_name):
        """
        Retrieve a goal by its name.

        Args:
            goal_name (str): The name of the goal.

        Returns:
            BingoGoal or None: The BingoGoal object, or None if not found.
        """
        return next((goal for goal in self.goals if goal.name.lower() == goal_name.lower()), None)

    def __str__(self):
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

    def __init__(self, api_endpoint=BINGO_EVENT_API_URL):
        self.api_endpoint = api_endpoint
        self._current_event = None
        self._load_current_event()

    def _load_current_event(self):
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

    def get_current_event(self):
        """
        Get the current bingo event.

        Returns:
            BingoEvent: The current bingo event.
        """
        return self._current_event
