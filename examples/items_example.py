from hypixel_api_lib.Items import Items

items = Items()

item = items.get_item("FARM_ARMOR_CHESTPLATE")

print(f"Item Name: {item.name}")
print(f"Item Material: {item.material}")
print(f"Item Tier: {item.tier}")
print(f"Item Category: {item.category}")
print(f"Item Stats: {item.stats}")
print(f"NPC Sell Price: {item.npc_sell_price}")

item_with_skin = items.get_item("MANDRAA")

print(f"\nItem Name: {item_with_skin.name}")
print(f"Item Material: {item_with_skin.material}")
print(f"Item Tier: {item_with_skin.tier}")
print(f"Item Category: {item_with_skin.category}")
print(f"Item Skin: {item_with_skin.skin}")
print(f"Item Durability: {item_with_skin.durability}")
print(f"NPC Sell Price: {item_with_skin.npc_sell_price}")

chestplate_items = items.get_items_by_category("CHESTPLATE")
print(f"Chestplate Items: {list(chestplate_items.keys())}")


all_categories = items.list_item_categories()

print(f"Item Category List: {all_categories}")