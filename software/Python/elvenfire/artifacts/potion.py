import random

from elvenfire import bonus5, bonus25
from elvenfire.artifacts import ArtifactError, _Artifact
from elvenfire.abilities.itemabilities import AttributeAbility
from elvenfire.abilities.charabilities import *

"""Potions: weapon poison, grenade, attribute, ability, or special

"""

class Potion (_Artifact):

    """Common base class for all potions"""

    def __init__(self, cls=None, name=None):

        if cls is not None:
            self.cls = cls
            _Artifact.__init__(self, name)
            return

        # Otherwise, generate a random potion...

        name = None
        type = random.choice(('Healing', 'Poison', 'Other'))

        if type == 'Healing':
            if random.randint(1, 8) == 1:
                cls = SpecialPotion
                name = 'Universal Antidote'
            else:
                cls = HealingPotion

        elif type == 'Poison':
            if random.random() < 0.50:
                cls = WeaponPoison
            else:
                cls = Grenade

        elif type == 'Other':
            roll = random.randint(1, 10)
            if roll <= 7:
                cls = AttributePotion
            elif roll == 8:
                cls = SpecialPotion
                name = 'Revival Potion'
            elif roll == 9:
                cls = SpecialPotion
                name = 'Universal Solvent'
            else:
                cls = AbilityPotion
        else:
            raise ArtifactError("Unknown potion type: %s")

        cls.__init__(self, name)

    def _randomize(self):
        self.cls._randomize(self)

    def _lookup(self):
        self.cls._lookup(self)


class HealingPotion (Potion):

    """Healing potion; 1..25 doses

    New attributes:
      doses -- number of available doses

    """

    # Description here, for easy access from store
    desc = ('May drink 1 point at a time to heal exact amount needed.')

    def __init__(self, doses=None):
        self.doses = doses
        Potion.__init__(self, HealingPotion)

    def _randomize(self):
        if self.doses is None:
            roll = random.choice((25, 20, 12, 10, 8, 6, 4))
            if roll == 25:
                self.doses = 25
            else:
                self.doses = 5 + random.randint(1, roll)
        elif not (isinstance(self.doses, int) and 1<= self.doses):
            raise ArtifactError("Invalid # of doses: %s!" % self.doses)
        self.name = "Healing Potion (%s points)" % self.doses

    def _lookup(self):
        # self.desc defined as class attribute
        self.value = 50 * self.doses


class WeaponPoison (Potion):

    """Poison for a weapon

    New attributes:
      doses -- number of available doses
      dmg   -- string describing damage done

    Class attributes:
      sizelist -- available dmg options
      typelist -- available types for the '+d20 vs' poisons

    """

    sizelist = ['Dam +d100', 'Dam +d12', 'Dam +d10', 'Dam +2d20', 'Dam +d20',
                'Dam +d6 & Sleep', 'Dam +d6 & Freeze', 'Dam +d6 & Slow',
                'Dam +d6', 'Drain 3/r for 6 rounds', '+d20 vs']
    values = (10000, 600, 500, 2000, 1000, 350, 300, 250, 50, 500, 50)

    typelist = ['Dragons', 'Hydras', 'Reptiles', 'Plants', 'Mammals', 'Insects']

    def __init__(self, dmg=None, type=None, doses=None):
        self.dmg = dmg
        self.type = type
        self.doses = doses
        Potion.__init__(self, WeaponPoison)

    def _randomize(self):
        if self.dmg is None:
            single = WeaponPoison.sizelist[:5]
            double = WeaponPoison.sizelist[5:8]
            triple = WeaponPoison.sizelist[8:]
            self.dmg = random.choice(single + 2 * double + 3 * triple)

        if self.dmg == '+d20 vs':
            if self.type is None:
                self.type = random.choice(WeaponPoison.typelist)
            elif self.type not in WeaponPoison.typelist:
                raise ArtifactError("Invalid poison type: %s" % self.type)
            self.dmg += " %s" % self.type
        elif self.type is not None:
            raise ArtifactError("Type not required for %s poison!" % self.dmg)

        self.name = "%s Weapon Poison" % self.dmg

        if self.dmg in ('Dam +d12', 'Dam +d10'):
            if self.doses is None:
                self.doses = random.randint(1, 4)
            elif not (isinstance(self.doses, int) and 1 <= self.doses <= 4):
                raise ArtifactError("Invalid number of doses: %s" % self.doses)
        elif self.doses is not None and self.doses != 1:
            raise ArtifactError("Multiple doses not allowed for %s poison" %
                                self.dmg)
        else:
            self.doses = 1

    def _lookup(self):
        self.desc = ('Requires 1 turn to apply prior to attack, but may be' +
                     ' applied prior to entering\n a room.')
        if self.dmg.startswith(WeaponPoison.sizelist[10]):
            self.value = WeaponPoison.values[10]
            return
        try:
            self.value = WeaponPoison.values[WeaponPoison.sizelist.index(self.dmg)]
        except ValueError as e:
            raise ArtifactError("Error locating value of %s" % self.name)
        self.value *= self.doses


class Grenade (Potion):

    """Thrown potion with damage to target hex and adjacent hexes.

    New attributes:
      type -- type of grenade damage (e.g. 'Contact')
      dmg  -- string describing damage done to each hex

    Class attributes:
      sizelist - available dmg values
      typelist - available grenade types

    """

    sizelist = ['d20 & d12 & d6', 'd12 & d8', 'd10 & d6', 'd8 & d4']
    values = (1000, 400, 250, 100)

    typelist = ['Gas', 'Contact', 'Water']

    def __init__(self, dmg=None, type=None):
        self.dmg = dmg
        self.type = type
        Potion.__init__(self, Grenade)

    def _randomize(self):
        if self.dmg is None:
            weighted = []
            for i in range(len(Grenade.sizelist)):
                weighted += [Grenade.sizelist[i],] * (i + 1)
            self.dmg = random.choice(weighted)
        elif self.dmg not in Grenade.sizelist:
            raise ArtifactError("Invalid grenade size: %s" % self.dmg)

        if self.type is None:
            weighted = ['Gas',] + Grenade.typelist
            self.type = random.choice(weighted)
        elif self.type not in Grenade.typelist:
            raise ArtifactError("Invalid grenade type: %s" % self.type)

        self.name = "%s Grenade (%s)" % (self.type, self.dmg)

    def _lookup(self):
        try:
            self.value = Grenade.values[Grenade.sizelist.index(self.dmg)]
        except ValueError as e:
            raise ArtifactError("Error locating value of %s" % self.name)
        self.desc = ('Thrown, damaging any friend or foe in the target hex' +
                     ' (and surrounded hexes)')


class AttributePotion (Potion):

    """Potions that increase a character attribute (e.g. ST).

    New attributes:
      ability    -- AttributeAbility in effect
      attributes -- list of available attributes

    """

    attributes = ['ST', 'DX', 'IQ', 'MA']

    def __init__(self, ability=None, attr=None, size=None):
        self.ability = ability
        self.attr = attr
        self.size = size
        Potion.__init__(self, AttributePotion)

    def _randomize(self):
        if self.ability is None:
            if self.attr is None:
                weighted = ['MA',] + AttributePotion.attributes
                self.ability = AttributeAbility(weighted, self.size)
            elif self.attr not in self.attributes:
                raise ArtifactError("Invalid attribute for potion: %s" %
                                    self.attr)
            else:
                self.ability = AttributeAbility([self.attr,], self.size)
        elif not isinstance(self.ability, AttributeAbility):
            raise ArtifactError("Invalid ability for attribute potion: %s" %
                                self.ability)
        self.name = "Potion of %s" % self.ability

    def _lookup(self):
        self.value = round(self.ability.AC / 5)
        self.desc = ('Swallow to activate; adds %s to %s for a full day' %
                     (self.ability.size, self.ability.attr))
        self.desc += '\n\n%s' % self.ability.description()


class AbilityPotion (Potion):

    """Potion that allows the temporary use of a character ability."""

    def __init__(self, ability=None, IIQ=None):
        self.ability = ability
        self.IIQ = IIQ
        Potion.__init__(self, AbilityPotion)

    def _randomize(self):
        if self.ability is None:
            self.ability = MentalAbilityWithOpposites(None, self.IIQ)
        elif not isinstance(self.ability, MentalAbility):
            raise ArtifactError("Invalid character ability for potion: %s" %
                                self.ability)
        self.name = "Potion of %s" % self.ability

    def _lookup(self):
        self.value = round(self.ability.AC / 20)
        self.desc = ('Ability potion requires one turn to consume; ability is then available for a\n' +
                     ' single use on any subsequent turn that day. Due to problems with interactions,\n' +
                     ' each ability potion over 5 consumed in the same day requires a 4vIQ roll or\n' +
                     ' one IQ point is lost forever.')
        self.desc += '\n\n%s' % self.ability.description()


class SpecialPotion (Potion):

    """Potions that don't fit anywhere else."""

    typelist = ['Revival Potion', 'Universal Solvent', 'Universal Antidote']

    def __init__(self, name=None):
        Potion.__init__(self, SpecialPotion, name)

    def _randomize(self):
        self.name = random.choice(SpecialPotion.typelist)

    def _lookup(self):
        if self.name == 'Revival Potion':
            self.value = 25000
            self.desc = ('Must be administered within a day of death, and always results in a character\n' +
                         ' losing 5 attribute points (selected by player).')
        elif self.name == 'Universal Solvent':
            self.value = 1000
            self.desc = ('Comes in two vials; when mixed, it destroys anything it touches. Avoiding a\n' +
                         ' spill when mixing requires 3vDx, or 3d6 damage is done to self.')
        elif self.name == 'Universal Antidote':
            self.value = 1000
            self.desc = ('Cures all hits and any poison')
        else:
            raise ArtifactError("Unrecognized potion type: %s" % self.name)


