from datetime import datetime, timezone
import requests

MOJANG_API_URL = r"https://api.mojang.com/users/profiles/minecraft/"

def convert_timestamp(timestamp: int | None) -> datetime | None:
    """Convert a timestamp in milliseconds to a timezone-aware datetime object in UTC."""
    if timestamp:
        return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    return None

def get_uuid_from_username(username: str) -> str:
        """
        Fetch the UUID of a player from their username using the Mojang API.

        Args:
            username (str): The username of the player.

        Returns:
            str: The UUID of the player without dashes.

        Raises:
            ValueError: If the username does not exist.
            ConnectionError: If there's an error contacting the Mojang API.
        """
        try:
            response = requests.get("https://api.mojang.com/users/profiles/minecraft/" + username)
            if response.status_code == 204:
                raise ValueError(f"Username '{username}' does not exist.")
            response.raise_for_status()
            data = response.json()
            uuid = data.get('id')
            if uuid:
                return uuid
            else:
                raise ValueError(f"UUID not found for username '{username}'.")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"HTTP Error while fetching UUID for username '{username}': {e}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"An error occurred while fetching UUID for username '{username}': {e}")

def get_username_from_uuid(uuid: str) -> str:
    """
    Fetch the username of a player from their UUID using the Mojang API.

    Args:
        uuid (str): The UUID of the player without dashes.

    Returns:
        str: The username of the player.

    Raises:
        ValueError: If the UUID does not exist or has no associated username.
        ConnectionError: If there's an error contacting the Mojang API.
    """
    try:
        response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        if response.status_code == 204:
            raise ValueError(f"UUID '{uuid}' does not exist.")
        response.raise_for_status()
        data = response.json()
        username = data.get('name')
        if username:
            return username
        else:
            raise ValueError(f"Username not found for UUID '{uuid}'.")
    except requests.exceptions.HTTPError as e:
        raise ConnectionError(f"HTTP Error while fetching username for UUID '{uuid}': {e}")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"An error occurred while fetching username for UUID '{uuid}': {e}")
