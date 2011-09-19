import random
import math

from elvenfire import bonus5
from elvenfire.labyrinth import s

class Trap:

    """Abstract class used to define common code for all potential Traps."""

    def __init__(self):
        """Initialize all common values to None."""
        self.name = None
        self.explanation = None
        self.detect = self.remove = self.avoid = None
        self.numdice = self.diesize = None
        self.extrainfo = None

    def newtrap(level):
        """Class method: generate and return a new Trap of random type."""
        type = random.randint(1, 100)
        if type <= 11:
            return ExplosiveTrap(level)
        elif type <= 30:
            return MissileTrap(level)
        elif type <= 45:
            return GasTrap(level)
        elif type <= 55:
            return LiquidTrap(level)
        elif type <= 65:
            return EtherealTrap(level)
        elif type <= 80:
            return PitTrap(level)
        elif type <= 97:
            return OtherTrap(level)
        else:
            return SpecialTrap(level)

    def __str__(self):
        """Return a description suitable for explanation to the players."""
        val = "  Potential %s trap" % self.name
        if self.explanation is not None:
            val += " (%s)" % self.explanation
        val += "\n    Requires %svIQ to detect, " % self.detect
        val += "%svDx to remove, and %svDx to avoid." % (self.remove, self.avoid)
        if self.numdice is not None:
            val += "\n    Inflicts %sd%s hits if triggered." % \
                   (self.numdice, self.diesize)
        if self.extrainfo is not None:
            val += "\n    " + self.extrainfo
        return val


class ExplosiveTrap (Trap):

    """Potential trap featuring some type of explosive."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        size = random.randint(1,3)
        self.detect = int(level * 2 + (4 - math.sqrt(random.uniform(0, 9))))
        self.remove = int(size + level * 3 + (6 - math.sqrt(random.uniform(0, 9))))
        self.avoid = int(size + level + (4 - math.sqrt(random.uniform(0, 9))))
        self.numdice = int(size + level - 1)
        self.diesize = 6
        if size == 3:
            self.name = 'large explosive'
            self.explanation = '2/3 dmg in adjacent hex, 1/3 two hexes away'
        elif size == 2:
            self.name = 'medium explosive'
            self.explanation = '1/2 damage in adjacent hex'
        else:
            self.name = 'small explosive'
            self.explanation = None


class MissileTrap (Trap):

    """Potential trap featuring some form of physical missile weapon."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        size = random.randint(1,8)
        self.detect = int(level * 2 + (5 - math.sqrt(random.uniform(0, 16))))
        self.remove = int(size + level * 3 + (5 - math.sqrt(random.uniform(0, 16))))
        self.avoid = int(size + level + (3 - math.sqrt(random.uniform(1, 4))))
        if (size < 3):
            self.numdice = level
            self.diesize = 6
            self.name = 'piercing arrow'
            self.explanation = s(self.numdice, 'arrow')
        elif (size < 4):
            self.numdice = level
            self.diesize = 8
            self.name = 'broadhead arrow'
            self.explanation = s(self.numdice, 'arrow')
        elif (size < 6):
            self.numdice = level
            self.diesize = 10
            self.name = 'crossbow bolt'
            self.explanation = s(self.numdice, 'bolt')
        elif (size < 7):
            self.numdice = level
            self.diesize = 20
            self.name = 'explosive crossbow bolt'
            self.explanation = s(self.numdice, 'bolt')
        elif (size < 8):
            self.numdice = level
            self.diesize = 12
            self.name = 'spear'
            self.explanation = s(self.numdice, 'spear')
        else:
            self.numdice = 1 + int(level/2)
            self.diesize = 12
            self.name = 'scything blade'
            self.explanation = '1 blade'
        self.extrainfo = "Randomly identify SOURCE of each missile " + \
                         "triggered; then 'roll to miss'"

class GasTrap (Trap):

    """Potential trap featuring some type of poison gas."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        size = random.randint(1, 10)
        self.detect = int(1 + level + 4 - math.sqrt(random.uniform(0, 9)))
        self.remove = int(level * 2 + (4 - math.sqrt(random.uniform(0, 9))))
        self.avoid = int(level + (4 - math.sqrt(random.uniform(0, 9))))
        saving = 3 + level
        self.explanation = "%svSt if triggered to avoid effects" % saving
        self.numdice = self.diesize = None
        if size < 3:
            self.name = 'poison gas'
            self.extrainfo = "Poison causes d8 damage, ignore armor / shields" + \
                             " or other hit protection"
        elif size < 4:
            self.name = 'sleeping gas'
            self.extrainfo = "Sleep for 2d6 minutes; if 12, then d4 days" + \
                             "\n      " + \
                             " (roll for wandering creatures each minute)"
            #duration = random.randint(2, 12)
            #self.extrainfo = "Sleep for %s minutes" % duration + \
            #                 " (roll for wandering creatures each minute)"
            #if duration == 12:
            #    duration = random.randint(1, 4)
            #    self.extrainfo = "Sleep for %s days" % duration
        elif size < 5:
            self.name = 'blinding gas'
            self.extrainfo = "Blind (Dx-8) for 2d6 minutes (roll for" + \
                             " wandering creatures each minute);\n      " + \
                             " if 12, then d12 hours."
        elif size < 6:
            self.name = 'slow gas'
            if (random.randint(1, 6) == 6):
                effect = "1/3 MA (round down)"
            else:
                effect = "1/2 MA (round down)"
            self.extrainfo = "If triggered, %s for d4 battles" % effect
        elif size < 7:
            self.name = 'chlorine gas'
            self.extrainfo = "Chlorine causes d12 damage, ignore armor," + \
                             " shields, and other hit protection"
        elif size < 8:
            self.name = 'corroding gas'
            self.explanation = "artifacts get 3vDx roll to avoid damage"
            self.extrainfo = "Destroys metallic armor and shields."
        else:
            self.name = 'attribute-affecting gas'
            self.explanation = "%svAttr if triggered to avoid effects" % saving
            attr = random.choice(('strength', 'dexterity', 'intelligence'))
            dmg = random.randint(1, 2*level)
            self.extrainfo = "Reduces %s by %s for d4 battles." % (attr, dmg)


class LiquidTrap (Trap):

    """Potential trap featuring some type of damaging liquid."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        size = random.randint(1, 10)
        self.detect = int(level * 2 + (4 - math.sqrt(random.uniform(0, 9))))
        self.remove = int(size + level * 3 + (6 - math.sqrt(random.uniform(0, 25))))
        self.avoid = int(size + level + (4 - math.sqrt(random.uniform(0, 9))))
        self.explanation = "armor doesn't protect"
        if size < 6:
            self.name = 'flaming oil'
            self.extrainfo = "Will burn for d8 rounds, inflicting 2" + \
                             " additional hits per round."
            self.numdice = level
            self.diesize = 6
        elif size < 8:
            self.name = 'acid'
            self.numdice = 1 + level
            self.diesize = 8
        else:
            self.name = 'contact poison'
            self.avoid *= 2
            self.remove = int(self.remove / 2 + 1)
            self.numdice = level
            self.diesize = 6


class EtherealTrap (Trap):

    """Potential trap featuring some type of mental ability."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        size = random.randint(1, 10)
        self.detect = int(level * 2 + (4 - math.sqrt(random.uniform(0, 9))))
        self.remove = int(size + level * 3 + (6 - math.sqrt(random.uniform(0, 25))))
        self.avoid = int(size + level + (4 - math.sqrt(random.uniform(0, 9))))
        if size < 6:
            type = random.choice(('Lightning Bolt', 'Ether Arrow', 'Iceball',
                                  'Fireball', 'Boulder'))
            self.name = "Ethereal Bow (%s)" % type
            self.numdice = bonus5(level)
            self.diesize = 2 * (level + random.randint(1, 2*level))
            self.diesize = min((12, self.diesize))
            self.detect *= 2
            self.avoid *= 2
        elif size < 8:
            self.name = 'shock'
            self.explanation = 'does double damage if wearing metal armor'
            self.numdice = bonus5(level)
            self.diesize = 2 * random.randint(1, 4*level)
            self.diesize = min((10, self.diesize))
            self.avoid -= 1
            self.remove += 1
        else:
            self.name = 'teleporter'
            self.explanation = 'd6 direction for d10 megahexes'
            self.numdice = 1
            self.diesize = 4
            self.remove *= 3


class PitTrap (Trap):

    """Potential trap featuring some type of trapdoor or pit."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        size = random.randint(1, 10)
        self.detect = int(level * 2 + (5 - math.sqrt(random.uniform(0, 16))))
        self.remove = int(level * 3 + (6 - math.sqrt(random.uniform(0, 25))))
        self.avoid = int(level * 2 + (3 - math.sqrt(random.uniform(0, 4))))
        depth = 5 * random.randint(1, 2 * level)
        if size < 3:
            self.name = '%s-meter deep empty pit' % depth
            self.numdice = round(depth / 5)
            self.diesize = 4
        elif size < 4:
            self.name = '%s-meter deep spiked pit' % depth
            self.numdice = round(depth / 5)
            self.diesize = 6
        elif size < 5:
            self.name = '%s-meter deep viper pit' % depth
            self.explanation = 'd4/round until escape'
            self.numdice = round(depth / 5)
            self.diesize = 4
        elif size < 6:
            self.name = '%s-meter deep water-filled pit' % depth
            self.explanation = 'swim or drown'
            self.numdice = 1
            self.diesize = 4
        elif size < 7:
            self.name = '%s-meter deep flooding pit' % depth
            self.explanation = 'swim or drown'
            self.numdice = round(depth / 5)
            self.diesize = 4
        else:
            self.name = 'trapdoor to next level'
            self.numdice = round(depth / 5)
            self.diesize = 4


class OtherTrap (Trap):

    """Miscellaneous potential trap types."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        size = random.randint(1, 15)
        self.detect = int(level * 2 + (4 - math.sqrt(random.uniform(0, 9))))
        self.remove = int(level * 3 + (6 - math.sqrt(random.uniform(0, 25))))
        self.avoid = int(level + (4 - math.sqrt(random.uniform(0, 9))))
        if size < 8:
            self.name = 'scorpion'
            self.explanation = '50% chance of sting/round trying to pick lock'
            self.numdice = 1
            self.diesize = 8
            self.detect -= 1
            self.remove = 3
        elif size < 11:
            self.name = 'ball pendulum'
            self.numdice = bonus5(level)
            self.diesize = 4 + 2 * level
            self.remove -= 1
        elif size < 13:
            self.name = 'blade pendulum'
            self.numdice = bonus5(level)
            self.diesize = 8 + 2 * level
            self.remove -= 1
        elif size < 14:
            area = 3 + random.randint(0, 9)
            self.name = 'collapsing ceiling'
            self.explanation = 'covers %s hexes' % area
            self.numdice = bonus5(level)
            self.diesize = 2 * random.randint(level, level + 1)
            self.remove -= 2
            self.avoid += 1
        else:
            self.name = 'rolling ball'
            self.explanation = 'select edge hex & direction,' + \
                               ' moves 10/round'
            self.numdice = 1 + random.randint(level, level + 1)
            self.diesize = 8
        self.diesize = min((12, self.diesize))


class SpecialTrap (Trap):

    """Potential trap featuring some type of special effect."""

    def __init__(self, level):
        """Determine required die rolls and damage."""
        Trap.__init__(self)  # set all variables to None
        self.detect = int(level * 4 + (4 - math.sqrt(random.uniform(0, 9))))
        self.remove = int(1 + level + 4 - math.sqrt(random.uniform(0, 9)))
        self.avoid  = int(1 + level + 4 - math.sqrt(random.uniform(0, 9)))
        type = random.randint(1, 10)
        if type <= 4:
            self.name = 'minor disease'
            self.explanation = 'ST-1 until healed'
        elif type <= 7:
            dx = random.randint(11, 17)
            self.name = 'animate weapon'
            self.explanation = 'DX = %s, d4 damage' % dx
            self.remove += random.randint(1, 3)
            self.avoid += random.randint(1, 2)
        elif type <= 9:
            self.name = 'destroy one artifact'
            self.remove += random.randint(1, 3)
            self.avoid += random.randint(1, 2)
        else:
            self.name = 'lose 1 attribute point'
            self.remove += 1
            self.avoid += random.randint(1, 2)