import random

from elvenfire import ELFError, bonus5
from elvenfire.abilities import _Ability

__all__ = ['special', 'combat', 'greater', 'lesser', 'written', 'potion']

class ArtifactError (ELFError):
    pass


class _Artifact:

    """Abstract class: an artifact with one or more abilities.

    Attributes:
      self.name     -- name (or brief description) of artifact
      self.desc     -- (optional)long-hand description of artifact, including
                       usage information as applicable
      self.value    -- fair market value of artifact
      self.itemtype -- class name (sans packages and any 'StockItem' suffix)

    Note that these attributes are chosen to align with the _StockItem
    class from elvenfire.storemanager.stockitems for multiple inheritance.

    Methods to implement:
      _randomize() -- randomly select a value for self.name (by default,
                      will be chosen from self.typelist, if it exists)
      _lookup()    -- set self.value [and self.desc] based on self.name

    """

    def __init__(self, name=None):
        self._setitemtype()
        self.name = name
        if self.name is None:
            self._randomize()
        self._lookup()

    def _randomize(self):
        if 'typelist' in dir(self):
            self.name = random.choice(self.typelist)
        else:
            raise NotImplementedError()

    def _lookup(self):
        raise NotImplementedError()

    def _setitemtype(self):
        if 'itemtype' in dir(self):
            return
        itemtype = str(type(self))  # <class 'Something.Weapon'>
        i1 = itemtype.rfind('.')
        i2 = itemtype.find("'", i1)
        self.itemtype = itemtype[i1+1:i2]  # Weapon
        if self.itemtype.endswith('StockItem'):
            self.itemtype = self.itemtype[:-9]

    def __str__(self):
        return self.name

    def description(self):
        if 'desc' in dir(self):
            return self.desc
        return ''

    def __eq__(self, other):
        return (self.name == other.name and 
                self.description() == other.description())


class _MultiAbilityArtifact (_Artifact):

    """Abstract class: an artifact with more than one ability.

    New Attributes:
      self.abilities    -- list of _Ability objects

    Class Attributes:
      multipliers     -- tuple showing the correct multipliers for each
                         ability, ordered from highest to lowest AC
      maxabilities    -- maximum number of abilities allowed (default 5)
      valuedivisor    -- after the AC of each ability has been computed,
                         and the multipliers have been applied, the total
                         will be divided by this integer to yield the final
                         artifact value (default 1)
      allowduplicates -- if True, the same ability with different IIQs may
                         exist on the artifact (default: False)

    Methods to implement:
      _numabilities()  -- (optional) return an integer indicating how many
                          abilities should be generated (default: 1..5)
      _newability()    -- return an appropriate random _Ability object
      _validability()  -- return boolean indicating if ability is valid

    """

    multipliers = (1, 2, 4, 8, 16)
    maxabilities = 5
    valuedivisor = 1

    allowduplicates = False

    def __init__(self, abilities=None):
        self.abilities = abilities
        _Artifact.__init__(self)

    def _randomize(self):
        if self.abilities is None:
            self.abilities = []
            num = self._numabilities()
            for i in range(num):
                abil = self.__newability()  # will remove duplicates
                if abil is not None:
                    self.abilities.append(abil)
        else:
            if not (1 <= len(self.abilities) <= self.maxabilities):
                raise ArtifactError('Invalid number of abilities: %s' %
                                    len(self.abilities))
            for ability in self.abilities:
                if not self._validability(ability):
                    raise ArtifactError('Invalid ability: %s' % ability)
        self._setname()

    def __newability(self, count=0):
        """Wrapper for _newability() method; removes duplicate abilities."""
        if count > 250:
            raise ArtifactError('Cannot add new ability to %s (%s)' % 
                                (self.itemtype, map(str, self.abilities)))
        ability = self._newability()
        if ability in self.abilities:
            return self.__newability(count+1)  # recurse; try again
        if not self.allowduplicates:  # duplicates are same name, diff IIQ
            for a in self.abilities:
                if a.duplicate(ability) and a.worsethan(ability):
                    self.abilities[self.abilities.index(a)] = ability  # replace
                    return self.__newability(count)
        return ability

    def _setname(self):
        """Build self.name from type(self) and self.abilities."""
        if len(self.abilities) == 1:
            abilitystr = str(self.abilities[0])
        else:
            abilitystr = '(' + '; '.join(map(str, self.abilities)) + ')'
        self.name = "%s of %s" % (self.itemtype, abilitystr)

    def _lookup(self):
        """Set self.value to item's FMV, based on self.abilities"""
        self.abilities.sort()
        self.abilities.reverse()
        self.value = 0
        for ability, multiplier in zip(self.abilities, self.multipliers):
            self.value += ability.AC * multiplier
        self.value = int(self.value / self.valuedivisor)

    def description(self):
        if 'desc' in dir(self):
            val = self.desc
            if len(self.abilities) <= 3:
                val += '\n\n'
                val += '\n\n'.join([a.description() for a in self.abilities])
            return val
        return ''

    def _numabilities(self):
        """Return a random number of abilities to include."""
        return bonus5()

    def _newability(self):
        """Return a single new random ability."""
        raise NotImplementedError()

    def _validability(self, ability):
        """Return boolean indicating if ability is valid for this item."""
        return isinstance(ability, _Ability)





