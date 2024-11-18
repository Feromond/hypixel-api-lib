from datetime import datetime
from hypixel_api_lib.utils import convert_timestamp, get_username_from_uuid
from .PlayerData import PlayerData
from .GlacitePlayerData import GlacitePlayerData
from .Events import Events
from .GardenPlayerData import GardenPlayerData
from .PetsData import PetsData
from .Rift import RiftData
from .AccessoryBagStorage import AccessoryBagStorage
from .Leveling import LevelingData
from .ItemData import ItemData
from .JacobsContest import JacobsContestData
from .Currencies import Currencies
from .dungeons import Dungeons
from .ProfileStats import ProfileStats
from .NetherIslandPlayerData import NetherIslandPlayerData
from .Experimentation import Experimentation
from .MiningCore import MiningCore
from .Bestiary import Bestiary
from .Quests import Quests
from .PlayerStats import PlayerStats
from .Slayer import Slayer
from .TrophyFish import TrophyFishStats
from .Objectives import Objectives
from .CollectionsStats import CollectionsStats

class DeletionNotice:
    """
    Represents a deletion notice for a member profile.

    Attributes:
        timestamp (datetime): The timestamp when the deletion notice was issued.
    """

    def __init__(self, data: dict) -> None:
        self.timestamp: datetime | None = convert_timestamp(data.get('timestamp'))

    def __str__(self) -> str:
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else 'N/A'
        return f"Deletion Notice at {timestamp_str}"

class SkyBlockProfileMember:
    """
    Represents a member of a SkyBlock profile.

    Attributes:
        uuid (str): The UUID of the member.
        rift (RiftData): Rift-related data.
        player_data (PlayerData): General player data.
        glacite_player_data (GlacitePlayerData): Glacite-specific player data.
        events (Events): Event-related data.
        garden_player_data (GardenPlayerData): Garden player data.
        pets_data (PetsData): Data about pets.
        accessory_bag_storage (AccessoryBagStorage): Accessory bag storage data.
        leveling (LevelingData): Leveling data.
        item_data (ItemData): Item data.
        jacobs_contest (JacobsContestData): Jacob's contest data.
        currencies (Currencies): Currency data.
        dungeons (Dungeons): Dungeon-related data.
        profile (ProfileStats): Profile statistics data.
        deleted_member (bool): Indicates if the member has been marked as deleted.
        deleted_timestamp (DeletionNotice | None): Deletion notice timestamp if member is deleted.
        player_id (str): The player ID.
        nether_island_player_data (NetherIslandPlayerData): Nether island data.
        experimentation (Experimentation): Experimentation data.
        mining_core (MiningCore): Mining core data.
        bestiary (Bestiary): Bestiary data.
        quests (Quests): Quest data.
        player_stats (PlayerStats): Player statistics.
        winter_player_data (dict): Winter event data.
        forge (dict): Forge data.
        fairy_soul (dict): Fairy soul data.
        slayer (Slayer): Slayer data.
        trophy_fish (TrophyFishStats): Trophy fish data.
        objectives (Objectives): Objectives data.
        inventory (dict): Inventory data containing NBT data representing items and positions.
        shared_inventory (dict): Shared inventory data.
        collection (CollectionsStats): Collection data.
    """

    def __init__(self, uuid: str, data: dict) -> None:
        self.uuid: str = uuid
        try:
            self.username: str = get_username_from_uuid(self.uuid)
        except ConnectionError:
            self.username : str = "Unknown"
        except ValueError:
            self.username : str = "Unknown"
        self.rift: RiftData = RiftData(data.get('rift', {}))
        self.player_data: PlayerData = PlayerData(data.get('player_data', {}))
        self.glacite_player_data: GlacitePlayerData = GlacitePlayerData(data.get('glacite_player_data', {}))
        self.events: Events = Events(data.get('events', {}))
        self.garden_player_data: GardenPlayerData = GardenPlayerData(data.get('garden_player_data', {}))
        self.pets_data: PetsData = PetsData(data.get('pets_data', {}))
        self.accessory_bag_storage: AccessoryBagStorage = AccessoryBagStorage(data.get('accessory_bag_storage', {}))
        self.leveling: LevelingData = LevelingData(data.get('leveling', {}))
        self.item_data: ItemData = ItemData(data.get('item_data', {}))
        self.jacobs_contest: JacobsContestData = JacobsContestData(data.get('jacobs_contest', {}))
        self.currencies: Currencies = Currencies(data.get('currencies', {}))
        self.dungeons: Dungeons = Dungeons(data.get('dungeons', {}))
        self.profile: ProfileStats = ProfileStats(data.get('profile', {}))
        self.deleted_member: bool = self.is_member_deleted()
        self.deleted_timestamp: DeletionNotice | None = DeletionNotice(self.profile.deletion_notice) if self.deleted_member else None
        self.player_id: str = data.get('player_id')
        self.nether_island_player_data: NetherIslandPlayerData = NetherIslandPlayerData(data.get('nether_island_player_data', {}))
        self.experimentation: Experimentation = Experimentation(data.get('experimentation', {}))
        self.mining_core: MiningCore = MiningCore(data.get('mining_core', {}))
        self.bestiary: Bestiary = Bestiary(data.get('bestiary', {}))
        self.quests: Quests = Quests(data.get('quests', {}))
        self.player_stats: PlayerStats = PlayerStats(data.get('player_stats', {}))
        self.winter_player_data: dict = data.get('winter_player_data', {})
        self.forge: dict = data.get('forge', {})
        self.fairy_soul: dict = data.get('fairy_soul', {})
        self.slayer: Slayer = Slayer(data.get('slayer', {}))
        self.trophy_fish: TrophyFishStats = TrophyFishStats(data.get('trophy_fish', {}))
        self.objectives: Objectives = Objectives(data.get('objectives', {}))
        self.inventory: dict = data.get('inventory', {}) # TODO: Inventory is HUGE with some kind of NBT data maybe representing items and inventory positions
        self.shared_inventory: dict = data.get('shared_inventory', {}) # TODO: Maybe a todo, extract some of he data again if needed
        self.collection: CollectionsStats = CollectionsStats(data.get('collection', {}))

    def is_member_deleted(self) -> bool:
        """Check if the current member has been marked as deleted in this profile"""
        return bool(self.profile.deletion_notice)


    def __str__(self) -> str:
        return f"SkyBlockProfileMember Username: {self.username}, UUID: {self.uuid}"