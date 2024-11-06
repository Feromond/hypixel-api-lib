from datetime import datetime, timezone
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

class DeletionNotice:
    """
    Represents a deletion notice for a member profile.

    Attributes:
        timestamp (datetime): The timestamp when the deletion notice was issued.
    """

    def __init__(self, data):
        self.timestamp = self._convert_timestamp(data.get('timestamp'))

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else 'N/A'
        return f"Deletion Notice at {timestamp_str}"



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

    def __init__(self, uuid, data):
        self.uuid = uuid
        self.rift = RiftData(data.get('rift', {}))
        self.player_data = PlayerData(data.get('player_data', {}))
        self.glacite_player_data = GlacitePlayerData(data.get('glacite_player_data', {}))
        self.events = Events(data.get('events', {}))
        self.garden_player_data = GardenPlayerData(data.get('garden_player_data', {}))
        self.pets_data = PetsData(data.get('pets_data', {}))
        self.accessory_bag_storage = AccessoryBagStorage(data.get('accessory_bag_storage', {}))
        self.leveling = LevelingData(data.get('leveling', {}))
        self.item_data = ItemData(data.get('item_data', {}))
        self.jacobs_contest = JacobsContestData(data.get('jacobs_contest', {}))
        self.currencies = data.get('currencies', {})
        self.dungeons = data.get('dungeons', {})
        self.profile = data.get('profile', {})
        self.deleted_member = self.is_member_deleted()
        self.deleted_timestamp = DeletionNotice(self.profile.get("deletion_notice")) if self.deleted_member else None
        self.player_id = data.get('player_id')
        self.nether_island_player_data = data.get('nether_island_player_data', {})
        self.experimentation = data.get('experimentation', {})
        self.mining_core = data.get('mining_core', {})
        self.bestiary = data.get('bestiary', {})
        self.quests = data.get('quests', {})
        self.player_stats = data.get('player_stats', {})
        self.winter_player_data = data.get('winter_player_data', {})
        self.forge = data.get('forge', {})
        self.fairy_soul = data.get('fairy_soul', {})
        self.slayer = data.get('slayer', {})
        self.trophy_fish = data.get('trophy_fish', {})
        self.objectives = data.get('objectives', {})
        self.inventory = data.get('inventory', {})
        self.shared_inventory = data.get('shared_inventory', {})
        self.collection = data.get('collection', {})

    def is_member_deleted(self):
        """Check if the current member has been marked as deleted in this profile"""
        if self.profile.get("deletion_notice"):
            return True
        return False

    def __str__(self):
        return f"SkyBlockProfileMember UUID: {self.uuid}"