from hypixel_api_lib import Bazaar

bazaar = Bazaar()

print(f"Bazaar data last updated on: {bazaar.last_updated}")

search_terms = [
    "ink sack",
    "rejuvinate",
    "wisdom 1",
    "jerry stone",
    "gemstone",
    "mithril ore",
    "dungeon potion",
    "booster cookie",
]

# Find a specific item using general item names
for term in search_terms:
    print(f"\nSearching for: '{term}'")
    product = bazaar.search_product(term)
    if product:
        print(f"Found Product ID: {product.product_id}")
        quick_status = product.quick_status
        print("Quick Status:")
        print(f"  Sell Price: {quick_status.sell_price}")
        print(f"  Buy Price: {quick_status.buy_price}")
    else:
        print("Product not found.")

# Get a specific product by its ID
product_id = "INK_SACK:3"  # Replace with any valid product ID
product = bazaar.get_product_by_id(product_id)

if product:
    print(f"\nDetails for Product ID: {product.product_id}")

    # Access the quick status
    quick_status = product.quick_status
    print("Quick Status:")
    print(f"  Sell Price: {quick_status.sell_price}")
    print(f"  Sell Volume: {quick_status.sell_volume}")
    print(f"  Buy Price: {quick_status.buy_price}")
    print(f"  Buy Volume: {quick_status.buy_volume}")

    # Get the top buy order
    top_buy_order = product.get_top_buy_order()
    if top_buy_order:
        print("\nTop Buy Order:")
        print(f"  Amount: {top_buy_order.amount}")
        print(f"  Price per Unit: {top_buy_order.price_per_unit}")
        print(f"  Orders: {top_buy_order.orders}")
    else:
        print("\nNo buy orders available.")

    # Get the top sell order
    top_sell_order = product.get_top_sell_order()
    if top_sell_order:
        print("\nTop Sell Order:")
        print(f"  Amount: {top_sell_order.amount}")
        print(f"  Price per Unit: {top_sell_order.price_per_unit}")
        print(f"  Orders: {top_sell_order.orders}")
    else:
        print("\nNo sell orders available.")
else:
    print(f"Product with ID '{product_id}' not found.")
