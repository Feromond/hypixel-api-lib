class Bestiary:
    """
    Represents the player's Bestiary data.

    Attributes:
        migrated_stats (bool): Whether the stats have been migrated.
        migration (bool): Migration status.
        kills (dict[str, int]): Dictionary of mobs and their kill counts.
        deaths (dict[str, int]): Dictionary of mobs and their death counts.
        milestone (int): Last claimed milestone.
        miscellaneous (bool): Whether max kills are visible.
    """

    def __init__(self, data: dict) -> None:
        self.migrated_stats: bool = data.get("migrated_stats", False)
        self.migration: bool = data.get("migration", False)
        self.kills: dict[str, int] = data.get("kills", {}).copy()
        self.last_killed_mob: str | None = self.kills.pop('last_killed_mob', None) 
        self.deaths: dict[str,int] = data.get("deaths", {})
        self.milestone: int = data.get("milestone", {}).get("last_claimed_milestone", 0)
        self.miscellaneous: bool = data.get("miscellaneous", {}).get("max_kills_visible", False)

    def get_kill_count(self, mob_name: str) -> int:
        """
        Get the kill count for a specific mob.

        Args:
            mob_name (str): The name of the mob.

        Returns:
            int: The kill count for the mob, or 0 if not found.
        """
        return self.kills.get(mob_name, 0)

    def get_death_count(self, mob_name: str) -> int:
        """
        Get the death count for a specific mob.

        Args:
            mob_name (str): The name of the mob.

        Returns:
            int: The death count for the mob, or 0 if not found.
        """
        return self.deaths.get(mob_name, 0)

    def top_kills(self, n: int = 5) -> list[tuple[str, int]]:
        """
        Get the top N mobs by kill count.

        Args:
            n (int): The number of top mobs to return.

        Returns:
            list[tuple[str, int]]: A list of tuples containing mob names and kill counts.
        """
        sorted_kills = sorted(self.kills.items(), key=lambda item: item[1], reverse=True)
        return sorted_kills[:n]

    def top_deaths(self, n: int = 5) -> list[tuple[str, int]]:
        """
        Get the top N mobs by death count.

        Args:
            n (int): The number of top mobs to return.

        Returns:
            list[tuple[str, int]]: A list of tuples containing mob names and death counts.
        """
        sorted_deaths = sorted(self.deaths.items(), key=lambda item: item[1], reverse=True)
        return sorted_deaths[:n]

    def total_kills(self) -> int:
        """
        Get the total number of kills across all mobs.

        Returns:
            int: Total kills.
        """
        return sum(self.kills.values())

    def total_deaths(self) -> int:
        """
        Get the total number of deaths across all mobs.

        Returns:
            int: Total deaths.
        """
        return sum(self.deaths.values())

    def search_mobs(self, query: str) -> list[str]:
        """
        Search for mobs containing the query string in their names.

        Args:
            query (str): The search query string.

        Returns:
            list[str]: A list of mob names that match the query.
        """
        query_lower = query.lower()
        matched_mobs = [mob for mob in self.kills.keys() if query_lower in mob.lower()]
        return matched_mobs

    def __str__(self) -> str:
        return (
            f"Bestiary(milestone={self.milestone}, total_kills={self.total_kills()}, "
            f"total_deaths={self.total_deaths()})"
        )