from hypixel_api_lib import Collections

collections = Collections()

# Get a category by name
farming_category = collections.get_category_by_name('Farming')
print(farming_category)

# Get an item by name within a category
wheat_collection = farming_category.get_item_by_name('Wheat')
print(wheat_collection)

# Iterate over the tiers of an item
for tier in wheat_collection.tiers:
    print(tier)
