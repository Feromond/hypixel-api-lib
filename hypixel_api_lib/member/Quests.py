class HarpQuest:
    """
    Represents the player's Harp Quest data.

    Attributes:
        selected_song (str): The currently selected song.
        selected_song_epoch (int): The epoch time when the song was selected.
        songs (Dict[str, Dict[str, float or int]]): A dictionary containing song statistics.
        claimed_talisman (bool): Whether the talisman has been claimed.
    """

    def __init__(self, data: dict) -> None:
        harp_data = data.get('harp_quest', {})
        self.selected_song: str | None = harp_data.get('selected_song')
        self.selected_song_epoch: int | None = harp_data.get('selected_song_epoch')
        self.claimed_talisman: bool = harp_data.get('claimed_talisman', False)
        self.songs: dict[str,dict[str,float|int]] = self._extract_song_stats(harp_data)

    def _extract_song_stats(self, harp_data: dict) -> dict[str,dict[str,float|int]]:
        """
        Extracts song statistics from the harp quest data.

        Args:
            harp_data (dict): The harp quest data.

        Returns:
            Dict[str, Dict[str, float or int]]: A dictionary of song statistics.
        """
        songs = {}
        for key, value in harp_data.items():
            if key.startswith('song_') and not key.endswith('_completions') and not key.endswith('_perfect_completions') and not key.endswith('_best_completion'):
                continue
            if key.startswith('song_'):
                parts = key.split('_')
                song_name = '_'.join(parts[1:-1])
                stat_type = parts[-1]
                if song_name not in songs:
                    songs[song_name] = {}
                songs[song_name][stat_type] = value
        return songs

    def get_song_stats(self, song_name: str) -> dict[str,float|int]:
        """
        Get statistics for a specific song.

        Args:
            song_name (str): The name of the song.

        Returns:
            Dict[str, float or int]: A dictionary of statistics for the song.
        """
        return self.songs.get(song_name, {})

    def get_best_completion(self, song_name: str) -> float | None:
        """
        Get the best completion percentage for a song.

        Args:
            song_name (str): The name of the song.

        Returns:
            Optional[float]: The best completion percentage, or None if not found.
        """
        return self.songs.get(song_name, {}).get('best_completion')

    def get_total_completions(self, song_name: str) -> int:
        """
        Get the total number of completions for a song.

        Args:
            song_name (str): The name of the song.

        Returns:
            int: The number of completions.
        """
        return self.songs.get(song_name, {}).get('completions', 0)

    def get_perfect_completions(self, song_name: str) -> int:
        """
        Get the number of perfect completions for a song.

        Args:
            song_name (str): The name of the song.

        Returns:
            int: The number of perfect completions.
        """
        return self.songs.get(song_name, {}).get('perfect_completions', 0)

    def __str__(self) -> str:
        return (
            f"HarpQuest(selected_song={self.selected_song}, claimed_talisman={self.claimed_talisman}, "
            f"songs_completed={len(self.songs)})"
        )

class TrapperQuest:
    """
    Represents the player's Trapper Quest data.

    Attributes:
        last_task_time (int): The epoch time of the last task.
        pelt_count (int): The number of pelts collected.
    """

    def __init__(self, data: dict) -> None:
        trapper_data = data.get('trapper_quest', {})
        self.last_task_time: int | None = trapper_data.get('last_task_time')
        self.pelt_count: int = trapper_data.get('pelt_count', 0)

    def time_since_last_task(self, current_time_epoch: int) -> int | None:
        """
        Calculate the time elapsed since the last task.

        Args:
            current_time_epoch (int): The current epoch time.

        Returns:
            Optional[int]: Time in milliseconds since the last task, or None if last_task_time is not set.
        """
        if self.last_task_time is not None:
            return current_time_epoch - self.last_task_time
        return None

    def __str__(self) -> str:
        return (
            f"TrapperQuest(pelt_count={self.pelt_count}, last_task_time={self.last_task_time})"
        )

class Quests:
    """
    Represents the player's Quests data, including Harp Quest and Trapper Quest.

    Attributes:
        harp_quest (HarpQuest): The Harp Quest data.
        trapper_quest (TrapperQuest): The Trapper Quest data.
    """

    def __init__(self, data: dict) -> None:
        self.harp_quest = HarpQuest(data)
        self.trapper_quest = TrapperQuest(data)

    def __str__(self) -> str:
        return f"Quests(harp_quest={self.harp_quest}, trapper_quest={self.trapper_quest})"
