class FloorStats():
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

class FastestTime(BestStats):
    def __str__(self) -> None:
        return f"Fastest Times for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, best: {self.best}"

class TierCompletions(TotalStats):
    def __str__(self) -> None:
        return f"Tier Completions for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, Total: {self.total}"

class MostHealing(BestStats):
    def __str__(self) -> None:
        return f"Most Healing for Entrance: {self.floor0}, Floor 1: {self.floor1}, Floor 2: {self.floor2}, Floor 3: {self.floor3}, Floor 4: {self.floor4}, Floor 5: {self.floor5}, Floor 6: {self.floor6}, Floor 7: {self.floor7}, best: {self.best}"

class MostDamageBerserk(FloorStats):
    def __str__(self) -> None:
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


class Catacombs():
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


"""
Catacombs
 'best_runs', 'watcher_kills', 'highest_tier_completed', 'fastest_time_s', 'most_damage_mage', 'most_damage_tank', 'fastest_time_s_plus', 'most_damage_archer', 'most_damage_healer', 'milestone_completions'])

Master Catacombs
dict_keys(['tier_completions', 'milestone_completions', 'best_score', 'mobs_killed', 'most_mobs_killed', 'most_damage_berserk', 'most_healing', 'fastest_time', 'highest_tier_completed', 'fastest_time_s', 'best_runs', 'most_damage_mage', 'most_damage_archer', 'fastest_time_s_plus', 'most_damage_healer'])
"""



class DungeonTypes():
    def __init__(self, data: dict) -> None:
        self.catacombs: dict = data.get("catacombs", {})
        self.master_catacombs: dict = data.get("master_catacombs")

