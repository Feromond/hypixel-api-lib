import requests
from datetime import datetime
from .member.ProfileMember import SkyBlockProfileMember
from hypixel_api_lib.utils import convert_timestamp, get_uuid_from_username

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

    def __init__(self, data: dict) -> None:
        self.upgrade: str = data.get('upgrade')
        self.tier: int = data.get('tier')
        self.started_ms: datetime | None = convert_timestamp(data.get('started_ms'))
        self.started_by: str = data.get('started_by')
        self.claimed_ms: datetime | None = convert_timestamp(data.get('claimed_ms'))
        self.claimed_by: str = data.get('claimed_by')
        self.fasttracked: bool = data.get('fasttracked', False)

    def __str__(self) -> str:
        return f"Upgrade: {self.upgrade}, Tier: {self.tier}, Fasttracked: {self.fasttracked}"


class CommunityUpgrades:
    """
    Represents the community upgrades of a SkyBlock profile.

    Attributes:
        currently_upgrading (CommunityUpgradeState or None): The current upgrade in progress.
        upgrade_states (list of CommunityUpgradeState): A list of completed upgrades.
    """

    def __init__(self, data: dict) -> None:
        currently_upgrading_data: dict = data.get('currently_upgrading')
        self.currently_upgrading: CommunityUpgradeState | None = (
            CommunityUpgradeState(currently_upgrading_data) if currently_upgrading_data else None
        )
        self.upgrade_states: list[CommunityUpgradeState] = [
            CommunityUpgradeState(upgrade_data) for upgrade_data in data.get('upgrade_states', [])
        ]

    def __str__(self) -> str:
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

    def __init__(self, data: dict) -> None:
        self.timestamp: datetime | None = convert_timestamp(data.get('timestamp'))
        self.action: str = data.get('action')
        self.initiator_name: str = data.get('initiator_name')
        self.amount: float = data.get('amount')

    def __str__(self) -> str:
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else 'N/A'
        return f"{self.action} of {self.amount} by {self.initiator_name} at {timestamp_str}"


class Banking:
    """
    Represents the banking information of a SkyBlock profile.

    Attributes:
        balance (float): The current balance of the bank.
        transactions (list of BankTransaction): A list of bank transactions.
    """

    def __init__(self, data: dict) -> None:
        self.balance: float = data.get('balance', 0.0)
        self.transactions: list[BankTransaction] = [BankTransaction(txn) for txn in data.get('transactions', [])]

    def __str__(self) -> str:
        return f"Banking Balance: {self.balance}, Transactions: {len(self.transactions)}"


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

    def __init__(self, data: dict) -> None:
        self.profile_id: str = data.get('profile_id')
        self.members: dict[str,SkyBlockProfileMember] = {}
        members_data: dict = data.get('members', {})
        for uuid, member_data in members_data.items():
            self.members[uuid] = SkyBlockProfileMember(uuid, member_data)

        self.community_upgrades: CommunityUpgrades | None = None
        if 'community_upgrades' in data:
            self.community_upgrades = CommunityUpgrades(data['community_upgrades'])

        self.banking: Banking | None = None
        if 'banking' in data:
            self.banking = Banking(data['banking'])

        self.cute_name: str | None = data.get('cute_name', None)
        self.selected: bool | None = data.get('selected', None)
        self.game_mode: str = data.get('game_mode', "Normal")

    def get_member(self, uuid: str) -> SkyBlockProfileMember | None:
        """
        Retrieve a member by UUID.

        Args:
            uuid (str): The UUID of the member.

        Returns:
            SkyBlockProfileMember or None: The member object, or None if not found.
        """
        return self.members.get(uuid)

    def list_member_uuids(self) -> list[str]:
        """
        List all member UUIDs in the profile.

        Returns:
            list of str: List of member UUIDs.
        """
        return list(self.members.keys())

    def __str__(self) -> str:
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

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        self._profile_endpoint: str = PROFILE_API_URL
        self._profiles_endpoint: str = PROFILES_API_URL

    def get_profile(self, profile_id: str) -> SkyBlockProfile:
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

            if data.get('success') and data.get('profile') is not None:
                profile_data = data['profile']
                return SkyBlockProfile(profile_data)
            else:
                raise ValueError("No profile data available in the response")
        except requests.exceptions.HTTPError as e:
            response_status = None
            if e.response is not None:
                response_status = e.response.status_code
            if response_status == 403:
                raise PermissionError("Access forbidden: Invalid API key.")
            elif response_status == 429:
                raise ConnectionError("Request limit reached: Throttling in effect.")
            else:
                raise ConnectionError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching the profile: {e}")

    def get_profiles_by_player_uuid(self, player_uuid: str) -> list[SkyBlockProfile]:
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

    def get_selected_profile_by_player_uuid(self, player_uuid: str) -> SkyBlockProfile | None:
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

    def get_profiles_by_player_name(self, username: str) -> list[SkyBlockProfile]:
        """
        Fetch profiles by player's username.

        Args:
            username (str): The username of the player.

        Returns:
            list[SkyBlockProfile]: List of profiles that the player is part of.

        Raises:
            ValueError: If the username does not exist or the API response indicates an error.
            ConnectionError: If there's a network-related error.
        """
        try:
            player_uuid = get_uuid_from_username(username)
            return self.get_profiles_by_player_uuid(player_uuid)
        except ValueError as ve:
            raise ve
        except ConnectionError as ce:
            raise ce
        
    def get_selected_profile_by_player_name(self, username: str) -> SkyBlockProfile | None:
        """
        Fetch currently selected profile by player's username.

        Args:
            username (str): The username of the player.

        Returns:
            SkyBlockProfile | None: Currently selected profile of the player if it exists, or None

        Raises:
            ValueError: If the username does not exist or the API response indicates an error.
            ConnectionError: If there's a network-related error.
        """
        try:
            player_uuid = get_uuid_from_username(username)
            return self.get_selected_profile_by_player_uuid(player_uuid)
        except ValueError as ve:
            raise ve
        except ConnectionError as ce:
            raise ce