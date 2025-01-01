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

    def __init__(self, data: dict) -> None:
        self.type: int = data.get('type')
        self.raw_data: str = data.get('data', '')

        self.data: str = self._decode_data(self.raw_data)

    def _decode_data(self, data: str) -> str:
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

    def __str__(self) -> str:
        data_preview = self.data[:500] + "..." if len(self.data) > 500 else self.data
        return f"InventoryData(Type: {self.type}, Data Preview: {data_preview})"


class VillagePlaza:
    def __init__(self, data: dict) -> None:
        self.murder: dict = data.get('murder', {})
        self.barry_center: dict = data.get('barry_center', {})
        self.cowboy: dict = data.get('cowboy', {})
        self.barter_bank: dict = data.get('barter_bank', {})
        self.lonely: dict = data.get('lonely', {})
        self.seraphine: dict = data.get('seraphine', {})

    def __str__(self) -> str:
        return f"VillagePlaza(Murder: {self.murder}, Barry Center: {self.barry_center}, Cowboy: {self.cowboy}, Barter Bank: {self.barter_bank}, Lonely: {self.lonely}, Seraphine: {self.seraphine})"


class WitherCage:
    def __init__(self, data: dict) -> None:
        self.killed_eyes: list = data.get('killed_eyes', [])

    def __str__(self) -> str:
        return f"WitherCage(Killed Eyes: {self.killed_eyes})"


class BlackLagoon:
    def __init__(self, data: dict) -> None:
        self.talked_to_edwin: bool = data.get('talked_to_edwin', False)
        self.received_science_paper: bool = data.get('received_science_paper', False)
        self.completed_step: int = data.get('completed_step', 0)
        self.delivered_science_paper: bool = data.get('delivered_science_paper', False)

    def __str__(self) -> str:
        return f"BlackLagoon(Talked to Edwin: {self.talked_to_edwin}, Received Science Paper: {self.received_science_paper}, Completed Step: {self.completed_step}, Delivered Science Paper: {self.delivered_science_paper})"


class DeadCats:
    def __init__(self, data: dict) -> None:
        self.talked_to_jacquelle: bool = data.get('talked_to_jacquelle', False)
        self.picked_up_detector: bool = data.get('picked_up_detector', False)
        self.found_cats: list = data.get('found_cats', [])
        self.unlocked_pet: bool = data.get('unlocked_pet', False)
        self.montezuma: dict = data.get('montezuma', {})

    def __str__(self) -> str:
        return f"DeadCats(Talked to Jacquelle: {self.talked_to_jacquelle}, Picked Up Detector: {self.picked_up_detector}, Found Cats: {self.found_cats}, Unlocked Pet: {self.unlocked_pet}, Montezuma: {self.montezuma})"


class WizardTower:
    def __init__(self, data: dict) -> None:
        self.wizard_quest_step: int = data.get('wizard_quest_step', 0)
        self.crumbs_laid_out: int = data.get('crumbs_laid_out', 0)

    def __str__(self) -> str:
        return f"WizardTower(Wizard Quest Step: {self.wizard_quest_step}, Crumbs Laid Out: {self.crumbs_laid_out})"


class Enigma:
    def __init__(self, data: dict) -> None:
        self.bought_cloak: bool = data.get('bought_cloak', False)
        self.found_souls: list = data.get('found_souls', [])
        self.claimed_bonus_index: int = data.get('claimed_bonus_index', 0)

    def __str__(self) -> None:
        return f"Enigma(Bought Cloak: {self.bought_cloak}, Found Souls: {self.found_souls}, Claimed Bonus Index: {self.claimed_bonus_index})"


class Gallery:
    def __init__(self, data: dict) -> None:
        self.elise_step: int = data.get('elise_step', 0)
        self.secured_trophies: list = data.get('secured_trophies', [])
        self.sent_trophy_dialogues: list = data.get('sent_trophy_dialogues', [])

    def __str__(self) -> str:
        return f"Gallery(Elise Step: {self.elise_step}, Secured Trophies: {self.secured_trophies}, Sent Trophy Dialogues: {self.sent_trophy_dialogues})"


class WestVillage:
    def __init__(self, data: dict) -> None:
        self.crazy_kloon: dict = data.get('crazy_kloon', {})
        self.mirrorverse: dict = data.get('mirrorverse', {})
        self.kat_house: dict = data.get('kat_house', {})
        self.glyphs: dict = data.get('glyphs', {})

    def __str__(self) -> str:
        return f"WestVillage(Crazy Kloon: {self.crazy_kloon}, Mirrorverse: {self.mirrorverse}, Kat House: {self.kat_house}, Glyphs: {self.glyphs})"


class WyldWoods:
    def __init__(self, data: dict) -> None:
        self.talked_threebrothers: list = data.get('talked_threebrothers', [])
        self.sirius_started_q_a: bool = data.get('sirius_started_q_a', False)
        self.bughunter_step: int = data.get('bughunter_step', 0)
        self.sirius_q_a_chain_done: bool = data.get('sirius_q_a_chain_done', False)
        self.sirius_claimed_doubloon: bool = data.get('sirius_claimed_doubloon', False)

    def __str__(self) -> str:
        return f"WyldWoods(Talked to Three Brothers: {self.talked_threebrothers}, Sirius Started Q&A: {self.sirius_started_q_a}, Bug Hunter Step: {self.bughunter_step}, Sirius Q&A Chain Done: {self.sirius_q_a_chain_done}, Sirius Claimed Doubloon: {self.sirius_claimed_doubloon})"

class Castle:
    # TODO: Verify there are no more hidden possible fields in the castle data. This is a new addition from a recent update to the rift
    def __init__(self, data:dict) -> None:
        self.unlocked_pathway_skip: bool = data.get("unlocked_pathway_skip", False)
        self.fairy_step: int = data.get("fairy_step", 0)
        self.grubber_stacks: int = data.get("grubber_stacks", 0)
    
    def __str__(self) -> str:
        return f"Castle(Unlocked Pathway Skip: {self.unlocked_pathway_skip}, Fairy Steps: {self.fairy_step}, Grubber Stacks: {self.grubber_stacks})"


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
        castle (Castle): Data related to the castle
        access (dict): Access data.
        dreadfarm (dict): Dreadfarm data.
        inventory (InventoryData): Inventory data.
        ender_chest_contents (InventoryData): Ender Chest data.
        ender_chest_page_icons (list): Ender Chest page icons.
        equipment_contents (InventoryData): Equipment contents.
    """

    def __init__(self, data: dict) -> None:
        self.village_plaza: VillagePlaza = VillagePlaza(data.get('village_plaza', {}))
        self.wither_cage: WitherCage = WitherCage(data.get('wither_cage', {}))
        self.black_lagoon: BlackLagoon = BlackLagoon(data.get('black_lagoon', {}))
        self.dead_cats: DeadCats = DeadCats(data.get('dead_cats', {}))
        self.wizard_tower: WizardTower = WizardTower(data.get('wizard_tower', {}))
        self.enigma: Enigma = Enigma(data.get('enigma', {}))
        self.gallery: Gallery = Gallery(data.get('gallery', {}))
        self.west_village: WestVillage = WestVillage(data.get('west_village', {}))
        self.wyld_woods: WyldWoods = WyldWoods(data.get('wyld_woods', {}))
        self.lifetime_purchased_boundaries: list = data.get('lifetime_purchased_boundaries', [])
        self.castle: Castle = Castle(data.get("castle", {}))
        self.access: dict = data.get('access', {})
        self.dreadfarm: dict = data.get('dreadfarm', {})

        self.inventory: InventoryData = InventoryData(data.get('inventory', {}).get('inv_contents', {}))
        self.ender_chest_contents: InventoryData = InventoryData(data.get('ender_chest_contents', {}))
        self.ender_chest_page_icons: list = data.get('ender_chest_page_icons', [])
        self.equipment_contents: InventoryData = InventoryData(data.get('equipment_contents', {}))

    def __str__(self) -> str:
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
            f"  Castle: {self.castle},\n"
            f"  Access: {self.access},\n"
            f"  Dreadfarm: {self.dreadfarm},\n"
            f"  Inventory: {self.inventory},\n"
            f"  Ender Chest: {self.ender_chest_contents},\n"
            f"  Ender Chest Page Icons: {self.ender_chest_page_icons},\n"
            f"  Equipment Contents: {self.equipment_contents}\n"
            f")"
        )
