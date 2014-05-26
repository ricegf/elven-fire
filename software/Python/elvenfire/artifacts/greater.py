import random

from elvenfire import bonus5, bonus25
from elvenfire.artifacts import ArtifactError, _Artifact, _MultiAbilityArtifact
from elvenfire.artifacts.special import STBattery
from elvenfire.abilities.charabilities import *


"""Greater Artifacts

Rod  -- carries 1-25 charges and a single Ethereal Bow ability
Ring -- carries 1-5 mental abilities and allows repeat use

"""


class Rod (_Artifact):

    """Rod containing 1-25 charges and a single Ethereal Bow ability."""

    def __init__(self, charges=None, ability=None, IIQ=None):
        self.charges = charges
        self.ability = ability
        self.IIQ = IIQ
        _Artifact.__init__(self)

    def _randomize(self):
        if self.ability is None:
            bow = random.choice(MentalAbility.EtherealBow)
            self.ability = MentalAbility(bow, self.IIQ)
        elif not (isinstance(self.ability, MentalAbility) and
                  self.ability.name in MentalAbility.EtherealBow):
            raise ArtifactError("Invalid rod ability: %s" % self.ability)
        if self.charges is None:
            self.charges = bonus25()
        elif not (isinstance(self.charges, int) and 1 <= self.charges <= 25):
            raise ArtifactError("Invalid # of charges: %s" % self.charges)
        self.name = "Rod of %s (%s charges)" % (self.ability, self.charges)

    def _lookup(self):
        self.value = self.ability.AC + STBattery(self.charges).value
        self.desc = ('Causes fatigue and a 3vDx roll, but has unlimited' +
                     ' usage. Recharge costs $25/ST\n in town.\n\n' +
                     self.ability.description())


class Ring (_MultiAbilityArtifact):

    """Ring containing 1-5 mental abilities."""

    desc = 'Requires one round to put on or remove.'

    def _newability(self):
        return MentalAbilityWithOpposites()

    def _validability(self, ability):
        """Return boolean indicating if ability is valid for this item."""
        return isinstance(ability, MentalAbility)