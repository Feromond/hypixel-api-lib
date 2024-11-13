from datetime import datetime
from hypixel_api_lib.utils import convert_timestamp
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
from .Profile import Profile
from .NetherIslandPlayerData import NetherIslandPlayerData
from .Experimentation import Experimentation

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


# TODO: Finish profile members and develop all the sub field data classes for them still. (last updated before dungeons)
class SkyBlockProfileMember:
    """
    Represents a member of a SkyBlock profile.

    Attributes:
        uuid (str): The UUID of the member.
        rift (dict): Rift-related data.
        player_data (dict): General player data.
        glacite_player_data (dict): Glacite-specific player data.
        events (dict): Event-related data.
        garden_player_data (dict): Garden player data.
        pets_data (dict): Data about pets.
        accessory_bag_storage (dict): Accessory bag storage data.
        leveling (dict): Leveling data.
        item_data (dict): Item data.
        jacobs_contest (dict): Jacob's contest data.
        currencies (dict): Currency data.
        dungeons (dict): Dungeon-related data.
        profile (dict): Profile data.
        player_id (str): The player ID.
        nether_island_player_data (dict): Nether island data.
        experimentation (dict): Experimentation data.
        mining_core (dict): Mining core data.
        bestiary (dict): Bestiary data.
        quests (dict): Quest data.
        player_stats (dict): Player statistics.
        winter_player_data (dict): Winter event data.
        forge (dict): Forge data.
        fairy_soul (dict): Fairy soul data.
        slayer (dict): Slayer data.
        trophy_fish (dict): Trophy fish data.
        objectives (dict): Objectives data.
        inventory (dict): Inventory data.
        shared_inventory (dict): Shared inventory data.
        collection (dict): Collection data.
    """

    def __init__(self, uuid: str, data: dict) -> None:
        self.uuid: str = uuid
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
        self.profile: Profile = Profile(data.get('profile', {}))
        self.deleted_member: bool = self.is_member_deleted()
        self.deleted_timestamp: DeletionNotice | None = DeletionNotice(self.profile.deletion_notice) if self.deleted_member else None
        self.player_id: str = data.get('player_id')
        self.nether_island_player_data: NetherIslandPlayerData = NetherIslandPlayerData(data.get('nether_island_player_data', {}))
        self.experimentation: Experimentation = Experimentation(data.get('experimentation', {}))
        self.mining_core: dict = data.get('mining_core', {})
        self.bestiary: dict = data.get('bestiary', {})
        self.quests: dict = data.get('quests', {})
        self.player_stats: dict = data.get('player_stats', {})
        self.winter_player_data: dict = data.get('winter_player_data', {})
        self.forge: dict = data.get('forge', {})
        self.fairy_soul: dict = data.get('fairy_soul', {})
        self.slayer: dict = data.get('slayer', {})
        self.trophy_fish: dict = data.get('trophy_fish', {})
        self.objectives: dict = data.get('objectives', {})
        self.inventory: dict = data.get('inventory', {})
        self.shared_inventory: dict = data.get('shared_inventory', {})
        self.collection: dict = data.get('collection', {})

    def is_member_deleted(self) -> bool:
        """Check if the current member has been marked as deleted in this profile"""
        if self.profile.deletion_notice:
            return True
        return False

    def __str__(self) -> str:
        return f"SkyBlockProfileMember UUID: {self.uuid}"