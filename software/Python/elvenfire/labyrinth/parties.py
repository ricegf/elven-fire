import random

from elvenfire.creatures.character import PlayerCharacter
from elvenfire.creatures.trainable import TrainableAnimal
from elvenfire.creatures.nontrainable import NonTrainableCreature
from elvenfire.creatures.special import SpecialCreature

class _Party:

    """A party of creatures within the labyrinth.

    Class Attributes:
      creaturetype -- name of creature type, for printing

    Attributes:
      totalCP   -- total power of all creatures in group
      creatures -- list of creatures in group

    """

    creaturetype = 'Creature'

    def __init__(self, level, maxCP):
        """Initialize the Party and randomize."""
        self.totalCP = 0
        self.creatures = []
        self._populate(level, maxCP)

    def _populate(self, level, maxCP):
        """Randomly generate a party with CP between 1/2 maxCP and maxCP."""
        minCP = maxCP / 2
        while self.totalCP < minCP:
            creature = self._newcreature(level)
            power = creature.stats.power()
            if self.totalCP + power < maxCP:
                self.addcreature(creature)

    def addcreature(self, creature):
        """Add creature to this party."""
        self.creatures.append(creature)
        self.totalCP += creature.stats.power()

    def _newcreature(self, level, type=None):
        """Return a valid random creature for inclusion in this party."""
        raise NotImplementedError

    def __str__(self):
        val = '%s Party (%.2f CP):\n\n' % (self.creaturetype, self.totalCP)
        for c in self.creatures:
            val += str(c) + '\n\n'
        return val


class PCParty (_Party):

    """A group of player characters - fellow adventurers in the labyrinth!"""

    creaturetype = 'Character'

    def _newcreature(self, level):
        """Return a random character of the appropriate level."""
        charlevel = 10 * (level - 1) + random.randint(0, 9)
        return PlayerCharacter(charlevel=charlevel)


class TrainableParty (_Party):

    """A group of trainable animals."""

    creaturetype = 'Trainable Animal'

    def _newcreature(self, level):
        """Return a random Trainable Animal.

        Multiple calls on the same Party will yield the same creature class.

        """
        class_ = type = None
        if self.creatures:
            class_ = self.creatures[0].subtype
            if class_ is None: type = self.creatures[0].name
        return TrainableAnimal(type, class_)
        


class NonTrainableParty (_Party):

    """A group of non-trainable animals."""

    creaturetype = 'Non-Trainable, Non-Character'

    def _newcreature(self, level):
        """Return a random non-trainable, non-character creature.

        Multiple calls on the same Party will yield the same creature class.

        """
        class_ = type = None
        if self.creatures:
            class_ = self.creatures[0].subtype
            if class_ is None: type = self.creatures[0].name
        return NonTrainableCreature(type, class_)


class SpecialParty (_Party):

    """A group of special creatures."""

    creaturetype = "Special Creature"

    def _newcreature(self, level):
        """Return a random special creature.

        Multiple calls on the same Party will yield the same creature class.

        """
        class_ = type = None
        if self.creatures:
            class_ = self.creatures[0].subtype
            if class_ is None: type = self.creatures[0].name
        return SpecialCreature(class_, type)