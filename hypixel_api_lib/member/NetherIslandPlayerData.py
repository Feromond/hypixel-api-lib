from datetime import datetime
from hypixel_api_lib.utils import convert_timestamp

class QuestStatus:
    """
    Represents the status of a quest.

    Attributes:
        status (str): The status of the quest.
        progress (int): The progress of the quest.
        completed_at (datetime): The completion time of the quest.
    """

    def __init__(self, data: dict) -> None:
        self.status: str = data.get('status', '')
        self.progress: int = data.get('progress', 0)
        self.completed_at: datetime | None = convert_timestamp(data.get('completed_at'))

    def __str__(self) -> str:
        return f"Status: {self.status}, Progress: {self.progress}, Completed At: {self.completed_at}"


class QuestData:
    """
    Represents the quest data.

    Attributes:
        fishing (QuestStatus): Fishing quest status.
        fetch (QuestStatus): Fetch quest status.
        dojo (QuestStatus): Dojo quest status.
        wanted_mini_boss (QuestStatus): Wanted miniboss quest status.
        boss (QuestStatus): Boss quest status.
        quest_list (list[str]): List of quests.
    """

    def __init__(self, data: dict) -> None:
        self.fishing: QuestStatus = QuestStatus(data.get('fishing', {}))
        self.fetch: QuestStatus = QuestStatus(data.get('fetch', {}))
        self.dojo: QuestStatus = QuestStatus(data.get('dojo', {}))
        self.wanted_mini_boss: QuestStatus = QuestStatus(data.get('wanted_mini_boss', {}))
        self.boss: QuestStatus = QuestStatus(data.get('boss', {}))
        self.quest_list: list[str] = data.get('quest_list', [])

    def __str__(self) -> str:
        return f"Quests: {self.quest_list}"


class AlchemistQuest:
    """
    Represents the alchemist quest.

    Attributes:
        progress (int): Progress of the alchemist quest.
        start (bool): Whether the quest has started.
    """

    def __init__(self, data: dict) -> None:
        self.progress: int = data.get('alchemist_quest_progress', 0)
        self.start: bool = data.get('alchemist_quest_start', False)

    def __str__(self) -> str:
        return f"Alchemist Quest - Progress: {self.progress}, Started: {self.start}"


class ChickenQuest:
    """
    Represents the chicken quest.

    Attributes:
        start (bool): Whether the quest has started.
        progress (int): Progress of the quest.
        collected (list[str]): List of collected items.
    """

    def __init__(self, data: dict) -> None:
        self.start: bool = data.get('chicken_quest_start', False)
        self.progress: int = data.get('chicken_quest_progress', 0)
        self.collected: list[str] = data.get('chicken_quest_collected', [])
        self.handed_in: datetime | None = None  # Will be set in Quests class if available

    def __str__(self) -> str:
        return f"Chicken Quest - Progress: {self.progress}, Collected: {self.collected}"


class MollimQuest:
    """
    Represents the Mollim quest.

    Attributes:
        talked_to_npc (bool): Whether the NPC has been talked to.
    """

    def __init__(self, data: dict) -> None:
        self.talked_to_npc: bool = data.get('talked_to_npc', False)

    def __str__(self) -> str:
        return f"Mollim Quest - Talked to NPC: {self.talked_to_npc}"


class AranyaQuest:
    """
    Represents the Aranya quest.

    Attributes:
        talked_to_npc (bool): Whether the NPC has been talked to.
        last_completion (datetime): Last completion time.
    """

    def __init__(self, data: dict) -> None:
        self.talked_to_npc: bool = data.get('talked_to_npc', False)
        self.last_completion: datetime | None = convert_timestamp(data.get('last_completion'))

    def __str__(self) -> str:
        return f"Aranya Quest - Talked to NPC: {self.talked_to_npc}, Last Completion: {self.last_completion}"


class Quests:
    """
    Represents all quests data.

    Attributes:
        quest_data (QuestData): Data about individual quests.
        miniboss_daily (dict[str,bool]): Miniboss daily statuses.
        quest_rewards (dict[str,dict]): Quest rewards.
        alchemist_quest (AlchemistQuest): Alchemist quest data.
        chicken_quest (ChickenQuest): Chicken quest data.
        mollim_quest (MollimQuest): Mollim quest data.
        aranya_quest (AranyaQuest): Aranya quest data.
        last_reset (int): Last reset value.
        paid_bruuh (bool): Whether Bruuh has been paid.
        chicken_quest_handed_in (datetime): Time when chicken quest was handed in.
    """

    def __init__(self, data: dict) -> None:
        self.quest_data: QuestData = QuestData(data.get('quest_data', {}))
        self.miniboss_daily: dict[str,bool] = data.get('miniboss_daily', {})
        self.kuuda_boss_daily: dict[str,dict] = data.get('kuuda_boss_daily', {})
        self.quest_rewards: dict[str,dict] = data.get('quest_rewards', {})
        self.alchemist_quest: AlchemistQuest = AlchemistQuest(data.get('alchemist_quest', {}))
        self.rulenor: dict[str,dict] = data.get('rulenor', {})
        self.chicken_quest: ChickenQuest = ChickenQuest(data.get('chicken_quest', {}))
        self.pomtair_quest: dict[str,dict] = data.get('pomtair_quest', {})
        self.suus_quest: dict[str,dict] = data.get('suus_quest', {})
        self.pablo_quest: dict[str,dict] = data.get('pablo_quest', {})
        self.duel_training_quest: dict[str,dict] = data.get('duel_training_quest', {})
        self.sirih_quest: dict[str,dict] = data.get('sirih_quest', {})
        self.edelis_quest: dict[str,dict] = data.get('edelis_quest', {})
        self.mollim_quest: MollimQuest = MollimQuest(data.get('mollim_quest', {}))
        self.aranya_quest: AranyaQuest = AranyaQuest(data.get('aranya_quest', {}))
        self.miniboss_data: dict[str,bool] = data.get('miniboss_data', {})
        self.last_reset: int = data.get('last_reset', 0)
        self.paid_bruuh: bool = data.get('paid_bruuh', False)
        self.chicken_quest_handed_in: datetime | None = convert_timestamp(data.get('chicken_quest_handed_in'))
        # Set handed_in time in chicken_quest if available
        self.chicken_quest.handed_in = self.chicken_quest_handed_in

    def __str__(self) -> str:
        return f"Quests Data - Last Reset: {self.last_reset}"


class KuudraCompletedTiers:
    """
    Represents Kuudra completed tiers.

    Attributes:
        none (int): Number of 'none' tier completions.
        hot (int): Number of 'hot' tier completions.
        burning (int): Number of 'burning' tier completions.
        fiery (int): Number of 'fiery' tier completions.
        infernal (int): Number of 'infernal' tier completions.
        highest_wave_hot (int): Highest wave reached in 'hot' tier.
        highest_wave_none (int): Highest wave reached in 'none' tier.
        highest_wave_burning (int): Highest wave reached in 'burning' tier.
        highest_wave_fiery (int): Highest wave reached in 'fiery' tier.
        highest_wave_infernal (int): Highest wave reached in 'infernal' tier.
    """

    def __init__(self, data: dict) -> None:
        self.none: int = data.get('none', 0)
        self.hot: int = data.get('hot', 0)
        self.burning: int = data.get('burning', 0)
        self.fiery: int = data.get('fiery', 0)
        self.infernal: int = data.get('infernal', 0)
        self.highest_wave_hot: int = data.get('highest_wave_hot', 0)
        self.highest_wave_none: int = data.get('highest_wave_none', 0)
        self.highest_wave_burning: int = data.get('highest_wave_burning', 0)
        self.highest_wave_fiery: int = data.get('highest_wave_fiery', 0)
        self.highest_wave_infernal: int = data.get('highest_wave_infernal', 0)

    def __str__(self) -> str:
        return f"Kuudra Completed Tiers - None: {self.none}, Hot: {self.hot}"


class Dojo:
    """
    Represents Dojo stats.

    Attributes:
        dojo_points_mob_kb (int): Points in mob knockback.
        dojo_time_mob_kb (int): Time in mob knockback.
        dojo_points_wall_jump (int): Points in wall jump.
        dojo_time_wall_jump (int): Time in wall jump.
        dojo_points_archer (int): Points in archer.
        dojo_time_archer (int): Time in archer.
        dojo_points_snake (int): Points in snake.
        dojo_time_snake (int): Time in snake.
        dojo_points_lock_head (int): Points in lock head.
        dojo_time_lock_head (int): Time in lock head.
        dojo_points_sword_swap (int): Points in sword swap.
        dojo_time_sword_swap (int): Time in sword swap.
        dojo_points_fireball (int): Points in fireball.
        dojo_time_fireball (int): Time in fireball.
    """

    def __init__(self, data: dict) -> None:
        self.dojo_points_mob_kb: int = data.get('dojo_points_mob_kb', 0)
        self.dojo_time_mob_kb: int = data.get('dojo_time_mob_kb', 0)
        self.dojo_points_wall_jump: int = data.get('dojo_points_wall_jump', 0)
        self.dojo_time_wall_jump: int = data.get('dojo_time_wall_jump', 0)
        self.dojo_points_archer: int = data.get('dojo_points_archer', 0)
        self.dojo_time_archer: int = data.get('dojo_time_archer', 0)
        self.dojo_points_snake: int = data.get('dojo_points_snake', 0)
        self.dojo_time_snake: int = data.get('dojo_time_snake', 0)
        self.dojo_points_lock_head: int = data.get('dojo_points_lock_head', 0)
        self.dojo_time_lock_head: int = data.get('dojo_time_lock_head', 0)
        self.dojo_points_sword_swap: int = data.get('dojo_points_sword_swap', 0)
        self.dojo_time_sword_swap: int = data.get('dojo_time_sword_swap', 0)
        self.dojo_points_fireball: int = data.get('dojo_points_fireball', 0)
        self.dojo_time_fireball: int = data.get('dojo_time_fireball', 0)

    def __str__(self) -> str:
        return "Dojo Stats"


class AbiphoneContact:
    """
    Represents an Abiphone contact.

    Attributes:
        talked_to (bool): Whether the contact has been talked to.
        completed_quest (bool): Whether the quest is completed.
        last_call (datetime): Last call time.
        incoming_calls_count (int): Number of incoming calls.
        last_call_incoming (datetime): Last incoming call time.
        dnd_enabled (bool): Do Not Disturb enabled.
        specific (dict[str,dict]): Specific data for the contact.
    """

    def __init__(self, data: dict) -> None:
        self.talked_to: bool = data.get('talked_to', False)
        self.completed_quest: bool = data.get('completed_quest', False)
        self.last_call: datetime | None = convert_timestamp(data.get('last_call'))
        self.incoming_calls_count: int = data.get('incoming_calls_count', 0)
        self.last_call_incoming: datetime | None = convert_timestamp(data.get('last_call_incoming'))
        self.dnd_enabled: bool = data.get('dnd_enabled', False)
        self.specific: dict[str,dict] = data.get('specific', {})

    def __str__(self) -> str:
        return f"Contact - Talked to: {self.talked_to}, Completed Quest: {self.completed_quest}"


class AbiphoneGames:
    """
    Represents games played on the Abiphone.

    Attributes:
        tic_tac_toe_draws (int): Number of Tic Tac Toe draws.
        tic_tac_toe_losses (int): Number of Tic Tac Toe losses.
        snake_best_score (int): Best score in Snake game.
    """

    def __init__(self, data: dict) -> None:
        self.tic_tac_toe_draws: int = data.get('tic_tac_toe_draws', 0)
        self.tic_tac_toe_losses: int = data.get('tic_tac_toe_losses', 0)
        self.snake_best_score: int = data.get('snake_best_score', 0)

    def __str__(self) -> str:
        return f"Games - Tic Tac Toe Draws: {self.tic_tac_toe_draws}"


class Abiphone:
    """
    Represents the Abiphone data.

    Attributes:
        contact_data (dict[str,AbiphoneContact]): Contacts data.
        games (AbiphoneGames): Games data.
        active_contacts (list[str]): List of active contacts.
        operator_chip (dict[str,dict]): Operator chip data.
        trio_contact_addons (int): Number of trio contact addons.
        selected_sort (str): Selected sort option.
    """

    def __init__(self, data: dict) -> None:
        self.contact_data: dict[str,AbiphoneContact] = self._parse_contact_data(data.get('contact_data', {}))
        self.games: AbiphoneGames = AbiphoneGames(data.get('games', {}))
        self.active_contacts: list[str] = data.get('active_contacts', [])
        self.operator_chip: dict[str,dict] = data.get('operator_chip', {})
        self.trio_contact_addons: int = data.get('trio_contact_addons', 0)
        self.selected_sort: str = data.get('selected_sort', '')

    def _parse_contact_data(self, data: dict) -> dict[str,AbiphoneContact]:
        return {name: AbiphoneContact(contact_data) for name, contact_data in data.items()}

    def __str__(self) -> str:
        return f"Abiphone - Active Contacts: {len(self.active_contacts)}"


class Matriarch:
    """
    Represents the Matriarch data.

    Attributes:
        last_attempt (datetime): Last attempt time.
        pearls_collected (int): Number of pearls collected.
        recent_refreshes (list[datetime]): List of recent refresh times.
    """

    def __init__(self, data: dict) -> None:
        self.last_attempt: datetime | None = convert_timestamp(data.get('last_attempt'))
        self.pearls_collected: int = data.get('pearls_collected', 0)
        self.recent_refreshes: list[datetime | None] = [
            convert_timestamp(ts) for ts in data.get('recent_refreshes', [])
        ]

    def __str__(self) -> str:
        return f"Matriarch - Pearls Collected: {self.pearls_collected}"


class SearchSettings:
    """
    Represents search settings for Kuudra party finder.

    Attributes:
        tier (str): Tier to search for.
    """

    def __init__(self, data: dict) -> None:
        self.tier: str = data.get('tier', '')

    def __str__(self) -> str:
        return f"Search Settings - Tier: {self.tier}"


class GroupBuilder:
    """
    Represents group builder settings.

    Attributes:
        tier (str): Tier for the group.
        note (str): Note for the group.
        combat_level_required (int): Required combat level.
    """

    def __init__(self, data: dict) -> None:
        self.tier: str = data.get('tier', '')
        self.note: str = data.get('note', '')
        self.combat_level_required: int = data.get('combat_level_required', 0)

    def __str__(self) -> str:
        return f"Group Builder - Tier: {self.tier}, Note: {self.note}"


class KuudraPartyFinder:
    """
    Represents the Kuudra party finder data.

    Attributes:
        search_settings (SearchSettings): Search settings.
        group_builder (GroupBuilder): Group builder settings.
    """

    def __init__(self, data: dict) -> None:
        self.search_settings: SearchSettings = SearchSettings(data.get('search_settings', {}))
        self.group_builder: GroupBuilder = GroupBuilder(data.get('group_builder', {}))

    def __str__(self) -> str:
        return "Kuudra Party Finder"


class NetherIslandPlayerData:
    """
    Represents the Nether Island player data.

    Attributes:
        quests (Quests): Quests data.
        kuudra_completed_tiers (KuudraCompletedTiers): Kuudra tiers data.
        dojo (Dojo): Dojo data.
        abiphone (Abiphone): Abiphone data.
        matriarch (Matriarch): Matriarch data.
        mages_reputation (float): Reputation with mages.
        barbarians_reputation (float): Reputation with barbarians.
        selected_faction (str): Selected faction.
        last_minibosses_killed (list[str]): List of last minibosses killed.
        kuudra_party_finder (KuudraPartyFinder): Kuudra party finder data.
    """

    def __init__(self, data: dict) -> None:
        self.quests: Quests = Quests(data.get('quests', {}))
        self.kuudra_completed_tiers: KuudraCompletedTiers = KuudraCompletedTiers(
            data.get('kuudra_completed_tiers', {})
        )
        self.dojo: Dojo = Dojo(data.get('dojo', {}))
        self.abiphone: Abiphone = Abiphone(data.get('abiphone', {}))
        self.matriarch: Matriarch = Matriarch(data.get('matriarch', {}))
        self.mages_reputation: float = data.get('mages_reputation', 0.0)
        self.barbarians_reputation: float = data.get('barbarians_reputation', 0.0)
        self.selected_faction: str = data.get('selected_faction', '')
        self.last_minibosses_killed: list[str] = data.get('last_minibosses_killed', [])
        self.kuudra_party_finder: KuudraPartyFinder = KuudraPartyFinder(data.get('kuudra_party_finder', {}))

    def __str__(self) -> str:
        return (
            f"NetherIslandPlayerData - Faction: {self.selected_faction}, "
            f"Mages Reputation: {self.mages_reputation}, "
            f"Barbarians Reputation: {self.barbarians_reputation}"
        )
