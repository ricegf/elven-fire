
import random
import re

from elvenfire import bonus5
from elvenfire.abilities import AbilityError, _Ability
# as needed: from elvenfire.artifacts.lesserartifacts import Ring
# as needed: from elvenfire.artifacts import ArtifactError


"""Non-Character Abilities (meant for use in ELF items).

AttributeAbility - a bonus to an attribute (ST, Damage, etc)
AmuletAbility - a special ability used in an Amulet (e.g. Control Dragon)
WeaponAbility - a special ability used in a Weapon (e.g. Animated)

"""


class AttributeAbility (_Ability):

    """An attribute ability: ST, DX, IQ, MA, Dam, or Hit.

    Additional Attributes:
      self.attr   -- attribute affected (e.g. 'ST')
      self.size   -- amount added to attribute (1..5)
      self.listAC -- tuple containing the AC at each size, in 1000s

    """

    def __init__(self, attr=('ST', 'DX', 'IQ', 'MA'), size=None):
        """Initialize the AttributeAbility.

        Parameters:
          attr -- a list/tuple of available attributes
                  default: ('ST', 'DX', 'IQ', 'MA')
          size -- (optional) desired size of attribute bonus

        """
        if isinstance(attr, str):
            self.attr = attr
        elif '__iter__' in dir(attr):
            self.attr = random.choice(attr)
        else:
            raise AbilityError("Invalid attribute list specification: %s" %
                               attr)
        self.size = size
        _Ability.__init__(self, "%s+" % self.attr)  # bypass _randomize()

    def _lookup(self):
        if self.size is None:
            self._randomSize()
        self._lookupAC()
        self._computeAC()
        self.desc = "Adds %s to the character's %s" % (self.size, self.attr) \
                    + " as long as the item is in use."

    def __str__(self):
        if self.attr == 'MA':
            size = self.size * 2
        else:
            size = self.size
        return "%s+%s" % (self.attr, size)

    def _randomSize(self):
        """Set self.size for this attribute boost: 1..5"""
        self.size = bonus5()

    def _lookupAC(self):
        """Determine self.listAC tuple based on attribute type."""
        map = {'ST' : (2, 4, 7, 15, 25),
               'DX' : (2, 4, 7, 15, 25),
               'IQ' : (1, 2, 3.5, 7, 15),
               'MA' : (1, 2, 3, 6, 12),
               'Dam' : (1, 2, 3.5, 7, 15),
               'Hit' : (1, 2.5, 5, 10, 18)}
        if self.attr not in map:
            raise AbilityError("Unrecognized attr '%s'" % self.attr)
        self.listAC = map[self.attr]

    def _computeAC(self):
        """Determine self.AC based on self.size and self.listAC."""
        if not (isinstance(self.size, int) and 1 <= self.size <= 5):
            raise AbilityError("Invalid size '%s'" % self.size)
        self.AC = int(1000 * self.listAC[self.size-1])

    def duplicate(self, other):
        """Return boolean indicating if the same attribute is modified."""
        if isinstance(other, AttributeAbility):
            return self.attr == other.attr
        return False

    def worsethan(self, other):
        """Return boolean indicating if other is a larger bonus."""
        return other.size > self.size


class AmuletAbility (_Ability):

    """An ability suited for use in an amulet."""

    controls = ['NPC', 'Trainable Riding Animal', 'Trainable Non-Riding Animal',
                'Non-Trainable Mammal', 'Non-Trainable Reptile',
                'Non-Trainable Insect', 'Dragon', 'Elemental']

    typelist = ['Control NPC', 
                'Control Trainable Riding Animal', 
                'Control Trainable Non-Riding Animal',
                'Control Non-Trainable Mammal', 
                'Control Non-Trainable Reptile',
                'Control Non-Trainable Insect',
                'Control Dragon', 
                'Control Elemental',
                'Proof', 
                'Attribute', 
                'Skepticism']

    elements = ['Fire', 'Water', 'Cold', 'Lightning']

    attributes = ['ST', 'DX', 'IQ']

    def __init__(self, type=None, element=None, attr=None, size=None):
        """Initialize the AmuletAbility.

        Parameters (generated randomly if not supplied):
            type    -- selected from AmuletAbility.typelist 
                       (e.g. Proof)
            element -- (for Proof only) selected from 
                       AmuletAbility.elements
            attr    -- (for Attribute only) selected from
                       AmuletAbility.attributes
            size    -- (for Skepticism only) integer 1..5

        """
        self.element = element
        self.attribute = attr
        self.size = size
        if type is None:
            if element is not None:
                type = 'Proof'
            elif attr is not None:
                type = 'Attribute'
            elif size is not None:
                type = 'Skepticism'
        _Ability.__init__(self, type)

    def _lookup(self):
        """Define self.desc and self.AC based on self.name."""
        self.type = self.name  # name will be updated with element/size
        if self.name.startswith('Control'):
            if self.name.endswith('NPC'):
                self.AC = 10000
            elif self.name.endswith('Dragon'):
                self.AC = 25000
            elif self.name.endswith('Elemental'):
                self.AC = 5000
            elif self.name.startswith('Control Trainable'):
                self.AC = 2000
            elif self.name.startswith('Control Non-Trainable'):
                self.AC = 3000
            else:
                raise AbilityError('Unknown type of control amulet: %s' %
                                   self.name)
            self.desc = "When encountered, if creature fails 3vIQ," + \
                        " amulet holder controls the creature totally."
        elif self.name == 'Proof':
            if self.element is None:
                self.element = random.choice(self.elements)
            elif self.element not in self.elements:
                raise AbilityError("Invalid amulet Proof element: '%s'" % 
                                   self.element)
            self.name += ': %s' % self.element
            if self.element == 'Cold':
                self.AC = 4000
            else:
                self.AC = 2000
            self.desc = "Makes wearer immune to damage by " + \
                        self.element.lower() + '.'
            if self.element == 'Water':
                self.desc += '  Allows breathing under water.'
        elif self.name == 'Attribute':
            # Not using an AttributeAbility, because this is always +1
            # and has inconsistent pricing.
            if self.attribute is None:
                self.attribute = random.choice(self.attributes)
            elif self.attribute not in self.attributes:
                raise AbilityError('Unknown amulet attribute: %s' % 
                                   self.attribute)
            self.name = "%s+1" % self.attribute
            self.AC = 5000
            self.desc = "Increases %s by 1 while worn." % self.attribute
            if self.attribute == 'IQ':
                self.desc += '  Does not allow learning of new abilities.'
        elif self.name == 'Skepticism':
            if self.size is None:
                self.size = bonus5()
            elif not (isinstance(self.size, int) and 1 <= self.size <= 5):
                raise AbilityError('Invalid Skepticism size: %s' % self.size)
            self.name += ' +%s' % self.size
            self.AC = (100, 250, 1000, 2000, 5000)[self.size-1]
            self.desc = 'Adjust roll by %s for each attempt to disbelieve.' \
                        % self.size
        else:
            raise AbilityError('Unknown amulet type: %s' % self.name)

        if self.element is not None and self.type != 'Proof':
            raise AbilityError('Element cannot be specified for %s amulets!' %
                               self.type)
        if self.attribute is not None and self.type != 'Attribute':
            raise AbilityError('Attribute cannot be specified for %s amulets!' %
                               self.type)
        if self.size is not None and self.type != 'Skepticism':
            raise AbilityError('Size cannot be specified for %s amulets!' %
                               self.type)

    def duplicate(self, other):
        """Return boolean indicating if abilities are of the same type.

        For Skepticism amulets, different sizes are treated as duplicates. For
        the remaining AbuletAbilitys, the name attribute is a sufficient
        comparison.

        """
        if not isinstance(other, AmuletAbility):
            return False
        if (re.match('Skepticism', self.name) and 
            re.match('Skepticism', other.name)):
            return True
        return self.name == other.name

    def worsethan(self, other):
        """Return indicating if other is a larger Skepticism bonus."""
        if re.match('Skepticism', self.name):
            return other.size > self.size
        return False  # otherwise, they are identical


class WeaponAbility(_Ability):

    """A special (non-attribute) ability suited for use in a weapon."""

    typelist = ['Animated', 'Changling', 'Defender', 'Electrified', 'Enhanced',
                'EverPoisoned', 'AutoPoisoned', 'Flaming', 'Frosted',
                'Guided', 'Replenisher']

    def __init__(self, type=None, range=None, size=None, abilities=None):
        """Initialize the WeaponAbility.

        Parameters (randomized if not provided):
          type      -- selected from WeaponAbility.typelist
          range     -- (Animated only) range of weapon
          size      -- (Defender only) Dx penalty to attacker
          abilities -- (Enhanced only) list of character abilities

        """
        self.range = range                # Animated
        self.size = size                  # Defender
        self.abilities = abilities        # Enhanced

        if type is None:
            if self.range is not None: type = 'Animated'
            if self.size is not None: type = 'Defender'
            if self.abilities is not None: type = 'Enhanced'

        _Ability.__init__(self, type)

        if self.range is not None and self.type != 'Animated':
            raise AbilityError('No range required for %s weapons!' % self.type)
        elif self.size is not None and self.type != 'Defender':
            raise AbilityError('No size required for %s weapons!' % self.type)
        elif self.abilities is not None and self.type != 'Enhanced':
            raise AbilityError('No abilities required for %s weapons!' % 
                                self.type)

    def _lookup(self):
        self.type = self.name  # name will be updated with range, etc.

        if self.type == 'Animated':
            if self.range is None:
                self.range = bonus5()
            elif not (isinstance(self.range, int) and 1 <= self.range <= 5):
                raise AbilityError("Invalid Animated weapon range: %s" %
                                   self.range)
            self.name += ' (%s MH)' % self.range
            self.AC = 1000 * (20, 22, 25, 30, 40)[self.range-1]
            self.desc = 'User can control weapon up to %s MH away' % self.range
            self.desc += ' Target is engaged; owner is not.'

        elif self.type == 'Changling':
            self.AC = 0  # calculated after both weapons determined
            self.desc = "Transforms between missile and melee weapon types" + \
                        " on bearer's command, even between rounds."
            self.desc += '  As a missile weapon, acts as a Replenisher.'

        elif self.type == 'Defender':
            if self.size is None:
                self.size = bonus5()
            elif not (isinstance(self.size, int) and 1 <= self.size <= 5):
                raise AbilityError("Invalid Defender weapon size: %s" %
                                   self.size)
            self.name += ' (DX-%s)' % self.size
            self.AC = 1000 * (2, 4, 7, 15, 25)[self.size-1]
            self.desc = "Holding weapon subtracts %s" % self.size + \
                        " from attacker's DX"

        elif self.type == 'Guided':
            self.AC = 12000
            self.desc = 'Can follow any course desired, flying around' + \
                        ' obstacles and friends to its full range.'

        elif self.type == 'Replenisher':
            self.AC = 2000
            self.desc = "Once the weapon completes its flight, it" + \
                        " reappears in the owner's hand, ready for reuse."

        elif self.type == 'Enhanced':
            from elvenfire.artifacts.greater import Ring
            from elvenfire.artifacts import ArtifactError
            try:
                # Handle generation/verification of mental abilities via Ring
                ability_gen = Ring(abilities=self.abilities)
            except ArtifactError as e:
                raise AbilityError('Enhanced WeaponAbility: %s' % e)
            self.abilities = ability_gen.abilities
            self.name += ': '
            if len(self.abilities) == 1:
                self.name += str(self.abilities[0])
            else:
                self.name += "%s abilities" % len(self.abilities)
            self.AC = ability_gen.value
            self.desc = 'Holding the weapon permits use of abilities,' + \
                        ' just like a ring.'

        else:  # Electrified, Flaming, etc
            self.AC = 10000
            if self.type == 'AutoPoisoned':
                self.desc = 'Can be preloaded with up to 12 weapon poisons.'
                self.desc += ' Wielder can invoke any loaded poison just\n' + \
                         ' before an attack, and poison will remain active' + \
                         ' until hit.'
                self.desc += '  Loading a poison requires 12 turns.'
            elif self.type == 'EverPoisoned':
                self.desc = 'If any damage is inflicted, victim must make' + \
                            ' 4vST for take 5.5 DCl additional damage.'
            else:
                self.desc = 'Adds 3.5 DCl to normal damage; double/half' + \
                            ' effects of the element apply.'

    def duplicate(self, other):
        """Return boolean indicating if special abilities are the same type."""
        if isinstance(other, WeaponAbility):
            return self.type == other.type
        return False

    def worsethan(self, other):
        """Return boolean indicating if other has a stronger ability.

        Account for range of 'Animated', DX of 'Defender', AC of 'Enhanced'.

        """
        if self.type == 'Animated':
            return other.range > self.range
        elif self.type == 'Defender':
            return other.size > self.size
        elif self.type == 'Enhanced':
            return other.AC > self.AC
        return False  # other types are identical


