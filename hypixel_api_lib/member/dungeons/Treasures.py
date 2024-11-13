import datetime
import re
from hypixel_api_lib.utils import convert_timestamp

def remove_color_codes(text: str) -> str:
    """
    Removes Minecraft color codes from a string.

    Args:
        text (str): The text containing Minecraft color codes.

    Returns:
        str: The text with color codes removed.
    """
    return re.sub(r'§.', '', text)

class RewardItem:
    """
    Represents a single reward item from a chest.

    Attributes:
        raw (str): The original reward string.
        type (str): The type of reward (e.g., 'rejuvenate', 'ESSENCE:UNDEAD').
        tier (int or None): The tier or amount associated with the reward.
    """
    def __init__(self, data: str) -> None:
        self.raw: str = data
        self.type: str = ''
        self.tier: int | None = None
        self.parse_reward(data)

    def parse_reward(self, data: str) -> None:
        """
        Parses the reward string to extract the type and tier.

        Args:
            data (str): The reward string to parse.
        """
        if ':' in data:
            # Handle essence or special items like 'ESSENCE:UNDEAD:28'
            parts = data.split(':')
            if len(parts) == 3:
                self.type = f"{parts[0]}:{parts[1]}"
                try:
                    self.tier = int(parts[2])
                except ValueError:
                    self.tier = None
        elif '_' in data:
            # Handle items with tiers like 'rejuvenate_1'
            parts = data.rsplit('_', 1)
            if len(parts) == 2:
                self.type = parts[0]
                try:
                    self.tier = int(parts[1])
                except ValueError:
                    self.tier = None
            else:
                self.type = data
        else:
            self.type = data

    def __repr__(self) -> str:
        return f"<RewardItem type={self.type}, tier={self.tier}>"

class Rewards:
    """
    Represents the rewards from a chest.

    Attributes:
        rewards (list of RewardItem): List of reward items.
        rolled_rng_meter_randomly (bool): Indicates if the RNG meter was rolled randomly.
    """
    def __init__(self, data: dict) -> None:
        rewards_list: list = data.get('rewards', [])
        self.rewards: list[RewardItem] = [RewardItem(item) for item in rewards_list]
        self.rolled_rng_meter_randomly: bool = data.get('rolled_rng_meter_randomly', False)

    def __iter__(self): 
        return iter(self.rewards)

    def __len__(self) -> int:
        return len(self.rewards)

    def __getitem__(self, index) -> RewardItem:
        return self.rewards[index]

class Chest:
    """
    Represents a single chest in a dungeon run.

    Attributes:
        run_id (str): The unique identifier of the run this chest belongs to.
        chest_id (str): The unique identifier of the chest.
        treasure_type (str): The type of chest (e.g., 'wood', 'gold').
        quality (int): The quality score of the chest.
        shiny_eligible (bool): Indicates if the chest is eligible for shiny rewards.
        paid (bool): Indicates if the chest was paid for.
        rerolls (int): The number of rerolls performed on the chest.
        rewards (Rewards): The rewards contained in the chest.
    """
    def __init__(self, data: dict) -> None:
        self.run_id: str = data.get('run_id', '')
        self.chest_id: str = data.get('chest_id', '')
        self.treasure_type: str = data.get('treasure_type', '')
        self.quality: int = data.get('quality', 0)
        self.shiny_eligible: bool = data.get('shiny_eligible', False)
        self.paid: bool = data.get('paid', False)
        self.rerolls: int = data.get('rerolls', 0)
        self.rewards: Rewards = Rewards(data.get('rewards', {}))

    def __repr__(self) -> str:
        return f"<Chest treasure_type={self.treasure_type}, quality={self.quality}>"

class Chests:
    """
    Represents a collection of chests.

    Attributes:
        chests (list of Chest): List of chests from dungeon runs.
    """
    def __init__(self, data: list[dict]) -> None:
        self.chests: list[Chest] = [Chest(chest_data) for chest_data in data]

    def __iter__(self):
        return iter(self.chests)

    def __len__(self) -> int:
        return len(self.chests)

    def __getitem__(self, index) -> Chest:
        return self.chests[index]

class Participant:
    """
    Represents a participant in a dungeon run.

    Attributes:
        player_uuid (str): The UUID of the player.
        display_name (str): The display name of the player with Minecraft color codes.
        class_milestone (int): The class milestone achieved by the player.
    """
    def __init__(self, data: dict) -> None:
        self.player_uuid: str = data.get('player_uuid', '')
        self.display_name: str = data.get('display_name', '')
        self.class_milestone: int = data.get('class_milestone', 0)

    @property
    def name(self) -> str:
        """
        str: The participant's name without color codes and extra text.
        """
        cleaned_name = remove_color_codes(self.display_name)
        parts = cleaned_name.split(': ')
        if len(parts) >= 1:
            return parts[0]
        return cleaned_name

    @property
    def player_class(self) -> str:
        """
        str: The participant's class (e.g., 'Mage', 'Healer').
        """
        cleaned_name = remove_color_codes(self.display_name)
        parts = cleaned_name.split(': ')
        if len(parts) >= 2:
            class_and_level = parts[1]
            class_parts = class_and_level.split(' (')
            if len(class_parts) >= 1:
                return class_parts[0]
        return ''

    @property
    def level(self) -> int:
        """
        int: The participant's class level.
        """
        cleaned_name = remove_color_codes(self.display_name)
        match = re.search(r'\((\d+)\)', cleaned_name)
        if match:
            return int(match.group(1))
        return 0
    
    def __repr__(self) -> str:
        return f"Participants Name: {self.name}, Class: {self.player_class}, Level: {self.level}"

class Run:
    """
    Represents a single dungeon run.

    Attributes:
        run_id (str): The unique identifier of the run.
        completion_ts (int): The completion timestamp in milliseconds since epoch.
        dungeon_type (str): The type of dungeon (e.g., 'master_catacombs').
        dungeon_tier (int): The tier or floor level of the dungeon.
        participants (list of Participant): List of participants in the run.
    """
    def __init__(self, data: dict) -> None:
        self.run_id: str = data.get('run_id', '')
        self.completion_ts: int = data.get('completion_ts', 0)
        self.dungeon_type: str = data.get('dungeon_type', '')
        self.dungeon_tier: int = data.get('dungeon_tier', 0)
        participants_data = data.get('participants', [])
        self.participants: list[Participant] = [Participant(p) for p in participants_data]

    @property
    def completion_time(self) -> datetime.datetime:
        """
        Returns the completion time as a datetime object.
        """
        return convert_timestamp(self.completion_ts)

class Runs:
    """
    Represents a collection of dungeon runs.

    Attributes:
        runs (list of Run): List of dungeon runs.
    """
    def __init__(self, data: list[dict]) -> None:
        self.runs: list[Run] = [Run(run_data) for run_data in data]

    def __iter__(self):
        return iter(self.runs)

    def __len__(self) -> int:
        return len(self.runs)

    def __getitem__(self, index) -> Run:
        return self.runs[index]

class Treasures:
    """
    Represents the treasures component, including runs and chests.

    Attributes:
        runs (Runs): Collection of dungeon runs.
        chests (Chests): Collection of chests from runs.
    """
    def __init__(self, data: dict[str,list[dict]]) -> None:
        self.runs: Runs = Runs(data.get("runs", []))
        self.chests: Chests = Chests(data.get("chests", []))