from hypixel_api_lib import PlayerAuctions
from dotenv import load_dotenv
import os

load_dotenv()

player_auctions = PlayerAuctions(os.getenv("HYPIXEL_API_KEY"))

try:
    # Fetch an auction by its UUID
    auction_uuid = '409a1e0f261a49849493278d6cd9305a' # Random Auction UUID
    auction = player_auctions.get_auction_by_uuid(auction_uuid)
    print(auction)

    # Fetch auctions by player UUID
    player_uuid = 'be5c42d4ea454601a57b944c6413f3cd' # Feromond
    auctions = player_auctions.get_auctions_by_player_uuid(player_uuid)
    for auction in auctions:
        print(auction)

    username = 'Feromond'
    auctions = player_auctions.get_auctions_by_username(username)
    for auction in auctions:
        print(auction)

    # Fetch auctions by profile UUID
    profile_uuid = 'ce2c4e5646b44616956a055bdc1635f8' # Feromond Main CO-OP Profile UUID
    auctions = player_auctions.get_auctions_by_profile_uuid(profile_uuid)
    for auction in auctions:
        print(auction)
except ValueError as ve:
    print(f"ValueError: {ve}")
except PermissionError as pe:
    print(f"PermissionError: {pe}")
except ConnectionError as ce:
    print(f"ConnectionError: {ce}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
