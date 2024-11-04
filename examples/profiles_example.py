from hypixel_api_lib.Profiles import SkyBlockProfiles
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HYPIXEL_API_KEY")
player_uuid = "be5c42d4ea454601a57b944c6413f3cd"  # Feromond

profiles_api = SkyBlockProfiles(api_key)

# Fetch all profiles for the player
try:
    profiles = profiles_api.get_profiles_by_player_uuid(player_uuid)
    print(f"Found {len(profiles)} profiles for player UUID {player_uuid}")
    for profile in profiles:
        print(profile)
        # Access members
        for member_uuid in profile.list_member_uuids():
            member = profile.get_member(member_uuid)
            print(member)
            # Access member attributes
            print(f"  Player Stats: {member.player_stats}")
            # Add additional processing as needed
except Exception as e:
    print(f"Error: {e}")

# Fetch the selected profile for the player
try:
    selected_profile = profiles_api.get_selected_profile_by_player_uuid(player_uuid)
    if selected_profile:
        print(f"Selected profile for player UUID {player_uuid}: {selected_profile}")

        # feromond = selected_profile.get_member(player_uuid)
        # print(feromond.events)
    else:
        print(f"No selected profile found for player UUID {player_uuid}")
except Exception as e:
    print(f"Error: {e}")
