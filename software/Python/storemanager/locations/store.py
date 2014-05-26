import random

from storemanager.locations import StoreError, _Store
from storemanager.stockitems.special import *
from storemanager.stockitems.combat import *
from storemanager.stockitems.greater import *
from storemanager.stockitems.lesser import *
from storemanager.stockitems.written import *
from storemanager.stockitems.potion import *

class GeneralStore (_Store):

    """A general store, carrying all manner of greater and lesser artifacts."""

    def randomname(self):
        """Return a random name."""
        return random.choice(('General Store', 'Pawn Shop', 
                              "Hugo's Big and Small", "The Donkey's Back",
                              "Hiawath's", "The Adventurer's Market",
                              "Labyrinth Kits, etc.", "Treasure Store",
                              "Treasure Island", "d8 dLite", "Off-Target", 
                              "Gandalf's Goods", "Lance's Lot"))

    def defaultdesc(self):
        """Return the default description."""
        return random.choice((
              "Carries a little bit of everything treasure.",
              "Greater and Lesser artifacts of all kinds.",
              "Everything your momma said you'd need.",
              "General treasure: a wholesale possibility",
              "Beware of Aisle 6: Traps!",
              "Blue Light Special: Lightning Rods!",
                             ))

    def randomitem(self):
        """Return an appropriate random artifact."""
        d6 = random.randint(1, 6)   # 1-2 = possibly Greater
        d20 = random.randint(1, 20) # 1-11 = Greater
        d10 = random.randint(1, 10) # for Lesser
        if d6 <= 2 and d20 <= 11:
            if d20 == 1:
                return SpecialArtifactStockItem()
            elif d20 <= 3:
                return STBatteryStockItem()
            elif d20 <= 5:
                return RingStockItem()
            elif d20 <= 7:
                return WeaponStockItem()
            elif d20 <= 9:
                return ArmorStockItem()
            else:
                return RodStockItem()
        else:
            if d10 == 1:
                return AmuletStockItem()
            elif d10 <= 3:
                return BookStockItem()
            elif d10 <= 5:
                return GemStockItem()
            elif d10 <= 7:
                return ScrollStockItem()
            else:
                return PotionStockItem()


class AnimalStore (_Store):

    def randomname(self):
        return random.choice(('Animals R Us', 'Purrfect Pets', 
                              'The Pooper Scooper', 'PetSmart',
                              'Creatures Galore', "Man's Best Friend",
                              'Trained to Kill', 'Trained and Ready'))

    def defaultdesc(self):
        return random.choice(('Trained animals of all sorts.',
                              'Friends to fight by your side.',
                              'For all your animal needs.',
                              'Where the pets go'))

    def randomitem(self):
        return TrainableAnimalStockItem()


class BookStore (_Store):

    """Contains books and scrolls."""

    def randomname(self):
        """Return a random name."""
        return random.choice(('Literate Warriors', 'Scrolls R Us',
                              'Black, White, and Read All Over',
                              'Kelvin 506', 'The Bonfire', 'Inkspots',
                              'The Wasp Nest', 'Quill and Power',
                              'Parchment and Prejudice', 'The Scrivner',
                              "Authors Hope", 'Litterbox', 'The Library',
                              'Open Sesame', 'Kindly Kindling',
                              'Inscrutable Ink', 'Words of Power'))

    def defaultdesc(self):
        """Return the default description."""
        return random.choice((
              "Ahhh, the smell of parchment!",
              "Books, Scrolls, and all things literate.",
              "If you can't read this, DO NOT ENTER!",
              "Parchment is not toilet paper!",
              "For literate eyes only",
                            ))

    def randomitem(self):
        """Return a random book or scroll."""
        roll = random.randint(1, 6)
        if roll <= 3:
            return BookStockItem()
        else:
            return ScrollStockItem()


class PotionStore (_Store):

    """Contains potions only."""

    def randomname(self):
        """Return a random name."""
        return random.choice(('Medieval Thymes', 'Drink Me', 'Double Bubble',
                              'Potions R Us', 'The Brewery', 'Half Full',
                              'Dealing Healing', 'On the Rocks',
                              'Drinks with a Twist', 'Flash and Burn',
                              'Potion Not Stirred', 'Moonbucks', 
                              'The Flaming Vial', 'Glittering Goblet',
                              'Pick Your Poison', 'Flash Bang'))

    def defaultdesc(self):
        """Return the default description."""
        return random.choice((
              "Potions: the poor man's magic",
              "Double, Bubble, Toil, and Trouble",
              "Chemistry at Work",
              "If you know what's in this bottle, you might be a Chemist!",
              "If you tried to make anything inside, you might be a Chemist!",
              "Antidotes found here; don't mind the markup...",
                             ))

    def randomitem(self):
        """Return a random potion, poison, or grenade."""
        return PotionStockItem()


class PhysicalWeaponStore (_Store):

    """Contains weapons only."""

    def randomname(self):
        """Return a random name."""
        return random.choice(('Neiman Hackus', 'The Point', "Bash'n'Smash",
                              'Pointy Sticks', "Ogre's Delight", 
                              "Trolls Welcome", '21 Folds', 'Double Edge',
                              'Broken Pen', 'Homemade Pincushions',
                              'The Big Stick', "Shakin' a Stick",
                              'Guilded Guard', 'Crushed', 'Sticks and Stuff',
                              'Lance A Lot'))

    def defaultdesc(self):
        """Return the default description."""
        return random.choice((
              "Enhanced weapons for all!",
              "Pointy things that make you go 'Ouch!'",
              "Sticks and stones that'll break some bones",
              "Dual Wielders, turn left-right.",
              "Sheathe our weekly specials!",
                             ))

    def randomitem(self):
        """Return a random physical weapon."""
        return WeaponStockItem()


class WeaponStore (_Store):

    """Contains weapons and rods."""

    def randomname(self):
        """Return a random name."""
        return random.choice(('Of Swords and Stones', 'Even Bigger Stick',
                              'The Staffing Agency', 'Hot Rods',
                              "Stewart's Shop of Has-Beens", 'Attack Dog',
                              'Wood and Steel', 'Clash and Burn',
                              'The Glory Hole', 'Rods R Us', 'Spare the Rod',
                              'Walk Softly'))

    def defaultdesc(self):
        """Return the default description."""
        return random.choice((
              "Carries both mental and physical weapons.",
              "Walk softly; carry one of our sticks",
              "This is the place to be offensive!",
              "Ethereal and other weapons",
              "Hacking and slashing prices every Thursday!",
                             ))

    def randomitem(self):
        """Return a random weapon or rod."""
        roll = random.randint(1, 6)
        if roll <= 4:
            return WeaponStockItem()
        else:
            return RodStockItem()


class ArmorStore (_Store):

    """Contains armor and shields."""

    def randomname(self):
        """Return a random name."""
        return random.choice(("Can't Touch This", 'Invincible', 'Iron Heart', 
                              'The Codpiece', 'With Girded Loins',
                              'Fire Hydrants R Us', 'Left-Handed Life',
                              'Tupper Wear', 'Gear of Champions',
                              'Shields n Sleds', "Brooke's Shields",
                              'Trappings of a Warrior', 'Suit of Armor'))

    def defaultdesc(self):
        """Return the default description."""
        return random.choice((
              "Shields and armor.",
              "Don't get Defensive!",
              "Protection from bumps in the night",
              "We've got your butt covered!",
              "Head-to-toe protection",
              "Our shields will survive - even if you don't...",
                             ))

    def randomitem(self):
        """Return a random shield or suit of armor."""
        return ArmorStockItem()


class MagicStore (_Store):

    """Contains rings, rods, amulets, gems, and special artifacts."""

    def randomname(self):
        """Return a random name."""
        return random.choice(('Little Shop of Heaven', "Merlin's",
                              'Atlantean Treasures', "Magic LeFey",
                              "Dumbledore's", "Potter's Hobby",
                              "Humphrey's", "Double Treasure",
                              "Abra Cadabra", 'House of Houdini'))

    def defaultdesc(self):
        """Return the default description."""
        return random.choice((
              "Artifacts: special, amulets, rods, rings, and gems.",
                            ))

    def randomitem(self):
        """Return an appropriate random artifact."""
        roll = random.randint(1, 21)
        if roll == 1:
            return SpecialArtifactStockItem()
        elif roll <= 3:
            return STBatteryStockItem()
        elif roll <= 6:
            return AmuletStockItem()
        elif roll <= 10:
            return RodStockItem()
        elif roll <= 15:
            return RingStockItem()
        else:
            return GemStockItem()

    def randomdice(self):
        """Determine store's die rolls based on townsize."""
        self.numdice = max(1, self.townsize - 2)
        self.diesize = 6


class GemStore (_Store):

    """Carries gems and the occasional strength battery."""

    def randomname(self):
        """Return a random name."""
        return random.choice(('Pet Rocks', 'Shiny Stones', 'Gems Galore',
                              'Stones that Sparkle', 'Singular Spells'))

    def defaultdesc(self):
        """Return an appropriate default description."""
        return random.choice((
              "Plenty of gems, and the occasional strength battery.",
              "Magic stones of all sorts.",
                            ))

    def randomitem(self):
        """Return an appropriate random artifact."""
        if random.randint(1, 20) == 1:
            return STBatteryStockItem()
        else:
            return GemStockItem()

