from hypixel_api_lib.Items import Items

# Initialize the Items manager
items_manager = Items()

# Retrieve a specific item by its ID
item = items_manager.get_item("ASPECT_OF_THE_END")

print(f"Item Name: {item.name}")
print(f"Item Material: {item.material}")
print(f"Item Tier: {item.tier}")

# Retrieve items with a specific tier
legendary_items = items_manager.get_items_by_tier("LEGENDARY")
print(f"Legendary Items: {list(legendary_items.keys())}")


