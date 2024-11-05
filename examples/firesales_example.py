import pytz 
from hypixel_api_lib import FireSales

fire_sales = FireSales()
all_sales = fire_sales.sales

# Check if there are any active or upcoming sales
if all_sales:
    print("Active or Upcoming Fire Sales:")
    for sale in all_sales:
        print(f"Item ID: {sale.item_id}")
        print(f"Start Time (UTC): {sale.start}")
        print(f"End Time (UTC): {sale.end}")
        print(f"Amount Available: {sale.amount}")
        print(f"Price (Gems): {sale.price}")
        print(f"Is Active: {'Yes' if sale.is_active() else 'No'}")
        print("-" * 40)
else:
    print("No active or upcoming fire sales at the moment.")

# Example: Convert sale start and end times to a specific timezone
tz = pytz.timezone('America/New_York')
for sale in all_sales:
    start_local = sale.start.astimezone(tz) if sale.start else None
    end_local = sale.end.astimezone(tz) if sale.end else None
    print(f"Item ID: {sale.item_id}")
    print(f"Start Time ({tz}): {start_local}")
    print(f"End Time ({tz}): {end_local}")
    print("-" * 40)

# Example: Get a sale by item ID. Note a common usecase but included incase somoene wants to check for a specific potential fire sale item easily
item_id_to_search = 'DYE_LAVA'
specific_sale = fire_sales.get_sale_by_item_id(item_id_to_search)
if specific_sale:
    print(f"Details for Item ID '{item_id_to_search}':")
    print(specific_sale)
else:
    print(f"No fire sale found for Item ID '{item_id_to_search}'.")

# Example: Check if a specific sale is active and time remaining
if specific_sale:
    if specific_sale.is_active():
        time_remaining = specific_sale.time_until_end()
        print(f"The sale for '{specific_sale.item_id}' is active.")
        print(f"Time remaining until sale ends: {time_remaining}")
    else:
        time_until_start = specific_sale.time_until_start()
        print(f"The sale for '{specific_sale.item_id}' is not active yet.")
        print(f"Time remaining until sale starts: {time_until_start}")
