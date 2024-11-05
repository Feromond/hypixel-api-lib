from datetime import datetime, timezone

class SlotTuning:
    """
    Represents tuning parameters for a specific accessory bag slot.

    Attributes:
        health (int): The health bonus for the slot.
        defense (int): The defense bonus for the slot.
        walk_speed (int): The walk speed bonus for the slot.
        strength (int): The strength bonus for the slot.
        critical_damage (int): The critical damage bonus for the slot.
        critical_chance (int): The critical chance bonus for the slot.
        attack_speed (int): The attack speed bonus for the slot.
        intelligence (int): The intelligence bonus for the slot.
        purchase_ts (datetime): Timestamp of purchase for the slot (if available).
        refund (bool): Indicates if the slot tuning has been refunded (if applicable).
    """
    def __init__(self, data):
        self.health = data.get('health', 0)
        self.defense = data.get('defense', 0)
        self.walk_speed = data.get('walk_speed', 0)
        self.strength = data.get('strength', 0)
        self.critical_damage = data.get('critical_damage', 0)
        self.critical_chance = data.get('critical_chance', 0)
        self.attack_speed = data.get('attack_speed', 0)
        self.intelligence = data.get('intelligence', 0)
        self.purchase_ts = self._convert_timestamp(data.get('purchase_ts'))
        self.refund = data.get('refund', False)

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        purchase_str = self.purchase_ts.strftime('%Y-%m-%d %H:%M:%S') if self.purchase_ts else 'N/A'
        return (f"SlotTuning(Health: {self.health}, Defense: {self.defense}, Walk Speed: {self.walk_speed}, "
                f"Strength: {self.strength}, Critical Damage: {self.critical_damage}, Critical Chance: {self.critical_chance}, "
                f"Attack Speed: {self.attack_speed}, Intelligence: {self.intelligence}, "
                f"Purchase Timestamp: {purchase_str}, Refund: {self.refund})")

class AccessoryBagStorage:
    """
    Represents the accessory bag storage data for a SkyBlock profile member.

    Attributes:
        tuning (dict): Tuning data for each slot, including health, defense, and other stats.
        selected_power (str): The currently selected accessory power.
        unlocked_powers (list): List of unlocked accessory powers.
        bag_upgrades_purchased (int): Number of bag upgrades purchased.
        highest_magical_power (int): Highest magical power level achieved.
        highest_unlocked_slot (int): The highest slot unlocked in tuning.
    """

    def __init__(self, data):
        self.tuning = self._parse_tuning(data.get('tuning', {}))
        self.selected_power = data.get('selected_power', '')
        self.unlocked_powers = data.get('unlocked_powers', [])
        self.bag_upgrades_purchased = data.get('bag_upgrades_purchased', 0)
        self.highest_magical_power = data.get('highest_magical_power', 0)
        self.highest_unlocked_slot = data.get('tuning', {}).get('highest_unlocked_slot', 0)

    def _parse_tuning(self, tuning_data):
        """Parse tuning data for each slot, creating SlotTuning instances."""
        tuning = {}
        for key, slot_data in tuning_data.items():
            if key.startswith('slot_'):
                slot_index = int(key.split('_')[1])
                tuning[slot_index] = SlotTuning(slot_data)
            elif key.startswith('refund'):
                slot_index = int(key.split('_')[1])
                if slot_index in tuning:
                    tuning[slot_index].refund = True
        return tuning

    def __str__(self):
        tuning_str = ", ".join(f"Slot {index}: {tuning}" for index, tuning in self.tuning.items())
        return (f"AccessoryBagStorage(\n"
                f"  Selected Power: {self.selected_power},\n"
                f"  Unlocked Powers: {self.unlocked_powers},\n"
                f"  Bag Upgrades Purchased: {self.bag_upgrades_purchased},\n"
                f"  Highest Magical Power: {self.highest_magical_power},\n"
                f"  Highest Unlocked Slot: {self.highest_unlocked_slot},\n"
                f"  Tuning: {tuning_str}\n"
                f")")
