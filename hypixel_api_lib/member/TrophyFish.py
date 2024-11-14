class TrophyFish:
    """
    Represents a single type of trophy fish with counts per tier.

    Attributes:
        name (str): The name of the fish.
        total_caught (int): Total number of this fish caught.
        tiers (dict[str,int]): Counts per tier (bronze, silver, gold, diamond).
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.total_caught: int = 0
        self.tiers: dict[str,int] = {}  # e.g., {'bronze': 10, 'silver': 5}

    def add_catch(self, tier: str | None, count: int) -> None:
        """
        Adds catch count to the fish.

        Args:
            tier (Optional[str]): The tier of the catch (e.g., 'bronze', 'silver').
            count (int): Number of fish caught.
        """
        if tier:
            self.tiers[tier] = self.tiers.get(tier, 0) + count
        else:
            self.total_caught += count

    def total_tier_catches(self) -> int:
        """
        Calculates the total catches across all tiers.

        Returns:
            int: Total catches across all tiers.
        """
        return sum(self.tiers.values())

    def __str__(self) -> str:
        return (
            f"TrophyFish(name={self.name}, total_caught={self.total_caught}, "
            f"tiers={self.tiers})"
        )

class TrophyFishStats:
    """
    Represents the player's trophy fish statistics.

    Attributes:
        rewards (list[int]): List of reward IDs.
        total_caught (int): Total number of trophy fish caught.
        fish_types (dict[str,TrophyFish]): Dictionary of trophy fish by name.
        last_caught (str): The last trophy fish caught with its tier.
    """

    def __init__(self, data: dict) -> None:
        self.rewards: list[int] = data.get('rewards', [])
        self.total_caught: int = data.get('total_caught', 0)
        self.last_caught: str = data.get('last_caught', '')
        self.fish_types: dict[str,TrophyFish] = {}

        self._parse_fish_data(data)

    def _parse_fish_data(self, data: dict) -> None:
        """
        Parses the fish data and populates the fish_types dictionary.

        Args:
            data (dict): The data dictionary.
        """
        special_keys = {'rewards', 'total_caught', 'last_caught'}
        for key, value in data.items():
            if key in special_keys:
                continue
            parts = key.split('_')
            if parts[-1] in {'bronze', 'silver', 'gold', 'diamond'}:
                tier = parts[-1]
                fish_name = '_'.join(parts[:-1])
            else:
                tier = None
                fish_name = key

            if fish_name not in self.fish_types:
                self.fish_types[fish_name] = TrophyFish(fish_name)

            self.fish_types[fish_name].add_catch(tier, value)

    def get_fish(self, fish_name: str) -> TrophyFish | None:
        """
        Retrieves a TrophyFish instance by name.

        Args:
            fish_name (str): The name of the fish.

        Returns:
            TrophyFish | None: The TrophyFish instance or None if not found.
        """
        return self.fish_types.get(fish_name)

    def __str__(self) -> str:
        fish_str = ', '.join(str(fish) for fish in self.fish_types.values())
        return (
            f"TrophyFishStats(rewards={self.rewards}, total_caught={self.total_caught}, "
            f"last_caught={self.last_caught}, fish_types=[{fish_str}])"
        )
