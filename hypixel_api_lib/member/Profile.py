from datetime import datetime
from hypixel_api_lib.utils import convert_timestamp

class Profile:
    """
    Profile component of the SkyBlockProfileMember component within the Profiles Data.

    Attributes:
        first_join (datetime): Datetime of when the member first joined the profile (Defaults)
        personal_bank_upgrade (int): Current upgrade level of the personal bank (Defaults 0)
        cookie_buff_active (bool): Whether there is an active cookie buff or not (Defaults False)
    """
    
    def __init__(self, data: dict) -> None:
        self.first_join: datetime = convert_timestamp(data.get("first_join", 0))
        self.personal_bank_upgrade: int = data.get("personal_bank_upgrade", 0)
        self.cookie_buff_active: bool = data.get("cookie_buff_active", False)
        self.deletion_notice: dict | None = data.get("deletion_notice", None)

    def __repr__(self) -> str:
        return f"SkyblockProfileMember Profile Details: First Joined: {self.first_join}, Personal Bank Upgrade: {self.personal_bank_upgrade}, Active Cookie Buff: {self.cookie_buff_active}"
