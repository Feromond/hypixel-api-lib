from hypixel_api_lib import RecentlyEndedAuctions

recent_auctions = RecentlyEndedAuctions()

# Print the total number of recently ended auctions
print(f"Total recently ended auctions: {len(recent_auctions.auctions)}")

# Get a specific auction by its ID
auction_id = "015fe0c67e6041e69797bbe0c2725a21"
auction = recent_auctions.get_auction_by_id(auction_id)
if auction:
    print(auction)
else:
    print(f"Auction with ID {auction_id} not found.")

# Search for auctions sold by a specific seller
seller_uuid = "fc76242bf64a4698ae0ebc136d900929"
seller_auctions = recent_auctions.search_auctions(seller=seller_uuid)
print(f"Auctions sold by seller {seller_uuid}:")
for auction in seller_auctions:
    print(auction)

# Search for BIN auctions above a certain price
high_value_bins = recent_auctions.search_auctions(bin_only=True, min_price=1000000)
print("High-value BIN auctions:")
for auction in high_value_bins:
    print(auction)
