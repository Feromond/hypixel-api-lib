from datetime import datetime, timezone

class EasterTimeTower:
    """
    Represents the time tower data in the Easter event.

    Attributes:
        charges (int): Number of charges left.
        activation_time (datetime): Time when the tower was activated.
        level (int): Level of the time tower.
        last_charge_time (datetime): Time when the last charge was used.
    """

    def __init__(self, data):
        self.charges = data.get('charges', 0)
        self.activation_time = self._convert_timestamp(data.get('activation_time'))
        self.level = data.get('level', 0)
        self.last_charge_time = self._convert_timestamp(data.get('last_charge_time'))

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        activation_time_str = self.activation_time.strftime('%Y-%m-%d %H:%M:%S') if self.activation_time else 'N/A'
        last_charge_time_str = self.last_charge_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_charge_time else 'N/A'
        return (f"EasterTimeTower(Charges: {self.charges}, Level: {self.level}, "
                f"Activation Time: {activation_time_str}, Last Charge Time: {last_charge_time_str})")


class EasterEmployees:
    """
    Represents the employees data in the Easter event.

    Attributes:
        employee_levels (dict of str to int): Mapping of employee names to their levels.
    """

    def __init__(self, data):
        self.employee_levels = data

    def __str__(self):
        return f"EasterEmployees(Employee Levels: {self.employee_levels})"


class EasterShop:
    """
    Represents the shop data in the Easter event.

    Attributes:
        year (int): The in-game year of the event.
        rabbits (list of str): List of rabbits available in the shop.
        rabbits_purchased (list of str): List of rabbits purchased by the player.
        chocolate_spent (int): Total chocolate spent in the shop.
        cocoa_fortune_upgrades (int): Number of cocoa fortune upgrades purchased.
    """

    def __init__(self, data):
        self.year = data.get('year', 0)
        self.rabbits = data.get('rabbits', [])
        self.rabbits_purchased = data.get('rabbits_purchased', [])
        self.chocolate_spent = data.get('chocolate_spent', 0)
        self.cocoa_fortune_upgrades = data.get('cocoa_fortune_upgrades', 0)

    def __str__(self):
        return (f"EasterShop(Year: {self.year}, Rabbits Purchased: {len(self.rabbits_purchased)}, "
                f"Chocolate Spent: {self.chocolate_spent})")


class EasterRabbitsData:
    """
    Represents the rabbits data in the Easter event.

    Attributes:
        collected_eggs (dict of str to int): Number of eggs collected per meal type.
        rabbit_counts (dict of str to int): Counts of each rabbit collected.
    """

    def __init__(self, data):
        self.collected_eggs = data.get('collected_eggs', {})
        self.collected_locations = data.get('collected_locations', {})
        # Exclude 'collected_eggs' and 'collected_locations' from rabbit_counts
        self.rabbit_counts = {k: v for k, v in data.items() if k not in ('collected_eggs', 'collected_locations')}

    def __str__(self):
        return (f"EasterRabbitsData(Collected Eggs: {self.collected_eggs}, "
                f"Rabbit Counts: {len(self.rabbit_counts)} rabbits)")


class EasterEvent:
    """
    Represents the data for the Easter event.

    Attributes:
        chocolate (int): Current chocolate count.
        chocolate_since_prestige (int): Chocolate earned since the last prestige.
        total_chocolate (int): Total chocolate earned.
        rabbits_data (EasterRabbitsData): Data about rabbits.
        shop (EasterShop): Shop-related data.
        employees (EasterEmployees): Employee-related data.
        last_viewed_chocolate_factory (datetime): Timestamp of the last chocolate factory view.
        rabbit_barn_capacity_level (int): Level of the rabbit barn capacity.
        chocolate_level (int): Current chocolate level.
        time_tower (EasterTimeTower): Time tower data.
        rabbit_sort (str): Sorting preference for rabbits.
        rabbit_filter (str): Filter preference for rabbits.
        el_dorado_progress (int): Progress towards El Dorado.
        chocolate_multiplier_upgrades (int): Number of chocolate multiplier upgrades.
        click_upgrades (int): Number of click upgrades.
        rabbit_rarity_upgrades (int): Number of rabbit rarity upgrades.
    """

    def __init__(self, data):
        self.chocolate = data.get('chocolate', 0)
        self.chocolate_since_prestige = data.get('chocolate_since_prestige', 0)
        self.total_chocolate = data.get('total_chocolate', 0)
        self.rabbits_data = EasterRabbitsData(data.get('rabbits', {}))
        self.shop = EasterShop(data.get('shop', {}))
        self.employees = EasterEmployees(data.get('employees', {}))
        self.last_viewed_chocolate_factory = self._convert_timestamp(data.get('last_viewed_chocolate_factory'))
        self.rabbit_barn_capacity_level = data.get('rabbit_barn_capacity_level', 0)
        self.chocolate_level = data.get('chocolate_level', 0)
        self.time_tower = EasterTimeTower(data.get('time_tower', {}))
        self.rabbit_sort = data.get('rabbit_sort', '')
        self.rabbit_filter = data.get('rabbit_filter', '')
        self.el_dorado_progress = data.get('el_dorado_progress', 0)
        self.chocolate_multiplier_upgrades = data.get('chocolate_multiplier_upgrades', 0)
        self.click_upgrades = data.get('click_upgrades', 0)
        self.rabbit_rarity_upgrades = data.get('rabbit_rarity_upgrades', 0)

    @staticmethod
    def _convert_timestamp(timestamp):
        """Convert a timestamp in milliseconds to a datetime object in UTC."""
        if timestamp is not None:
            return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        return None

    def __str__(self):
        return (f"EasterEvent(Chocolate: {self.chocolate}, Total Chocolate: {self.total_chocolate}, "
                f"RabbitsData: {self.rabbits_data}, Shop: {self.shop}, Employees: {self.employees}, "
                f"TimeTower: {self.time_tower})")


class Events:
    """
    Represents the events data for a SkyBlock profile member.

    Attributes:
        easter (EasterEvent): Data related to the Easter event.
        # If there are ever any other events besides easter we can add them here
    """

    def __init__(self, data):
        self.easter = EasterEvent(data.get('easter', {})) if 'easter' in data else None

    def __str__(self):
        return f"Events(Easter: {self.easter})"