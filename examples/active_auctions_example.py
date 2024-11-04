from hypixel_api_lib.ActiveAuctions import ActiveAuctions

# Initialize the Auctions manager
auctions_manager = ActiveAuctions()

# Fetch the first page of auctions
first_page = auctions_manager.get_page(0)
print(first_page)
print(first_page.auctions[0].item_name)
print(first_page.auctions[0].starting_bid)
print(first_page.auctions[0].highest_bid_amount)



matching_auctions = auctions_manager.search_auctions(
    item_name="Aspect of the Dragons",
    min_price=1_000_000,
    sort_by_price=True,
    descending=True
)

# Print the matching auctions
for auction in matching_auctions:
    print(auction)


# If you prefer to preload all data for faster local speed on a given snapshot:
auctions_manager_preloaded = ActiveAuctions(preload_all=True)

# Now searches will use the preloaded data
matching_auctions = auctions_manager_preloaded.search_auctions(
    item_name="Aspect of the Dragons",
    min_price=1_000_000,
    sort_by_price=True,
    descending=True
)
