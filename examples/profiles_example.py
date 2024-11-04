from hypixel_api_lib.Profiles import SkyBlockProfiles
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HYPIXEL_API_KEY")
profile_id = "ce2c4e5646b44616956a055bdc1635f8"

profile_api = SkyBlockProfiles(api_key)

try:
    profile = profile_api.get_profile(profile_id)
    print(profile)

    print(profile.community_upgrades)

    for member_uuid, member in profile.members.items():
        print(member)
        print(f"  Player Data: {member.player_data}")
        print(f"  Inventory: {member.inventory}")
        print(f"  Collection: {member.collection}")
        print(f"  Slayer: {member.slayer}")
        print(f"  Dungeons: {member.dungeons}")
except Exception as e:
    print(f"Error: {e}")
