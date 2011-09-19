import random
import pickle

from elvenfire import bonus5
from elvenfire.mundane.weapons import MundaneWeapon
from elvenfire.mundane.armor import MundaneArmor
from elvenfire.artifacts import ArtifactError, _MultiAbilityArtifact
from elvenfire.abilities.itemabilities import AttributeAbility, WeaponAbility
from elvenfire.abilities.charabilities import *


class Weapon (MundaneWeapon, _MultiAbilityArtifact):

    """A weapon, with one or more enhancements.

    New class attributes:
      attributes   -- list of all available attributes

    New attributes:
      specials   -- the number of special weapon abilities present
      changling  -- boolean indicating if this is a Changling weapon;
                    if True, primaryweapon and secondaryweapon will also be
                    defined, as Weapons

    """

    attributes = ['ST', 'DX', 'Dam']

    def __init__(self, style=None, type=None, maxST=None, abilities=None, 
                       secondary=False, secondaryweapon=None, artifact=True):
        typeset = (style is not None or type is not None)
        abilitiesset = (abilities is not None)
        self.changling = False
        MundaneWeapon.__init__(self, style, type, maxST)
        self.name = self.type

        if artifact:
            self.itemtype = self.type
            _MultiAbilityArtifact.__init__(self, abilities)
            self._handlespecials(secondary, typeset, abilitiesset, secondaryweapon)
            if abilities is not None:
                # Set self.specials anyway, for use in short()
                self.specials = 0
                for a in abilities:
                    if isinstance(a, WeaponAbility):
                        self.specials += 1

    def __str__(self):
        if 'abilities' in dir(self):
            return _MultiAbilityArtifact.__str__(self)
        else:
            return MundaneWeapon.__str__(self)

    def _numabilities(self):
        """Return total number of abilities to be added; set self.specials.

        This method is designed to closely follow the rolls made when manually
        generating random weapons.

        """
        rolls_remaining = 1
        numabilities = 0
        numspecials = 0
        while rolls_remaining > 0:
            roll = random.randint(1, 12)
            if roll == 1:                          # roll twice more
                rolls_remaining += 1
            elif roll == 2:                        # special & roll again
                numspecials += 1
                numabilities += 1
            else:                                  # attribute
                numabilities += 1
                rolls_remaining -= 1
            if numabilities >= self.maxabilities:  # limit total abilities
                rolls_remaining = 0
        numspecials = max(numspecials,             # limit attr abilities
                          numabilities - len(self.attributes))
        self.specials = numspecials
        return numabilities

    def _newability(self):
        if self.specials > len(self.abilities):
            return WeaponAbility()
        else:
            return AttributeAbility(self.attributes)

    def _handlespecials(self, secondary, typeset, abilitiesset, 
                              secondaryweapon):
        """Handle any necessary adjustments based on special abilities."""

        # Guided weapons must be distance weapons.
        GUIDED = WeaponAbility('Guided')
        if GUIDED in self.abilities and not self.isdistance():
            if typeset and abilitiesset:
                raise ArtifactError("Cannot comply with both type/style" +
                                    " and ability requirements.")
            elif not typeset:
                newstyle = random.choice(('Missile Weapon', 'Thrown Weapon'))
                self._setweapontype(newstyle)
            else:  # not abilitiesset
                self.abilities.remove(GUIDED)
                replacement = WeaponAbility()
                while (replacement == GUIDED or
                       replacement in self.abilities):
                    replacement = WeaponAbility()
                self.abilities.append(replacement)
            _MultiAbilityArtifact._setname(self)

        # Changlings are two weapons in one, with two separate ability sets
        CHANGLING = WeaponAbility('Changling')
        self.changling = False
        if not secondary and CHANGLING in self.abilities:

            # What we have so far becomes the primary
            self.primaryweapon = Weapon(self.style, self.type,
                                        abilities=list(self.abilities), 
                                        secondary=True)

            # And we roll a new set for the secondary...
            if secondaryweapon is not None:
                self.secondaryweapon = secondaryweapon
                if not isinstance(self.secondaryweapon, Weapon):
                    raise ArtifactError('%s is not a weapon!' % 
                                        self.secondaryweapon)
            else:
                if 'Bow' in self.style:
                    newstyle = random.choice(('Sword', 'Ax/Mace/Hammer',
                                              'Pole Weapon', 'Unusual Weapon'))
                else:
                    newstyle = random.choice(('Drawn Bow', 'Cross Bow'))
                self.secondaryweapon = Weapon(style=newstyle, secondary=True)

            # ... which must also include Changling (so max four)
            if CHANGLING in self.secondaryweapon.abilities:
                self.secondaryweapon.abilities.remove(CHANGLING)
            if len(self.secondaryweapon.abilities) == 5:
                self.secondaryweapon.abilities = \
                    self.secondaryweapon.abilities[:4]

            # Update this weapon to show ALL abilities, types, etc
            self.abilities += self.secondaryweapon.abilities
            self.type = "%s / %s" % (self.primaryweapon.type,
                                     self.secondaryweapon.type)
            self.itemtype = "Changling %s" % self.type
            self.value = (5000 + max(self.primaryweapon.value,
                                     self.secondaryweapon.value) +
                          2 * min(self.primaryweapon.value,
                                  self.secondaryweapon.value))

            # Finally, remove 'Changling' from the primary's list
            # to clean up the display, and update.
            self.primaryweapon.abilities.remove(CHANGLING)
            _MultiAbilityArtifact._setname(self.primaryweapon)
            self.changling = True
            _MultiAbilityArtifact._setname(self)

    def _validability(self, ability):
        """Return boolean indicating if ability is valid for this item."""
        return (isinstance(ability, AttributeAbility) or
                isinstance(ability, WeaponAbility))

    def description(self):
        if self.changling:
            (p, s) = (self.primaryweapon, self.secondaryweapon)
            return "%s:\n\n%s\n\n\n\n%s:\n\n%s" % (p.itemtype,
                                                   p.description(),
                                                   s.itemtype,
                                                   s.description())
        else:
            return _MultiAbilityArtifact.description(self)


class Armor (MundaneArmor, _MultiAbilityArtifact):

    """Armor or shield, with one or more attribute enhancement(s).

    Class attributes:
      attributes  -- list of available attributes

    """

    attributes = ['Hit', 'DX', 'MA']

    def __init__(self, type=None, wearer=None, abilities=None, artifact=True):
        MundaneArmor.__init__(self, type, wearer)
        if artifact:
            self.itemtype = self.name
            _MultiAbilityArtifact.__init__(self, abilities)

    def __str__(self):
        if 'abilities' in dir(self):
            return _MultiAbilityArtifact.__str__(self)
        else:
            return MundaneArmor.__str__(self)

    def _numabilities(self):
        num = 1
        while num < 5 and random.randint(1, 10) == 1:  # roll twice more
            num += 1
        return min(num, len(self.attributes))

    def _newability(self):
        return AttributeAbility(self.attributes)

    def _validability(self, ability):
        """Return boolean indicating if ability is valid for this item."""
        return isinstance(ability, AttributeAbility)


