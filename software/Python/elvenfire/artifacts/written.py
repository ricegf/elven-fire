import random

from elvenfire import bonus5, bonus25
from elvenfire import languages, rarelanguages, randomlanguage
from elvenfire.artifacts import ArtifactError, _MultiAbilityArtifact
from elvenfire.abilities.charabilities import *


class _WrittenArtifact (_MultiAbilityArtifact):

    """An artifact that has been written in a particular language.

    New attributes:
      self.language -- string indicating the language

    allowduplicates is set True for this artifact type, meaning the same
    ability may exist multiple times, with different IIQs.

    """

    allowduplicates = True

    def __init__(self, abilities=None, language=None):
        self.language = language
        if self.language is None:
            self.language = randomlanguage()
        elif self.language not in languages:
            raise ArtifactError("Invalid language: %s" % self.language)
        _MultiAbilityArtifact.__init__(self, abilities)
        self.name += ': %s' % self.language

    def _lookup(self):
        _MultiAbilityArtifact._lookup(self)
        if self.language in rarelanguages:
            self.value = round(self.value * 0.75)
        elif self.language != 'Common':
            self.value = round(self.value * 0.90)

class Scroll (_WrittenArtifact):

    """A scroll, containing up to 5 mental abilities."""

             #########!#########!#########!#########!#########!#########!#########!#########!
    desc = ('Requires 2 hands to hold; read out loud to activate. Self-powered and requires\n' +
            ' no 3vDx roll.')

    # A scroll is worth 1/20 the equivalent ring
    valuedivisor = 20

    def _newability(self):
        return MentalAbilityWithOpposites()

    def _validability(self, ability):
        """Return boolean indicating if ability is valid for this item."""
        return isinstance(ability, MentalAbility)


class Book (_WrittenArtifact):

    """A book, containing up to 25 pages of physical or mental abilities."""

             #########!#########!#########!#########!#########!#########!#########!#########!
    desc = ('Using an ability from a book costs a Dx penalty twice the IIQ value. Causes\n' + 
            ' fatigue and requires a 3vDx roll to cast.')

    maxabilities = 25

    # A book is worth the sum of its pages divided by 10
    multipliers = [1] * 25
    valuedivisor = 10

    def _newability(self):
        return PhysicalOrMentalAbility()

    def _validability(self, ability):
        """Return boolean indicating if ability is valid for this item."""
        return (isinstance(ability, PhysicalAbility) or
                isinstance(ability, MentalAbility))

    def _numabilities(self):
        return bonus25()


