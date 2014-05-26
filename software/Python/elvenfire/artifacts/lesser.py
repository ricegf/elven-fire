import random

from elvenfire import bonus5, bonus25
from elvenfire.artifacts import ArtifactError, _Artifact, _MultiAbilityArtifact
from elvenfire.abilities.itemabilities import AmuletAbility
from elvenfire.abilities.charabilities import *


"""Lesser Artifacts

"""


class Amulet (_MultiAbilityArtifact):

    """Amulet containing one or more amulet abilities."""

    def _numabilities(self):
        val = 1
        while val < 5 and random.randint(1, 12) == 1:  # roll twice more
            val += 1
        return val

    def _newability(self):
        return AmuletAbility()

    def _validability(self, ability):
        """Return boolean indicating if ability is valid for this item."""
        return isinstance(ability, AmuletAbility)


class Gem (_Artifact):

    """Gem containing a single mental ability."""

    def __init__(self, ability=None, IIQ=None):
        self.ability = ability
        self.IIQ = IIQ
        _Artifact.__init__(self)

    def _randomize(self):
        if self.ability is None:
            self.ability = MentalAbilityWithOpposites(None, self.IIQ)
        elif not isinstance(self.ability, MentalAbility):
            raise ArtifactError("Invalid gem ability: %s" % self.ability)
        self.name = "Gem of %s" % self.ability

    def _lookup(self):
        self.value = round(self.ability.AC / 10)
                     #########!#########!#########!#########!#########!#########!#########!#########!
        self.desc = ('Smash on ground to activate. Maybe be thrown to initiate from different\n'
                     ' location. Self-powered, and does not require a roll to activate.\n\n' +
                     self.ability.description())