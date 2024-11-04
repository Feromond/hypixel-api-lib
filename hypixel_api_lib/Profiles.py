import requests
from datetime import datetime, timezone

PROFILE_API_URL = r"https://api.hypixel.net/v2/skyblock/profile"
PROFILES_API_URL = r"https://api.hypixel.net/v2/skyblock/profiles"

class CommunityUpgradeState:
    """
    Represents a completed community upgrade.

    Attributes:
        upgrade (str): The name of the upgrade.
        tier (int): The tier level of the upgrade.
        started_ms (datetime): The datetime when the upgrade started.
        started_by (str): The UUID of the player who started the upgrade.
        claimed_ms (datetime): The datetime when the upgrade was claimed.
        claimed_by (str): The UUID of the player who claimed the upgrade.
        fasttracked (bool): Whether the upgrade was fast-tracked.
    """

    def __init__(self, data):
        self.upgrade = data.get('upgrade')
        self.tier = data.get('tier')
        self.started_ms = self._convert_timestamp(data.get('started_ms'))
        self.started_by = data.get('started_by')
        self.claimed_ms = self._convert_timestamp(data.get('claimed_ms'))
        self.claimed_by = data.get('claimed_by')
        self.fasttracked = data.get('fasttracked', False)

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        return f"Upgrade: {self.upgrade}, Tier: {self.tier}, Fasttracked: {self.fasttracked}"


class CommunityUpgrades:
    """
    Represents the community upgrades of a SkyBlock profile.

    Attributes:
        currently_upgrading (CommunityUpgradeState or None): The current upgrade in progress.
        upgrade_states (list of CommunityUpgradeState): A list of completed upgrades.
    """

    def __init__(self, data):
        currently_upgrading_data = data.get('currently_upgrading')
        self.currently_upgrading = (
            CommunityUpgradeState(currently_upgrading_data) if currently_upgrading_data else None
        )
        self.upgrade_states = [
            CommunityUpgradeState(upgrade_data) for upgrade_data in data.get('upgrade_states', [])
        ]

    def __str__(self):
        upgrading = str(self.currently_upgrading) if self.currently_upgrading else "None"
        return f"Community Upgrades (Currently Upgrading: {upgrading})"


class BankTransaction:
    """
    Represents a bank transaction.

    Attributes:
        timestamp (datetime): The timestamp of the transaction.
        action (str): The action of the transaction ('DEPOSIT' or 'WITHDRAW').
        initiator_name (str): The name of the player who initiated the transaction.
        amount (float): The amount of the transaction.
    """

    def __init__(self, data):
        self.timestamp = self._convert_timestamp(data.get('timestamp'))
        self.action = data.get('action')
        self.initiator_name = data.get('initiator_name')
        self.amount = data.get('amount')

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else 'N/A'
        return f"{self.action} of {self.amount} by {self.initiator_name} at {timestamp_str}"


class Banking:
    """
    Represents the banking information of a SkyBlock profile.

    Attributes:
        balance (float): The current balance of the bank.
        transactions (list of BankTransaction): A list of bank transactions.
    """

    def __init__(self, data):
        self.balance = data.get('balance', 0.0)
        self.transactions = [BankTransaction(txn) for txn in data.get('transactions', [])]

    def __str__(self):
        return f"Banking Balance: {self.balance}, Transactions: {len(self.transactions)}"


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

class EasterTimeTower:
    """
    Represents the time tower data in the Easter event.

    Attributes:
        charges (int): Number of charges left.
        activation_time (datetime): Time when the tower was activated.
        level (int): Level of the time tower.
        last_charge_time (datetime): Time when the last charge was used.
    """

    def __init__(self, data):
        self.charges = data.get('charges', 0)
        self.activation_time = self._convert_timestamp(data.get('activation_time'))
        self.level = data.get('level', 0)
        self.last_charge_time = self._convert_timestamp(data.get('last_charge_time'))

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        activation_time_str = self.activation_time.strftime('%Y-%m-%d %H:%M:%S') if self.activation_time else 'N/A'
        last_charge_time_str = self.last_charge_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_charge_time else 'N/A'
        return (f"EasterTimeTower(Charges: {self.charges}, Level: {self.level}, "
                f"Activation Time: {activation_time_str}, Last Charge Time: {last_charge_time_str})")


class EasterEmployees:
    """
    Represents the employees data in the Easter event.

    Attributes:
        employee_levels (dict of str to int): Mapping of employee names to their levels.
    """

    def __init__(self, data):
        self.employee_levels = data

    def __str__(self):
        return f"EasterEmployees(Employee Levels: {self.employee_levels})"


class EasterShop:
    """
    Represents the shop data in the Easter event.

    Attributes:
        year (int): The in-game year of the event.
        rabbits (list of str): List of rabbits available in the shop.
        rabbits_purchased (list of str): List of rabbits purchased by the player.
        chocolate_spent (int): Total chocolate spent in the shop.
        cocoa_fortune_upgrades (int): Number of cocoa fortune upgrades purchased.
    """

    def __init__(self, data):
        self.year = data.get('year', 0)
        self.rabbits = data.get('rabbits', [])
        self.rabbits_purchased = data.get('rabbits_purchased', [])
        self.chocolate_spent = data.get('chocolate_spent', 0)
        self.cocoa_fortune_upgrades = data.get('cocoa_fortune_upgrades', 0)

    def __str__(self):
        return (f"EasterShop(Year: {self.year}, Rabbits Purchased: {len(self.rabbits_purchased)}, "
                f"Chocolate Spent: {self.chocolate_spent})")


class EasterRabbitsData:
    """
    Represents the rabbits data in the Easter event.

    Attributes:
        collected_eggs (dict of str to int): Number of eggs collected per meal type.
        rabbit_counts (dict of str to int): Counts of each rabbit collected.
    """

    def __init__(self, data):
        self.collected_eggs = data.get('collected_eggs', {})
        self.collected_locations = data.get('collected_locations', {})
        # Exclude 'collected_eggs' and 'collected_locations' from rabbit_counts
        self.rabbit_counts = {k: v for k, v in data.items() if k not in ('collected_eggs', 'collected_locations')}

    def __str__(self):
        return (f"EasterRabbitsData(Collected Eggs: {self.collected_eggs}, "
                f"Rabbit Counts: {len(self.rabbit_counts)} rabbits)")


class EasterEvent:
    """
    Represents the data for the Easter event.

    Attributes:
        chocolate (int): Current chocolate count.
        chocolate_since_prestige (int): Chocolate earned since the last prestige.
        total_chocolate (int): Total chocolate earned.
        rabbits_data (EasterRabbitsData): Data about rabbits.
        shop (EasterShop): Shop-related data.
        employees (EasterEmployees): Employee-related data.
        last_viewed_chocolate_factory (datetime): Timestamp of the last chocolate factory view.
        rabbit_barn_capacity_level (int): Level of the rabbit barn capacity.
        chocolate_level (int): Current chocolate level.
        time_tower (EasterTimeTower): Time tower data.
        rabbit_sort (str): Sorting preference for rabbits.
        rabbit_filter (str): Filter preference for rabbits.
        el_dorado_progress (int): Progress towards El Dorado.
        chocolate_multiplier_upgrades (int): Number of chocolate multiplier upgrades.
        click_upgrades (int): Number of click upgrades.
        rabbit_rarity_upgrades (int): Number of rabbit rarity upgrades.
    """

    def __init__(self, data):
        self.chocolate = data.get('chocolate', 0)
        self.chocolate_since_prestige = data.get('chocolate_since_prestige', 0)
        self.total_chocolate = data.get('total_chocolate', 0)
        self.rabbits_data = EasterRabbitsData(data.get('rabbits', {}))
        self.shop = EasterShop(data.get('shop', {}))
        self.employees = EasterEmployees(data.get('employees', {}))
        self.last_viewed_chocolate_factory = self._convert_timestamp(data.get('last_viewed_chocolate_factory'))
        self.rabbit_barn_capacity_level = data.get('rabbit_barn_capacity_level', 0)
        self.chocolate_level = data.get('chocolate_level', 0)
        self.time_tower = EasterTimeTower(data.get('time_tower', {}))
        self.rabbit_sort = data.get('rabbit_sort', '')
        self.rabbit_filter = data.get('rabbit_filter', '')
        self.el_dorado_progress = data.get('el_dorado_progress', 0)
        self.chocolate_multiplier_upgrades = data.get('chocolate_multiplier_upgrades', 0)
        self.click_upgrades = data.get('click_upgrades', 0)
        self.rabbit_rarity_upgrades = data.get('rabbit_rarity_upgrades', 0)

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        return (f"EasterEvent(Chocolate: {self.chocolate}, Total Chocolate: {self.total_chocolate}, "
                f"RabbitsData: {self.rabbits_data}, Shop: {self.shop}, Employees: {self.employees}, "
                f"TimeTower: {self.time_tower})")


class Events:
    """
    Represents the events data for a SkyBlock profile member.

    Attributes:
        easter (EasterEvent): Data related to the Easter event.
        # Additional events can be added here as needed.
    """

    def __init__(self, data):
        self.easter = EasterEvent(data.get('easter', {})) if 'easter' in data else None

    def __str__(self):
        return f"Events(Easter: {self.easter})"


class GlacitePlayerData:
    """
    Represents the glacite player data for a SkyBlock profile member.

    Attributes:
        fossils_donated (list of str): List of fossils donated.
        fossil_dust (float): Amount of fossil dust.
        corpses_looted (dict of str to int): Mapping of corpse types to the number looted.
        mineshafts_entered (int): Number of mineshafts entered.
    """

    def __init__(self, data):
        self.fossils_donated = data.get('fossils_donated', [])
        self.fossil_dust = data.get('fossil_dust', 0.0)
        self.corpses_looted = data.get('corpses_looted', {})
        self.mineshafts_entered = data.get('mineshafts_entered', 0)

    def __str__(self):
        return (f"GlacitePlayerData(Fossils Donated: {self.fossils_donated}, "
                f"Fossil Dust: {self.fossil_dust}, Corpses Looted: {self.corpses_looted}, "
                f"Mineshafts Entered: {self.mineshafts_entered})")


class Perk:
    """
    Represents a perk and its level.

    Attributes:
        name (str): The name of the perk.
        level (int): The level of the perk.
    """

    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __str__(self):
        return f"{self.name}: Level {self.level}"

class SkillExperience:
    """
    Represents experience in a specific skill.

    Attributes:
        skill_name (str): The name of the skill.
        experience (float): The amount of experience in the skill.
    """

    def __init__(self, skill_name, experience):
        self.skill_name = skill_name
        self.experience = experience

    def __str__(self):
        return f"{self.skill_name}: {self.experience} XP"
    
    def __repr__(self):
        return f"{self.skill_name}: {self.experience} XP"


class PlayerData:
    """
    Represents the player data for a SkyBlock profile member.

    Attributes:
        visited_zones (list of str): List of zones the player has visited.
        last_death (datetime): Datetime of the player's last death.
        perks (dict of str to int): Perks and their levels.
        active_effects (list): List of active effects.
        paused_effects (list): List of paused effects.
        temp_stat_buffs (list): List of temporary stat buffs.
        death_count (int): Total number of deaths.
        disabled_potion_effects (list of str): List of disabled potion effects.
        achievement_spawned_island_types (list of str): List of spawned island types for achievements.
        visited_modes (list of str): List of game modes the player has visited.
        unlocked_coll_tiers (list of str): List of unlocked collection tiers.
        crafted_generators (list of str): List of crafted generators.
        fastest_target_practice (float): Fastest time in target practice.
        fishing_treasure_caught (int): Number of fishing treasures caught.
        experience (dict of str to float): Experience in various skills.
    """

    def __init__(self, data):
        self.visited_zones = data.get('visited_zones', [])
        self.last_death = self._convert_timestamp(data.get('last_death'))
        self.perks = self._parse_perks(data.get('perks', {}))
        self.active_effects = data.get('active_effects', [])
        self.paused_effects = data.get('paused_effects', [])
        self.temp_stat_buffs = data.get('temp_stat_buffs', [])
        self.death_count = data.get('death_count', 0)
        self.disabled_potion_effects = data.get('disabled_potion_effects', [])
        self.achievement_spawned_island_types = data.get('achievement_spawned_island_types', [])
        self.visited_modes = data.get('visited_modes', [])
        self.unlocked_coll_tiers = data.get('unlocked_coll_tiers', [])
        self.crafted_generators = data.get('crafted_generators', [])
        self.fastest_target_practice = data.get('fastest_target_practice', None)
        self.fishing_treasure_caught = data.get('fishing_treasure_caught', 0)
        self.experience = self._parse_experience(data.get('experience', {}))

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None
    
    def _parse_perks(self, perks_dict):
        """Convert the perks dictionary into a list of Perk objects."""
        return [Perk(name, level) for name, level in perks_dict.items()]

    def _parse_experience(self, experience_dict):
        """Convert the experience dictionary into a list of SkillExperience objects."""
        return [SkillExperience(skill, xp) for skill, xp in experience_dict.items()]

    def __str__(self):
        last_death_str = self.last_death.strftime('%Y-%m-%d %H:%M:%S') if self.last_death else 'N/A'
        return (f"PlayerData(Deaths: {self.death_count}, Last Death: {last_death_str}, "
                f"Visited Zones: {len(self.visited_zones)}, Experience: {self.experience})")

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
        self.rift = data.get('rift', {})
        self.player_data = PlayerData(data.get('player_data', {}))
        self.glacite_player_data = GlacitePlayerData(data.get('glacite_player_data', {}))
        self.events = Events(data.get('events', {}))
        self.garden_player_data = data.get('garden_player_data', {})
        self.pets_data = data.get('pets_data', {})
        self.accessory_bag_storage = data.get('accessory_bag_storage', {})
        self.leveling = data.get('leveling', {})
        self.item_data = data.get('item_data', {})
        self.jacobs_contest = data.get('jacobs_contest', {})
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


class SkyBlockProfile:
    """
    Represents a SkyBlock profile.

    Attributes:
        profile_id (str): The unique identifier of the profile.
        members (dict): A dictionary mapping member UUIDs to SkyBlockProfileMember objects.
        community_upgrades (CommunityUpgrades or None): The community upgrades associated with the profile.
        banking (Banking or None): The banking information of the profile.
        cute_name (str or None): The cute name of the profile (only provided by the profiles endpoint).
        selected (bool or None): Whether this is the player's selected profile (only provided by the profiles endpoint).
        game_mode (str): The game mode of the profile ('ironman', 'island', 'bingo', or 'Normal').
    """

    def __init__(self, data):
        self.profile_id = data.get('profile_id')
        self.members = {}
        members_data = data.get('members', {})
        for uuid, member_data in members_data.items():
            self.members[uuid] = SkyBlockProfileMember(uuid, member_data)

        self.community_upgrades = None
        if 'community_upgrades' in data:
            self.community_upgrades = CommunityUpgrades(data['community_upgrades'])

        self.banking = None
        if 'banking' in data:
            self.banking = Banking(data['banking'])

        self.cute_name = data.get('cute_name', None)
        self.selected = data.get('selected', None)
        self.game_mode = data.get('game_mode', "Normal")

    def get_member(self, uuid):
        """
        Retrieve a member by UUID.

        Args:
            uuid (str): The UUID of the member.

        Returns:
            SkyBlockProfileMember or None: The member object, or None if not found.
        """
        return self.members.get(uuid)

    def list_member_uuids(self):
        """
        List all member UUIDs in the profile.

        Returns:
            list of str: List of member UUIDs.
        """
        return list(self.members.keys())

    def __str__(self):
        cute_name_str = f", Cute Name: {self.cute_name}" if self.cute_name else ""
        selected_str = ", Selected" if self.selected else ""
        game_mode_str = f", Game Mode: {self.game_mode}" if self.game_mode else ""
        return f"SkyBlockProfile ID: {self.profile_id}{cute_name_str}{selected_str}{game_mode_str}, Members: {self.list_member_uuids()}"


class SkyBlockProfiles:
    """
    Handles fetching and managing SkyBlock profile data from the Hypixel API.

    Attributes:
        api_key (str): The API key required for the requests.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self._profile_endpoint = PROFILE_API_URL
        self._profiles_endpoint = PROFILES_API_URL

    def get_profile(self, profile_id):
        """
        Fetches a single profile by profile ID using the profile endpoint.

        Args:
            profile_id (str): The profile ID to fetch.

        Returns:
            SkyBlockProfile: The SkyBlockProfile object containing profile data.

        Raises:
            ValueError: If no profile data is available in the response.
            PermissionError: If access is forbidden (e.g., invalid API key).
            ConnectionError: If there's an issue with the connection or request.
        """
        try:
            params = {'key': self.api_key, 'profile': profile_id}
            response = requests.get(self._profile_endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('success') and 'profile' in data:
                profile_data = data['profile']
                return SkyBlockProfile(profile_data)
            else:
                raise ValueError("No profile data available in the response")
        except requests.exceptions.HTTPError as e:
            response_status = e.response.status_code
            if response_status == 403:
                raise PermissionError("Access forbidden: Invalid API key.")
            elif response_status == 429:
                raise ConnectionError("Request limit reached: Throttling in effect.")
            else:
                raise ConnectionError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching the profile: {e}")

    def get_profiles_by_player_uuid(self, player_uuid):
        """
        Fetches all profiles associated with a player UUID using the profiles endpoint.

        Args:
            player_uuid (str): The UUID of the player.

        Returns:
            list of SkyBlockProfile: A list of SkyBlockProfile objects.

        Raises:
            ValueError: If no profiles data is available in the response.
            PermissionError: If access is forbidden (e.g., invalid API key).
            ConnectionError: If there's an issue with the connection or request.
        """
        try:
            params = {'key': self.api_key, 'uuid': player_uuid}
            response = requests.get(self._profiles_endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('success') and 'profiles' in data:
                profiles_data = data['profiles']
                profiles = [SkyBlockProfile(profile_data) for profile_data in profiles_data]
                return profiles
            else:
                raise ValueError("No profiles data available in the response")
        except requests.exceptions.HTTPError as e:
            response_status = e.response.status_code
            if response_status == 403:
                raise PermissionError("Access forbidden: Invalid API key.")
            elif response_status == 429:
                raise ConnectionError("Request limit reached: Throttling in effect.")
            else:
                raise ConnectionError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching the profiles: {e}")

    def get_selected_profile_by_player_uuid(self, player_uuid):
        """
        Fetches the selected profile for a player UUID.

        Args:
            player_uuid (str): The UUID of the player.

        Returns:
            SkyBlockProfile or None: The selected SkyBlockProfile object, or None if not found.

        Raises:
            Exception: If there's an issue fetching profiles.
        """
        profiles = self.get_profiles_by_player_uuid(player_uuid)
        for profile in profiles:
            if profile.selected:
                return profile
        return None
