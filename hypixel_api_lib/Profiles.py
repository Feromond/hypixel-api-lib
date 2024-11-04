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
        started_ms (int): The timestamp when the upgrade started.
        started_by (str): The UUID of the player who started the upgrade.
        claimed_ms (int): The timestamp when the upgrade was claimed.
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

    def _convert_timestamp(self, timestamp):
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

class SkyBlockProfileMember:
    """
    Represents a member of a SkyBlock profile.

    Attributes:
        uuid (str): The UUID of the member.
        All member data fields.
    """
    def __init__(self, uuid, data):
        self.uuid = uuid
        self.rift = data.get('rift', {})
        self.player_data = data.get('player_data', {})
        self.glacite_player_data = data.get('glacite_player_data', {})
        self.events = data.get('events', {})
        self.garden_player_data = data.get('garden_player_data', {})
        self.pets_data = data.get('pets_data', {})
        self.accessory_bag_storage = data.get('accessory_bag_storage', {})
        self.leveling = data.get('leveling', {})
        self.item_data = data.get('item_data', {})
        self.jacobs_contest = data.get('jacobs_contest', {})
        self.currencies = data.get('currencies', {})
        self.dungeons = data.get('dungeons', {})
        self.profile = data.get('profile', {})
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

    def __str__(self):
        return f"SkyBlockProfileMember UUID: {self.uuid}"

class SkyBlockProfile:
    """
    Represents a SkyBlock profile. (Currently just with the profile endpoint and not profiles...)

    Attributes:
        profile_id (str): The unique identifier of the profile.
        community_upgrades (CommunityUpgrades): The community upgrades associated with the profile.
        members (dict): A dictionary of members in the profile.
    """
    def __init__(self, data):
        self.profile_id = data.get('profile_id')
        community_upgrades_data = data.get('community_upgrades', {})
        self.community_upgrades = CommunityUpgrades(community_upgrades_data)
        self.members = {}
        members_data = data.get('members', {})
        for uuid, member_data in members_data.items():
            self.members[uuid] = SkyBlockProfileMember(uuid, member_data)

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
        return f"SkyBlockProfile ID: {self.profile_id}, Members: {self.list_member_uuids()}"

class SkyBlockProfiles:
    """
    Handles fetching and managing SkyBlock profile data from the API.

    Attributes:
        api_key (str): The API key required for the request.
        api_endpoint (str): The endpoint URL to fetch the profile data.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self._profile_endpoint = PROFILE_API_URL
        self._profiles_endpoint = PROFILES_API_URL

    def get_profile(self, profile_id):
        """
        Fetches a single profile by profile ID.

        Args:
            profile_id (str): The profile ID to fetch.

        Returns:
            SkyBlockProfile: The SkyBlockProfile object containing profile data.
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
                raise ConnectionError(f"An error occurred while fetching the profile: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching the profile: {e}")

    def get_profiles_by_player_uuid(self, player_uuid):
        """
        Fetches all profiles associated with a player UUID.

        Args:
            player_uuid (str): The UUID of the player.

        Returns:
            list of SkyBlockProfile: A list of SkyBlockProfile objects.
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
                raise ConnectionError(f"An error occurred while fetching the profiles: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching the profiles: {e}")

    def get_selected_profile_by_player_uuid(self, player_uuid):
        """
        Fetches the selected profile for a player UUID.

        Args:
            player_uuid (str): The UUID of the player.

        Returns:
            SkyBlockProfile or None: The selected SkyBlockProfile object, or None if not found.
        """
        profiles = self.get_profiles_by_player_uuid(player_uuid)
        for profile in profiles:
            if hasattr(profile, 'selected') and profile.selected:
                return profile
        return None
