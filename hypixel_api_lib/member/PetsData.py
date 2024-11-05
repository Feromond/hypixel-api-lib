class PetCareData:
    """
    Represents the pet care data for a SkyBlock profile member.

    Attributes:
        coins_spent (float): Total coins spent on pet care.
        pet_types_sacrificed (list of str): List of pet types that have been sacrificed.
    """

    def __init__(self, data):
        self.coins_spent = data.get('coins_spent', 0.0)
        self.pet_types_sacrificed = data.get('pet_types_sacrificed', [])

    def __str__(self):
        return f"PetCareData(Coins Spent: {self.coins_spent}, Pets Sacrificed: {self.pet_types_sacrificed})"


class AutoPetRule:
    """
    Represents an auto-pet rule.

    Attributes:
        uuid (str): The UUID of the rule.
        rule_id (str): The ID of the rule.
        name (str): The name of the rule.
        unique_id (str): A unique identifier for the rule.
        exceptions (list of dict): Exceptions for the rule.
        disabled (bool): Whether the rule is disabled.
        data (dict): Additional data associated with the rule.
    """

    def __init__(self, data):
        self.uuid = data.get('uuid')
        self.rule_id = data.get('id')
        self.name = data.get('name')
        self.unique_id = data.get('uniqueId')
        self.exceptions = data.get('exceptions', [])
        self.disabled = data.get('disabled', False)
        self.data = data.get('data', {})

    def __str__(self):
        return f"AutoPetRule(Name: {self.name}, Disabled: {self.disabled})"

class AutoPetData:
    """
    Represents the auto-pet data for a SkyBlock profile member.

    Attributes:
        rules_limit (int): The limit on the number of rules.
        rules (list of AutoPetRule): A list of auto-pet rules.
        migrated (bool): Whether the auto-pet rules have been migrated.
        migrated_2 (bool): Whether the secondary migration has occurred.
    """

    def __init__(self, data):
        self.rules_limit = data.get('rules_limit', 0)
        self.rules = [AutoPetRule(rule) for rule in data.get('rules', [])]
        self.migrated = data.get('migrated', False)
        self.migrated_2 = data.get('migrated_2', False)

    def __str__(self):
        return f"AutoPetData(Rules Limit: {self.rules_limit}, Rules Count: {len(self.rules)})"

class PetData:
    """
    Represents an individual pet's data.

    Attributes:
        uuid (str): The UUID of the pet.
        unique_id (str): A unique identifier for the pet.
        type (str): The type of the pet.
        experience (float): The experience points of the pet.
        active (bool): Whether the pet is active.
        tier (str): The tier of the pet.
        held_item (str): The item held by the pet.
        candy_used (int): The number of candy items used on the pet.
        skin (str): The skin applied to the pet, if any.
        extra (dict): Additional data for the pet.
    """

    def __init__(self, data):
        self.uuid = data.get('uuid')
        self.unique_id = data.get('uniqueId')
        self.type = data.get('type')
        self.experience = data.get('exp', 0.0)
        self.active = data.get('active', False)
        self.tier = data.get('tier')
        self.held_item = data.get('heldItem')
        self.candy_used = data.get('candyUsed', 0)
        self.skin = data.get('skin')
        self.extra = data.get('extra', {})

    def __str__(self):
        return f"PetData(Type: {self.type}, Tier: {self.tier}, Active: {self.active})"

class PetsData:
    """
    Represents all pets data for a SkyBlock profile member.

    Attributes:
        pet_care (PetCareData): Data on pet care.
        autopet (AutoPetData): Data on auto-pet rules.
        pets (list of PetData): List of all pets.
    """

    def __init__(self, data):
        self.pet_care = PetCareData(data.get('pet_care', {}))
        self.autopet = AutoPetData(data.get('autopet', {}))
        self.pets = [PetData(pet) for pet in data.get('pets', [])]

    def __str__(self):
        return (f"PetsData(Pet Care: {self.pet_care}, AutoPet Rules: {len(self.autopet.rules)}, "
                f"Total Pets: {len(self.pets)})")