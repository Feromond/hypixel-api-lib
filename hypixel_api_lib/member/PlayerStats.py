class SpookyStats:
    """
    Represents the player's statistics related to the Spooky event.

    Attributes:
        bats_spawned (Dict[str, float]): Dictionary of bats spawned, where keys are identifiers
            (representing the skyblockyear), and values are counts.
    """

    def __init__(self, data: dict) -> None:
        self.bats_spawned: dict[str,float] = data.get('bats_spawned', {})

    def total_bats_spawned(self) -> float:
        """
        Calculates the total number of bats spawned, excluding the 'total' key if present.

        Returns:
            float: Total number of bats spawned.
        """
        return sum(
            value for key, value in self.bats_spawned.items()
            if key != 'total' and isinstance(value, (int, float))
        )

    def __str__(self) -> str:
        return f"SpookyStats(bats_spawned={self.bats_spawned})"

class RiftStats:
    """
    Represents the player's statistics within the Rift dimension.

    Attributes:
        visits (float): Total number of times the player has visited the Rift.
        pass_consumed (float): Number of Rift passes consumed.
        lifetime_motes_earned (float): Total motes earned over the player's lifetime.
        motes_orb_pickup (float): Number of motes orbs picked up.
        woods_larva_killed (float): Number of larva killed in the woods area.
        woods_odonata_bottled (float): Number of odonata bottled in the woods area.
        lagoon_mushroom_popped_out (float): Number of times mushrooms popped out in the lagoon.
        lagoon_leech_supreme_killed (float): Number of Leech Supremes killed in the lagoon.
        lagoon_rocks_game_complete (float): Number of times the rocks game was completed in the lagoon.
        west_cake_part_eaten (float): Number of cake parts eaten in the western area.
        west_hot_dogs_given (float): Number of hot dogs given in the western area.
        west_vermin_vacuumed (Dict[str, float]): Vermin vacuumed in the western area, categorized by type.
        dreadfarm_caducous_harvested (float): Number of caducous harvested in the Dreadfarm.
        dreadfarm_wilted_harvested (float): Number of wilted crops harvested in the Dreadfarm.
        dreadfarm_agaricus_harvested (float): Number of agaricus harvested in the Dreadfarm.
        dreadfarm_chicken_killed (float): Number of chickens killed in the Dreadfarm.
        popped_balloons (float): Number of balloons popped.
        dreadfarm_riftwarts_harvested (float): Number of riftwarts harvested in the Dreadfarm.
        dreadfarm_bean_bulb_collected (float): Number of bean bulbs collected in the Dreadfarm.
        plaza_red_light_deaths (float): Number of deaths by red light in the plaza.
        plaza_horsezooka_shot (float): Number of horsezooka shots fired in the plaza.
        living_metal_spawnegg_used (float): Number of living metal spawn eggs used.
        living_metal_piece_maxed (float): Number of living metal pieces that have been maxed out.
        living_cave_snake_collected (float): Number of living cave snakes collected.
        colosseum_globowls_at_tentacle (float): Number of globowls thrown at a tentacle in the colosseum.
        colosseum_blaster_shots (float): Number of blaster shots fired in the colosseum.
        colosseum_bacte_defeated (float): Number of bacte defeated in the colosseum.
        plaza_pillar_deaths (float): Number of deaths by the plaza pillar.
        castle_sent_to_prison (float): Number of times sent to prison in the castle.
        castle_effigy_broken (float): Number of effigies broken in the castle.
    """

    def __init__(self, data: dict) -> None:
        self.visits: float = data.get('visits', 0.0)
        self.pass_consumed: float = data.get('pass_consumed', 0.0)
        self.lifetime_motes_earned: float = data.get('lifetime_motes_earned', 0.0)
        self.motes_orb_pickup: float = data.get('motes_orb_pickup', 0.0)
        self.woods_larva_killed: float = data.get('woods_larva_killed', 0.0)
        self.woods_odonata_bottled: float = data.get('woods_odonata_bottled', 0.0)
        self.lagoon_mushroom_popped_out: float = data.get('lagoon_mushroom_popped_out', 0.0)
        self.lagoon_leech_supreme_killed: float = data.get('lagoon_leech_supreme_killed', 0.0)
        self.lagoon_rocks_game_complete: float = data.get('lagoon_rocks_game_complete', 0.0)
        self.west_cake_part_eaten: float = data.get('west_cake_part_eaten', 0.0)
        self.west_hot_dogs_given: float = data.get('west_hot_dogs_given', 0.0)
        self.west_vermin_vacuumed: dict[str, float] = data.get('west_vermin_vacuumed', {})
        self.dreadfarm_caducous_harvested: float = data.get('dreadfarm_caducous_harvested', 0.0)
        self.dreadfarm_wilted_harvested: float = data.get('dreadfarm_wilted_harvested', 0.0)
        self.dreadfarm_agaricus_harvested: float = data.get('dreadfarm_agaricus_harvested', 0.0)
        self.dreadfarm_chicken_killed: float = data.get('dreadfarm_chicken_killed', 0.0)
        self.popped_balloons: float = data.get('popped_balloons', 0.0)
        self.dreadfarm_riftwarts_harvested: float = data.get('dreadfarm_riftwarts_harvested', 0.0)
        self.dreadfarm_bean_bulb_collected: float = data.get('dreadfarm_bean_bulb_collected', 0.0)
        self.plaza_red_light_deaths: float = data.get('plaza_red_light_deaths', 0.0)
        self.plaza_horsezooka_shot: float = data.get('plaza_horsezooka_shot', 0.0)
        self.living_metal_spawnegg_used: float = data.get('living_metal_spawnegg_used', 0.0)
        self.living_metal_piece_maxed: float = data.get('living_metal_piece_maxed', 0.0)
        self.living_cave_snake_collected: float = data.get('living_cave_snake_collected', 0.0)
        self.colosseum_globowls_at_tentacle: float = data.get('colosseum_globowls_at_tentacle', 0.0)
        self.colosseum_blaster_shots: float = data.get('colosseum_blaster_shots', 0.0)
        self.colosseum_bacte_defeated: float = data.get('colosseum_bacte_defeated', 0.0)
        self.plaza_pillar_deaths: float = data.get('plaza_pillar_deaths', 0.0)
        self.castle_sent_to_prison: float = data.get('castle_sent_to_prison', 0.0)
        self.castle_effigy_broken: float = data.get('castle_effigy_broken', 0.0)

    def total_vermin_vacuumed(self) -> float:
        """
        Calculates the total number of vermin vacuumed in the western area.

        Returns:
            float: Total vermin vacuumed.
        """
        return self.west_vermin_vacuumed.get('total', 0.0)

    def __str__(self) -> str:
        return (
            f"RiftStats("
            f"visits={self.visits}, pass_consumed={self.pass_consumed}, "
            f"lifetime_motes_earned={self.lifetime_motes_earned}, motes_orb_pickup={self.motes_orb_pickup}, "
            f"woods_larva_killed={self.woods_larva_killed}, woods_odonata_bottled={self.woods_odonata_bottled}, "
            f"lagoon_mushroom_popped_out={self.lagoon_mushroom_popped_out}, "
            f"lagoon_leech_supreme_killed={self.lagoon_leech_supreme_killed}, "
            f"lagoon_rocks_game_complete={self.lagoon_rocks_game_complete}, "
            f"west_cake_part_eaten={self.west_cake_part_eaten}, "
            f"west_hot_dogs_given={self.west_hot_dogs_given}, "
            f"west_vermin_vacuumed={self.west_vermin_vacuumed}, "
            f"dreadfarm_caducous_harvested={self.dreadfarm_caducous_harvested}, "
            f"dreadfarm_wilted_harvested={self.dreadfarm_wilted_harvested}, "
            f"dreadfarm_agaricus_harvested={self.dreadfarm_agaricus_harvested}, "
            f"dreadfarm_chicken_killed={self.dreadfarm_chicken_killed}, "
            f"popped_balloons={self.popped_balloons}, "
            f"dreadfarm_riftwarts_harvested={self.dreadfarm_riftwarts_harvested}, "
            f"dreadfarm_bean_bulb_collected={self.dreadfarm_bean_bulb_collected}, "
            f"plaza_red_light_deaths={self.plaza_red_light_deaths}, "
            f"plaza_horsezooka_shot={self.plaza_horsezooka_shot}, "
            f"living_metal_spawnegg_used={self.living_metal_spawnegg_used}, "
            f"living_metal_piece_maxed={self.living_metal_piece_maxed}, "
            f"living_cave_snake_collected={self.living_cave_snake_collected}, "
            f"colosseum_globowls_at_tentacle={self.colosseum_globowls_at_tentacle}, "
            f"colosseum_blaster_shots={self.colosseum_blaster_shots}, "
            f"colosseum_bacte_defeated={self.colosseum_bacte_defeated}, "
            f"plaza_pillar_deaths={self.plaza_pillar_deaths}, "
            f"castle_sent_to_prison={self.castle_sent_to_prison}, "
            f"castle_effigy_broken={self.castle_effigy_broken}"
            f")"
        )


class MythosStats:
    """
    Represents the player's Mythological event statistics.

    Attributes:
        kills (float): Total number of mythological creatures killed.
        burrows_dug_next (dict[str, float]): Number of 'next' burrows dug, categorized by rarity.
        burrows_dug_combat (dict[str, float]): Number of combat burrows dug, categorized by rarity.
        burrows_dug_treasure (dict[str, float]): Number of treasure burrows dug, categorized by rarity.
        burrows_chains_complete (dict[str, float]): Number of burrow chains completed, categorized by rarity.
    """

    def __init__(self, data: dict) -> None:
        self.kills: float = data.get('kills', 0.0)
        self.burrows_dug_next: dict[str,float] = data.get('burrows_dug_next', {})
        self.burrows_dug_combat: dict[str,float] = data.get('burrows_dug_combat', {})
        self.burrows_dug_treasure: dict[str,float] = data.get('burrows_dug_treasure', {})
        self.burrows_chains_complete: dict[str,float] = data.get('burrows_chains_complete', {})

    def total_burrows_dug(self) -> float:
        """
        Calculates the total number of burrows dug across all categories.

        Returns:
            float: Total number of burrows dug.
        """
        total_next = self.burrows_dug_next.get('total', 0.0)
        total_combat = self.burrows_dug_combat.get('total', 0.0)
        total_treasure = self.burrows_dug_treasure.get('total', 0.0)
        return total_next + total_combat + total_treasure

    def __str__(self) -> str:
        return (
            f"MythosStats(kills={self.kills}, burrows_dug_next={self.burrows_dug_next}, "
            f"burrows_dug_combat={self.burrows_dug_combat}, burrows_dug_treasure={self.burrows_dug_treasure}, "
            f"burrows_chains_complete={self.burrows_chains_complete})"
        )

class ItemsFishedStats:
    """
    Represents the player's fishing statistics.

    Attributes:
        total (float): Total number of items fished.
        treasure (float): Number of treasure items fished.
        normal (float): Number of normal items fished.
        large_treasure (float): Number of large treasure items fished.
        trophy_fish (float): Number of trophy fish caught.
    """

    def __init__(self, data: dict) -> None:
        self.total: float = data.get('total', 0.0)
        self.treasure: float = data.get('treasure', 0.0)
        self.normal: float = data.get('normal', 0.0)
        self.large_treasure: float = data.get('large_treasure', 0.0)
        self.trophy_fish: float = data.get('trophy_fish', 0.0)

    def __str__(self) -> str:
        return (
            f"ItemsFishedStats(total={self.total}, treasure={self.treasure}, "
            f"normal={self.normal}, large_treasure={self.large_treasure}, "
            f"trophy_fish={self.trophy_fish})"
        )

class WinterStats:
    """
    Represents the player's Winter statistics.

    Attributes:
        most_snowballs_hit (float): Most snowballs hit by the player during a winter event.
        most_damage_dealt (float): Most damage dealt by the player during the winter event.
        most_magma_damage_dealt (float): Most magma damage dealt by the player during the winter event.
    """

    def __init__(self, data: dict) -> None:
        self.most_snowballs_hit: float = data.get('most_snowballs_hit', 0.0)
        self.most_damage_dealt: float = data.get('most_damage_dealt', 0.0)
        self.most_magma_damage_dealt: float = data.get('most_magma_damage_dealt', 0.0)


    def __str__(self) -> str:
        return (
            f"WinterStats(most_snowballs_hit={self.most_snowballs_hit}, "
            f"most_damage_dealt={self.most_damage_dealt}, "
            f"most_magma_damage_dealt={self.most_magma_damage_dealt})"
        )
    
class GiftsStats:
    """
    Represents the player's gift statistics.

    Attributes:
        total_received (float): Total number of gifts received by the player.
        total_given (float): Total number of gifts given by the player.
    """

    def __init__(self, data: dict) -> None:
        self.total_received: float = data.get('total_received', 0.0)
        self.total_given: float = data.get('total_given', 0.0)

    def __str__(self) -> str:
        return (
            f"GiftsStats(total_received={self.total_received}, "
            f"total_given={self.total_given})"
        )

class MostDamage:
    """
    Represents the most damage dealt to dragons of different types.

    Attributes:
        best (float): The highest damage dealt to any dragon.
        dragon_types (dict[str,float]): Dictionary mapping dragon types to damage dealt.
    """
    def __init__(self, data: dict) -> None:
        self.best: float = data.get('best', 0.0)
        self.dragon_types: dict[str,float] = {k: v for k, v in data.items() if k != 'best'}

    def get_damage(self, dragon_type: str) -> float:
        return self.dragon_types.get(dragon_type.lower(), 0.0)

    def __str__(self) -> str:
        return f"MostDamage(best={self.best}, dragon_types={self.dragon_types})"

class FastestKill:
    """
    Represents the fastest kill times for dragons of different types.

    Attributes:
        best (float): The fastest kill time for any dragon in milliseconds.
        dragon_types (dict[str,float]): Dictionary mapping dragon types to kill times in milliseconds.
    """
    def __init__(self, data: dict) -> None:
        self.best: float = data.get('best', 0.0)
        self.dragon_types: dict[str,float] = {k: v for k, v in data.items() if k != 'best'}

    def get_time(self, dragon_type: str) -> float:
        return self.dragon_types.get(dragon_type.lower(), 0.0)

    def __str__(self) -> str:
        return f"FastestKill(best={self.best}, dragon_types={self.dragon_types})"

class HighestRank:
    """
    Represents the highest rank achieved in dragon fights for different dragon types.

    Attributes:
        best (float): The highest rank achieved in any dragon fight.
        dragon_types (dict[str,float]): Dictionary mapping dragon types to highest ranks achieved.
    """
    def __init__(self, data: dict) -> None:
        self.best: float = data.get('best', 0.0)
        self.dragon_types: dict[str,float] = {k: v for k, v in data.items() if k != 'best'}

    def get_rank(self, dragon_type: str) -> float:
        return self.dragon_types.get(dragon_type.lower(), 0.0)

    def __str__(self) -> str:
        return f"HighestRank(best={self.best}, dragon_types={self.dragon_types})"

class DragonFightStats:
    """
    Represents the player's dragon fight statistics.

    Attributes:
        ender_crystals_destroyed (float): Number of ender crystals destroyed by the player.
        most_damage (MostDamage): Instance containing most damage dealt statistics.
        fastest_kill (FastestKill): Instance containing fastest kill times.
        highest_rank (HighestRank): Instance containing highest ranks achieved.
        amount_summoned (dict[str,float]): Number of dragons summoned by the player, per dragon type.
        summoning_eyes_contributed (dict[str,float]): Number of summoning eyes contributed, per dragon type.
    """

    def __init__(self, data: dict) -> None:
        self.ender_crystals_destroyed: float = data.get('ender_crystals_destroyed', 0.0)
        self.most_damage = MostDamage(data.get('most_damage', {}))
        self.fastest_kill = FastestKill(data.get('fastest_kill', {}))
        self.highest_rank = HighestRank(data.get('highest_rank', {}))
        self.amount_summoned: dict[str,float] = data.get('amount_summoned', {})
        self.summoning_eyes_contributed: dict[str,float] = data.get('summoning_eyes_contributed', {})

    def total_dragons_summoned(self) -> float:
        return self.amount_summoned.get('total', 0.0)

    def total_summoning_eyes_contributed(self) -> float:
        return self.summoning_eyes_contributed.get('total', 0.0)

    def __str__(self) -> str:
        return (
            f"DragonFightStats(ender_crystals_destroyed={self.ender_crystals_destroyed}, "
            f"most_damage={self.most_damage}, fastest_kill={self.fastest_kill}, "
            f"highest_rank={self.highest_rank}, amount_summoned={self.amount_summoned}, "
            f"summoning_eyes_contributed={self.summoning_eyes_contributed})"
        )

class EndIslandStats:
    """
    Represents the player's End Island statistics.

    Attributes:
        dragon_fight (DragonFightStats): Instance containing dragon fight statistics.
        special_zealot_loot_collected (float): Number of special zealot loots collected by the player.
    """
    def __init__(self, data: dict) -> None:
        self.dragon_fight = DragonFightStats(data.get('dragon_fight', {}))
        self.special_zealot_loot_collected: float = data.get('special_zealot_loot_collected', 0.0)

    def __str__(self) -> str:
        return (
            f"EndIslandStats(dragon_fight={self.dragon_fight}, "
            f"special_zealot_loot_collected={self.special_zealot_loot_collected})"
        )

class RaceTime:
    """
    Represents the best time for a specific race.

    Attributes:
        race_name (str): The name of the race.
        best_time (float): The best completion time in milliseconds.
    """

    def __init__(self, race_name: str, best_time: float) -> None:
        self.race_name: str = race_name
        self.best_time: float = best_time

    def __str__(self) -> str:
        return f"{self.race_name}: best_time={self.best_time}ms"

class RacesStats:
    """
    Represents the player's race statistics.

    Attributes:
        races (Dict[str, RaceTime]): Dictionary of race names and their best times.
    """

    def __init__(self, data: dict) -> None:
        self.races: dict[str,RaceTime] = self._extract_race_stats(data)

    def _extract_race_stats(self, data: dict) -> dict[str,RaceTime]:
        races = {}
        for key, value in data.items():
            if key.endswith('_best_time'):
                race_name = key.replace('_best_time', '').replace('_', ' ').title()
                races[race_name] = RaceTime(race_name, value)
            elif key == 'dungeon_hub':
                for dungeon_key, dungeon_value in data[key].items():
                    if dungeon_key.endswith('_best_time'):
                        race_name = dungeon_key.replace('_best_time', '').replace('_', ' ').title()
                        races[race_name] = RaceTime(race_name, dungeon_value)
        return races

    def get_race_time(self, race_name: str) -> RaceTime | None:
        """
        Get the best time for a specific race.

        Args:
            race_name (str): The name of the race.

        Returns:
            Optional[RaceTime]: The best time for the race or None if not found.
        """
        return self.races.get(race_name.title())

    def total_races_participated(self) -> int:
        """
        Get the total number of races participated in.

        Returns:
            int: Number of races.
        """
        return len(self.races)

    def __str__(self) -> str:
        race_list = ', '.join([str(race) for race in self.races.values()])
        return f"RacesStats(total_races={len(self.races)}, races=[{race_list}])"

class AuctionsStats:
    """
    Represents the player's auction statistics.

    Attributes:
        bids (float): Total number of bids placed.
        highest_bid (float): The highest bid placed.
        created (float): Number of auctions created.
        fees (float): Total fees paid.
        won (float): Number of auctions won.
        total_bought (Dict[str, float]): Statistics about items bought by rarity.
        gold_spent (float): Total gold spent in auctions.
        no_bids (float): Number of auctions with no bids.
        completed (float): Number of auctions completed.
        total_sold (Dict[str, float]): Statistics about items sold by rarity.
        gold_earned (float): Total gold earned from auctions.
    """

    def __init__(self, data: dict) -> None:
        self.bids: float = data.get('bids', 0.0)
        self.highest_bid: float = data.get('highest_bid', 0.0)
        self.created: float = data.get('created', 0.0)
        self.fees: float = data.get('fees', 0.0)
        self.won: float = data.get('won', 0.0)
        self.total_bought: dict[str,float] = data.get('total_bought', {})
        self.gold_spent: float = data.get('gold_spent', 0.0)
        self.no_bids: float = data.get('no_bids', 0.0)
        self.completed: float = data.get('completed', 0.0)
        self.total_sold: dict[str,float] = data.get('total_sold', {})
        self.gold_earned: float = data.get('gold_earned', 0.0)

    def get_total_items_bought(self) -> float:
        """
        Get the total number of items bought.

        Returns:
            float: Total items bought.
        """
        return self.total_bought.get('total', 0.0)

    def get_total_items_sold(self) -> float:
        """
        Get the total number of items sold.

        Returns:
            float: Total items sold.
        """
        return self.total_sold.get('total', 0.0)

    def get_items_bought_by_rarity(self, rarity: str) -> float:
        """
        Get the number of items bought of a specific rarity.

        Args:
            rarity (str): The rarity of the items.

        Returns:
            float: Number of items bought of that rarity.
        """
        return self.total_bought.get(rarity.upper(), 0.0)

    def get_items_sold_by_rarity(self, rarity: str) -> float:
        """
        Get the number of items sold of a specific rarity.

        Args:
            rarity (str): The rarity of the items.

        Returns:
            float: Number of items sold of that rarity.
        """
        return self.total_sold.get(rarity.upper(), 0.0)

    def net_profit(self) -> float:
        """
        Calculate the net profit from auctions.

        Returns:
            float: Net profit (gold earned - gold spent - fees).
        """
        return self.gold_earned - self.gold_spent - self.fees

    def __str__(self) -> str:
        return (
            f"AuctionsStats(bids={self.bids}, highest_bid={self.highest_bid}, "
            f"created={self.created}, gold_spent={self.gold_spent}, gold_earned={self.gold_earned})"
        )

class Pets:
    """
    Represents the pets player stats for upgrades and milestones that unlock pets (rock or dolphin pet)

    Attributes:
        ores_mined (float): Number of ores mined towards tied to the rock pet milestone
        sea_creatures_killed (float): Number of sea creatures killed towards the dolphin pet milestone
        total_exp_gained (float): Amount of exp gained in total for pets.
    """
    def __init__(self, data: dict[dict[str,float] | float]) -> None:
        self._milestone: dict[str,float] = data.get("milestone", {})
        self.ores_mined: float = self._milestone.get("ores_mined", 0.0)
        self.sea_creatures_killed: float = self._milestone.get("sea_creatures_killed", 0.0)
        self.total_exp_gained: float = data.get("total_exp_gained")

class FestivalCandyStats:
    """
    Represents candy statistics for a specific spooky festival.

    Attributes:
        festival_number (int): The festival number.
        total (int): Total candies collected during the festival.
        green_candy (int): Number of green candies collected.
        purple_candy (int): Number of purple candies collected.
    """
    def __init__(self, festival_number: int, data: dict) -> None:
        self.festival_number: int = festival_number
        self.total: int = data.get('total', 0)
        self.green_candy: int = data.get('green_candy', 0)
        self.purple_candy: int = data.get('purple_candy', 0)

    def __str__(self) -> str:
        return (
            f"Festival {self.festival_number}: total={self.total}, "
            f"green_candy={self.green_candy}, purple_candy={self.purple_candy}"
        )

class CandyCollected:
    """
    Represents the player's candy collected statistics.

    Attributes:
        total (int): Total candies collected.
        green_candy (int): Total green candies collected.
        purple_candy (int): Total purple candies collected.
        festivals (Dict[int, FestivalCandyStats]): Dictionary of festival numbers and their stats.
    """
    def __init__(self, data: dict) -> None:
        self.total: int = data.get('total', 0)
        self.green_candy: int = data.get('green_candy', 0)
        self.purple_candy: int = data.get('purple_candy', 0)
        self.festivals: dict[int,FestivalCandyStats] = self._extract_festival_stats(data)

    def _extract_festival_stats(self, data: dict) -> dict[int,FestivalCandyStats]:
        festivals = {}
        for key, value in data.items():
            if key.startswith('spooky_festival_'):
                festival_number = int(key.split('_')[-1])
                festivals[festival_number] = FestivalCandyStats(festival_number, value)
        return festivals

    def get_festival_stats(self, festival_number: int) -> FestivalCandyStats | None:
        """
        Get candy statistics for a specific festival.

        Args:
            festival_number (int): The festival number.

        Returns:
            Optional[FestivalCandyStats]: The stats for the festival or None if not found.
        """
        return self.festivals.get(festival_number)

    def total_festivals_participated(self) -> int:
        """
        Get the total number of festivals participated in.

        Returns:
            int: Number of festivals.
        """
        return len(self.festivals)

    def __str__(self) -> str:
        return (
            f"CandyCollected(total={self.total}, green_candy={self.green_candy}, "
            f"purple_candy={self.purple_candy}, festivals={len(self.festivals)})"
        )

class PlayerStats:
    """
    Represents the player's statistics data.

    Attributes:
        candy_collected (int): The total amount of candy collected.
        highest_critical_damage (int): The highest critical damage dealt.
        highest_damage (int): The highest damage dealt.
        kills (dict[str,int]): Dictionary of mob names and their kill counts.
        deaths (dict[str,int]): Dictionary of causes and their death counts.
        pets (dict[str,int]): Dictionary of pet-related stats.
        auctions (dict[str,int]): Dictionary of auction-related stats.
        races (dict[str,dict[str,int]]): Dictionary of race names and their stats.
        end_island (dict[str,int]): Dictionary of End Island stats.
        gifts (dict[str,int]): Dictionary of gift-related stats.
        winter (dict[str,int]): Dictionary of winter event stats.
        items_fished (dict[str,int]): Dictionary of items fished stats.
        mythos (dict[str,int]): Dictionary of mythos event stats.
        sea_creature_kills (dict[str,int]): Dictionary of sea creature kills.
        rift (dict[str,int]): Dictionary of Rift dimension stats.
        spooky (dict[str,int]): Dictionary of spooky event stats.
    """
    def __init__(self, player_stats: dict) -> None:
        self.candy_collected: CandyCollected = CandyCollected(player_stats.get('candy_collected', {}))
        self.highest_critical_damage: float = player_stats.get('highest_critical_damage', 0.0)
        self.highest_damage: float = player_stats.get('highest_damage', 0.0)
        self.kills: dict[str, float] = player_stats.get('kills', {}).copy()
        self.total_kills: float | None = self.kills.pop("total", None)# CHECK
        self.deaths: dict[str, int] = player_stats.get('deaths', {}).copy()
        self.total_deaths: float | None = self.deaths.pop("total", None) # CHECK
        self.pets: Pets = Pets(player_stats.get('pets', {}))
        self.auctions: AuctionsStats = AuctionsStats(player_stats.get('auctions', {}))
        self.races: RacesStats = RacesStats(player_stats.get('races', {}))
        self.end_island: EndIslandStats = EndIslandStats(player_stats.get('end_island', {}))
        self.gifts: GiftsStats = GiftsStats(player_stats.get('gifts', {}))
        self.winter: WinterStats = WinterStats(player_stats.get('winter', {}))
        self.items_fished: ItemsFishedStats = ItemsFishedStats(player_stats.get('items_fished', {}))
        self.mythos: MythosStats = MythosStats(player_stats.get('mythos', {}))
        self.sea_creature_kills: float = player_stats.get('sea_creature_kills', 0.0)
        self.rift: RiftStats = RiftStats(player_stats.get('rift', {}))
        self.spooky: SpookyStats = SpookyStats(player_stats.get('spooky', {}))

    def get_kill_count(self, mob_name: str) -> float:
        """
        Get the kill count for a specific mob.

        Args:
            mob_name (str): The name of the mob.

        Returns:
            int: The kill count for the mob, or 0 if not found.
        """
        return self.kills.get(mob_name, 0.0)

    def get_death_count(self, mob_name: str) -> float:
        """
        Get the death count for a specific mob.

        Args:
            mob_name (str): The name of the mob.

        Returns:
            int: The death count for the mob, or 0 if not found.
        """
        return self.deaths.get(mob_name, 0.0)

    def top_kills(self, n: int = 5) -> list[tuple[str, float]]:
        """
        Get the top N mobs by kill count.

        Args:
            n (int): The number of top mobs to return.

        Returns:
            list[tuple[str, int]]: A list of tuples containing mob names and kill counts.
        """
        sorted_kills = sorted(self.kills.items(), key=lambda item: item[1], reverse=True)
        return sorted_kills[:n]

    def top_deaths(self, n: int = 5) -> list[tuple[str, float]]:
        """
        Get the top N mobs by death count.

        Args:
            n (int): The number of top mobs to return.

        Returns:
            list[tuple[str, int]]: A list of tuples containing mob names and death counts.
        """
        sorted_deaths = sorted(self.deaths.items(), key=lambda item: item[1], reverse=True)
        return sorted_deaths[:n]

    def __str__(self) -> str:
        top_kills_str = ', '.join(f"{mob}: {count}" for mob, count in self.top_kills(3))
        top_deaths_str = ', '.join(f"{cause}: {count}" for cause, count in self.top_deaths(3))
        return (
            f"PlayerStats:\n"
            f"  Highest Critical Damage: {self.highest_critical_damage}\n"
            f"  Highest Damage: {self.highest_damage}\n"
            f"  Total Kills: {self.total_kills}\n"
            f"  Total Deaths: {self.total_deaths}\n"
            f"  Top Kills: {top_kills_str}\n"
            f"  Top Deaths: {top_deaths_str}\n"
            f"  Sea Creature Kills: {self.sea_creature_kills}"
        )