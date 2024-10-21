from datetime import timezone, timedelta
from hypixel_api_lib.Bingo import BingoEvents
from zoneinfo import ZoneInfo

def main():
    try:
        bingo_events = BingoEvents()
    except ConnectionError as e:
        print(f"Failed to load bingo events: {e}")
        return

    current_event = bingo_events.get_current_event()

    print(f"Bingo Event: {current_event.name} (ID: {current_event.id})")
    print(f"Modifier: {current_event.modifier}")

    print(f"Start Time (UTC): {current_event.start.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"End Time (UTC): {current_event.end.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Convert times to Mountain Standard Time (MST)
    # mst = timezone(timedelta(hours=-6))
    mst = ZoneInfo("America/Edmonton") # Handles differences due to daylight savings issues
    start_time_mst = current_event.get_start_time_in_timezone(mst)
    end_time_mst = current_event.get_end_time_in_timezone(mst)
    print(f"Start Time (MST): {start_time_mst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"End Time (MST): {end_time_mst.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # List all goals
    print("\nGoals:")
    for goal in current_event.goals:
        print(f"- {goal.name} (ID: {goal.id})")
        print(f"  Lore: {goal.get_clean_lore()}")
        completion = goal.get_completion_percentage()
        if completion is not None:
            print(f"  Completion: {completion:.2f}%")
        else:
            print("  Completion: N/A")
        print()

    # Get a specific goal by ID
    goal_id = "kill_endermen"
    goal = current_event.get_goal_by_id(goal_id)
    if goal:
        print(f"Details for Goal ID '{goal_id}':")
        print(f"Name: {goal.name}")
        print(f"Lore: {goal.get_clean_lore()}")
        print(f"Progress: {goal.progress}")
        print(f"Required Amount: {goal.required_amount}")
        print(f"Tiers: {goal.tiers}")
        completion = goal.get_completion_percentage()
        if completion is not None:
            print(f"Completion Percentage: {completion:.2f}%")
        else:
            print("Completion Percentage: N/A")
    else:
        print(f"Goal with ID '{goal_id}' not found.")

    # Get a goal by name
    goal_name = "Farmer"
    goal = current_event.get_goal_by_name(goal_name)
    if goal:
        print(f"\nDetails for Goal '{goal_name}':")
        print(f"ID: {goal.id}")
        print(f"Lore: {goal.get_clean_lore()}")
    else:
        print(f"Goal with name '{goal_name}' not found.")

if __name__ == "__main__":
    main()
