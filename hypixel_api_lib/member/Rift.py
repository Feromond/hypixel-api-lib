import zlib
import base64
import gzip
from io import BytesIO

class InventoryData:
    """
    Represents inventory-related data, handling Minecraft-specific encoding and compression formats.

    Attributes:
        type (int): Type identifier of the inventory data.
        raw_data (str): Raw compressed data of the inventory.
        data (str): Decoded or decompressed data, or an error message if decoding fails.
    """

    def __init__(self, data):
        self.type = data.get('type')
        self.raw_data = data.get('data', '')

        self.data = self._decode_data(self.raw_data)

    def _decode_data(self, data):
        """Attempt to decode and decompress the inventory data."""
        if not data:
            return "No data available"
        
        try:
            decoded_data = base64.b64decode(data)
            
            try:
                decompressed_data = zlib.decompress(decoded_data)
                return decompressed_data.decode('utf-8', errors='ignore')
            except zlib.error as e:
                try:
                    with gzip.open(BytesIO(decoded_data), 'rb') as f:
                        return f.read().decode('utf-8', errors='ignore')
                except gzip.BadGzipFile as e:
                    return f"Error decoding inventory: Gzip decompression failed - {e}"

        except (base64.binascii.Error, zlib.error) as e:
            return f"Error decoding inventory: {e}"

    def __str__(self):
        data_preview = self.data[:500] + "..." if len(self.data) > 500 else self.data
        return f"InventoryData(Type: {self.type}, Data Preview: {data_preview})"



class VillagePlaza:
    def __init__(self, data):
        self.murder = data.get('murder', {})
        self.barry_center = data.get('barry_center', {})
        self.cowboy = data.get('cowboy', {})
        self.barter_bank = data.get('barter_bank', {})
        self.lonely = data.get('lonely', {})
        self.seraphine = data.get('seraphine', {})

    def __str__(self):
        return f"VillagePlaza(Murder: {self.murder}, Barry Center: {self.barry_center}, Cowboy: {self.cowboy}, Barter Bank: {self.barter_bank}, Lonely: {self.lonely}, Seraphine: {self.seraphine})"


class WitherCage:
    def __init__(self, data):
        self.killed_eyes = data.get('killed_eyes', [])

    def __str__(self):
        return f"WitherCage(Killed Eyes: {self.killed_eyes})"


class BlackLagoon:
    def __init__(self, data):
        self.talked_to_edwin = data.get('talked_to_edwin', False)
        self.received_science_paper = data.get('received_science_paper', False)
        self.completed_step = data.get('completed_step', 0)
        self.delivered_science_paper = data.get('delivered_science_paper', False)

    def __str__(self):
        return f"BlackLagoon(Talked to Edwin: {self.talked_to_edwin}, Received Science Paper: {self.received_science_paper}, Completed Step: {self.completed_step}, Delivered Science Paper: {self.delivered_science_paper})"


class DeadCats:
    def __init__(self, data):
        self.talked_to_jacquelle = data.get('talked_to_jacquelle', False)
        self.picked_up_detector = data.get('picked_up_detector', False)
        self.found_cats = data.get('found_cats', [])
        self.unlocked_pet = data.get('unlocked_pet', False)
        self.montezuma = data.get('montezuma', {})

    def __str__(self):
        return f"DeadCats(Talked to Jacquelle: {self.talked_to_jacquelle}, Picked Up Detector: {self.picked_up_detector}, Found Cats: {self.found_cats}, Unlocked Pet: {self.unlocked_pet}, Montezuma: {self.montezuma})"


class WizardTower:
    def __init__(self, data):
        self.wizard_quest_step = data.get('wizard_quest_step', 0)
        self.crumbs_laid_out = data.get('crumbs_laid_out', 0)

    def __str__(self):
        return f"WizardTower(Wizard Quest Step: {self.wizard_quest_step}, Crumbs Laid Out: {self.crumbs_laid_out})"


class Enigma:
    def __init__(self, data):
        self.bought_cloak = data.get('bought_cloak', False)
        self.found_souls = data.get('found_souls', [])
        self.claimed_bonus_index = data.get('claimed_bonus_index', 0)

    def __str__(self):
        return f"Enigma(Bought Cloak: {self.bought_cloak}, Found Souls: {self.found_souls}, Claimed Bonus Index: {self.claimed_bonus_index})"


class Gallery:
    def __init__(self, data):
        self.elise_step = data.get('elise_step', 0)
        self.secured_trophies = data.get('secured_trophies', [])
        self.sent_trophy_dialogues = data.get('sent_trophy_dialogues', [])

    def __str__(self):
        return f"Gallery(Elise Step: {self.elise_step}, Secured Trophies: {self.secured_trophies}, Sent Trophy Dialogues: {self.sent_trophy_dialogues})"


class WestVillage:
    def __init__(self, data):
        self.crazy_kloon = data.get('crazy_kloon', {})
        self.mirrorverse = data.get('mirrorverse', {})
        self.kat_house = data.get('kat_house', {})
        self.glyphs = data.get('glyphs', {})

    def __str__(self):
        return f"WestVillage(Crazy Kloon: {self.crazy_kloon}, Mirrorverse: {self.mirrorverse}, Kat House: {self.kat_house}, Glyphs: {self.glyphs})"


class WyldWoods:
    def __init__(self, data):
        self.talked_threebrothers = data.get('talked_threebrothers', [])
        self.sirius_started_q_a = data.get('sirius_started_q_a', False)
        self.bughunter_step = data.get('bughunter_step', 0)
        self.sirius_q_a_chain_done = data.get('sirius_q_a_chain_done', False)
        self.sirius_claimed_doubloon = data.get('sirius_claimed_doubloon', False)

    def __str__(self):
        return f"WyldWoods(Talked to Three Brothers: {self.talked_threebrothers}, Sirius Started Q&A: {self.sirius_started_q_a}, Bug Hunter Step: {self.bughunter_step}, Sirius Q&A Chain Done: {self.sirius_q_a_chain_done}, Sirius Claimed Doubloon: {self.sirius_claimed_doubloon})"


class RiftData:
    """
    Represents all Rift-related data for a SkyBlock profile member.

    Attributes:
        village_plaza (VillagePlaza): Village Plaza data.
        wither_cage (WitherCage): Wither Cage data.
        black_lagoon (BlackLagoon): Black Lagoon data.
        dead_cats (DeadCats): Dead Cats data.
        wizard_tower (WizardTower): Wizard Tower data.
        enigma (Enigma): Enigma data.
        gallery (Gallery): Gallery data.
        west_village (WestVillage): West Village data.
        wyld_woods (WyldWoods): Wyld Woods data.
        lifetime_purchased_boundaries (list): List of purchased boundaries.
        access (dict): Access data.
        dreadfarm (dict): Dreadfarm data.
        inventory (InventoryData): Inventory data.
        ender_chest_contents (InventoryData): Ender Chest data.
        ender_chest_page_icons (list): Ender Chest page icons.
        equipment_contents (InventoryData): Equipment contents.
    """

    def __init__(self, data):
        self.village_plaza = VillagePlaza(data.get('village_plaza', {}))
        self.wither_cage = WitherCage(data.get('wither_cage', {}))
        self.black_lagoon = BlackLagoon(data.get('black_lagoon', {}))
        self.dead_cats = DeadCats(data.get('dead_cats', {}))
        self.wizard_tower = WizardTower(data.get('wizard_tower', {}))
        self.enigma = Enigma(data.get('enigma', {}))
        self.gallery = Gallery(data.get('gallery', {}))
        self.west_village = WestVillage(data.get('west_village', {}))
        self.wyld_woods = WyldWoods(data.get('wyld_woods', {}))
        self.lifetime_purchased_boundaries = data.get('lifetime_purchased_boundaries', [])
        self.access = data.get('access', {})
        self.dreadfarm = data.get('dreadfarm', {})

        self.inventory = InventoryData(data.get('inventory', {}).get('inv_contents', {}))
        self.ender_chest_contents = InventoryData(data.get('ender_chest_contents', {}))
        self.ender_chest_page_icons = data.get('ender_chest_page_icons', [])
        self.equipment_contents = InventoryData(data.get('equipment_contents', {}))

    def __str__(self):
        return (
            f"RiftData(\n"
            f"  Village Plaza: {self.village_plaza},\n"
            f"  Wither Cage: {self.wither_cage},\n"
            f"  Black Lagoon: {self.black_lagoon},\n"
            f"  Dead Cats: {self.dead_cats},\n"
            f"  Wizard Tower: {self.wizard_tower},\n"
            f"  Enigma: {self.enigma},\n"
            f"  Gallery: {self.gallery},\n"
            f"  West Village: {self.west_village},\n"
            f"  Wyld Woods: {self.wyld_woods},\n"
            f"  Lifetime Purchased Boundaries: {self.lifetime_purchased_boundaries},\n"
            f"  Access: {self.access},\n"
            f"  Dreadfarm: {self.dreadfarm},\n"
            f"  Inventory: {self.inventory},\n"
            f"  Ender Chest: {self.ender_chest_contents},\n"
            f"  Ender Chest Page Icons: {self.ender_chest_page_icons},\n"
            f"  Equipment Contents: {self.equipment_contents}\n"
            f")"
        )
