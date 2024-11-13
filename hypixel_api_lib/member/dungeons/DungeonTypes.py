from datetime import datetime
class DungeonRun:
    """
    The DungeonRun class stores data related to a dungeon run.

    Attributes:
        timestamp (datetime): The timestamp of the run in datetime format.
        score_exploration (int): Exploration score achieved in the run.
        score_speed (int): Speed score achieved in the run.
        score_skill (int): Skill score achieved in the run.
        score_bonus (int): Bonus score achieved in the run.
        dungeon_class (str): Class type of the dungeon (e.g., 'berserk').
        teammates (list[str]): List of teammate IDs.
        elapsed_time (int): Time taken for the run in milliseconds.
        damage_dealt (float): Total damage dealt by the player.
        deaths (int): Number of deaths in the run.
        mobs_killed (int): Number of mobs killed.
        secrets_found (int): Number of secrets found.
        damage_mitigated (float): Total damage mitigated.
        ally_healing (float): Total healing done to allies.
    """

    def __init__(self, data: dict) -> None:
        self.timestamp: datetime = datetime.fromtimestamp(data.get("timestamp", 0) / 1000)
        self.score_exploration: int = data.get("score_exploration", 0)
        self.score_speed: int = data.get("score_speed", 0)
        self.score_skill: int = data.get("score_skill", 0)
        self.score_bonus: int = data.get("score_bonus", 0)
        self.dungeon_class: str = data.get("dungeon_class", "unknown")
        self.teammates: list[str] = data.get("teammates", [])   # TODO: Add conversion from UUID to usernames
        self.elapsed_time: int = data.get("elapsed_time", 0)
        self.damage_dealt: float = data.get("damage_dealt", 0.0)
        self.deaths: int = data.get("deaths", 0)
        self.mobs_killed: int = data.get("mobs_killed", 0)
        self.secrets_found: int = data.get("secrets_found", 0)
        self.damage_mitigated: float = data.get("damage_mitigated", 0.0)
        self.ally_healing: float = data.get("ally_healing", 0.0)

    def __str__(self) -> str:
        return (f"Dungeon Run on {self.timestamp}: "
                f"Class: {self.dungeon_class}, "
                f"Scores - Exploration: {self.score_exploration}, Speed: {self.score_speed}, "
                f"Skill: {self.score_skill}, Bonus: {self.score_bonus}, "
                f"Teammates: {', '.join(self.teammates)}, "
                f"Elapsed Time: {self.elapsed_time}ms, "
                f"Damage Dealt: {self.damage_dealt}, Deaths: {self.deaths}, "
                f"Mobs Killed: {self.mobs_killed}, Secrets Found: {self.secrets_found}, "
                f"Damage Mitigated: {self.damage_mitigated}, Ally Healing: {self.ally_healing}")

class DungeonRuns:
    def __init__(self, list_of_runs: list[dict]) -> None:
        self.dungeon_runs = []
        for run in list_of_runs:
            self.dungeon_runs.append(DungeonRun(run))
            

class BestRuns:
    def __init__(self, data: dict[str,dict]) -> None:
        self.floor0: list[dict] = data.get("0", [])
        self.floor1: list[dict] = data.get("1", [])
        self.floor2: list[dict] = data.get("2", [])
        self.floor3: list[dict] = data.get("3", [])
        self.floor4: list[dict] = data.get("4", [])
        self.floor5: list[dict] = data.get("5", [])
        self.floor6: list[dict] = data.get("6", [])
        self.floor7: list[dict] = data.get("7", [])
    

class FloorStats:
    def __init__(self, data: dict[str,float]) -> None:
        self.floor0: float = data.get("0", 0.0)
        self.floor1: float = data.get("1", 0.0)
        self.floor2: float = data.get("2", 0.0)
        self.floor3: float = data.get("3", 0.0)
        self.floor4: float = data.get("4", 0.0)
        self.floor5: float = data.get("5", 0.0)
        self.floor6: float = data.get("6", 0.0)
        self.floor7: float = data.get("7", 0.0)

class BestStats(FloorStats):
    def __init__(self, data: dict[str,float]) -> None:
        super().__init__(data)
        self.best: float = data.get("best")
    
class TotalStats(FloorStats):
    def __init__(self, data: dict[str,float]) -> None:
        super().__init__(data)
        self.total: float = data.get("total")

class MostDamageMage(BestStats):
    def __str__(self) -> str:
        return f"Most Mage Damage for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, best: {self.best}"

class FastestTimeS(FloorStats):
    def __str__(self) -> str:
        return f"Fastest S Times for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}"

class WatcherKills(TotalStats):
    def __str__(self) -> str:
        return f"Watchers Killed In Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, Total: {self.total}"

class FastestTime(BestStats):
    def __str__(self) -> str:
        return f"Fastest Times for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, best: {self.best}"

class TierCompletions(TotalStats):
    def __str__(self) -> str:
        return f"Tier Completions for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, Total: {self.total}"

class MostHealing(BestStats):
    def __str__(self) -> str:
        return f"Most Healing for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, best: {self.best}"

class MostDamageBerserk(FloorStats):
    def __str__(self) -> str:
        return f"Most Berserk Damage for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}"

class MostMobsKilled(BestStats):
    def __str__(self) -> str:
        return f"Most Mobs Killed for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, best: {self.best}"

class MobsKilled(TotalStats):
    def __str__(self) -> str:
        return f"Mobs Killed In Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, Total: {self.total}"

class BestScore(BestStats):
    def __str__(self) -> str:
        return f"Best Score for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, best: {self.best}"


class TimesPlayedCatacombs(TotalStats):
    def __str__(self) -> str:
        return f"Times Played for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, Total: {self.total}"


class Catacombs: #TODO test all these to verify
    def __init__(self, data:dict) -> None:
        self.times_played: TimesPlayedCatacombs = TimesPlayedCatacombs(data.get("times_played", {}))
        self.experience: float = data.get("experience", 0.0)
        self.best_score: BestScore = BestScore(data.get("best_score", {}))
        self.mobs_killed: MobsKilled = MobsKilled(data.get("mobs_killed", {}))
        self.most_mobs_killed: MostMobsKilled = MostMobsKilled(data.get("most_mobs_killed", {}))
        self.most_damage_berserk: MostDamageBerserk = MostDamageBerserk(data.get("most_damage_berserk", {}))
        self.most_healing: MostHealing = MostHealing(data.get("most_healing", {}))
        self.tier_completions: TierCompletions = TierCompletions(data.get("tier_completions", {}))
        self.fastest_time: FastestTime = FastestTime(data.get("fastest_time", {}))
        self.best_runs: BestRuns = BestRuns(data.get("best_runs", {}))
        self.watcher_kills: WatcherKills = WatcherKills(data.get("watcher_kills", {}))
        self.highest_tier_completed: int | None = data.get("highest_tier_completed", None)
        self.fastest_time_s: FastestTimeS = FastestTimeS(data.get("fastest_time_s", {}))
        self.most_damage_mage: MostDamageMage = MostDamageMage(data.get("most_damage_mage", {}))

"""
Catacombs
 'most_damage_tank', 'fastest_time_s_plus', 'most_damage_archer', 'most_damage_healer', 'milestone_completions'])

Master Catacombs
dict_keys(['tier_completions', 'milestone_completions', 'best_score', 'mobs_killed', 'most_mobs_killed', 'most_damage_berserk', 'most_healing', 'fastest_time', 'highest_tier_completed', 'fastest_time_s', 'best_runs', 'most_damage_mage', 'most_damage_archer', 'fastest_time_s_plus', 'most_damage_healer'])
"""



class DungeonTypes:
    def __init__(self, data: dict) -> None:
        self.catacombs: dict = data.get("catacombs", {})
        self.master_catacombs: dict = data.get("master_catacombs")

