from hypixel_api_lib.Active_Auctions import Auctions

# Initialize the Auctions manager
auctions_manager = Auctions()

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
