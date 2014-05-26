import random
import math

from elvenfire import bonus5
from elvenfire.labyrinth.features import *
from elvenfire.labyrinth.special import SpecialArtifact
from elvenfire.labyrinth.containers import ContainerSet
from elvenfire.labyrinth.parties import *

class Room:

    """A labyrinth room, and all of its contents."""

    def __init__(self, level, num, difficulty=2):
        """Determine the features and contents of the room."""
        self.name = "Room %s" % num
        self.level = level
        self.setfeatures()
        self.setcontents(level, difficulty)

    def __str__(self):

        """Return a description suitable for explanation to the players."""

        val = self.name

        if self.features is not None:
            val += " with the following (distribute artistically):\n"
            val += "  " + "\n  ".join(self.features)
            val += "\n\n"
        else:
            val += ":\n"

        if self.contents:
            val += "\n".join(map(str, self.contents))
            val += "\n\n"
        else:
            val += "Nothing is in this room. "
            val += "Perhaps this would be a good resting place?"
            val += "\n\n"
            
        return val

    ## Features ##

    def setfeatures(self):

        """Determine the features of this room (column, bushes, etc)."""

        numfeatures = int(4 - math.sqrt(random.uniform(0, 16)))
        if numfeatures < 1:
            self.features = None
            return

        cannot_reuse = (Columns, RoughFloor, Bushes, Boulders)
        usedup = []

        self.features = []
        for i in range(numfeatures):
            feature = random.choice((Columns, Pools, RoughFloor, Bushes,
                                     Boulders, Pits, Walls))
            if feature in usedup:
                continue

            self.features.append(feature())
            if feature in cannot_reuse:
                usedup.append(feature)

    ## Contents ##

    def setcontents(self, level, difficulty):
        """Determine the contents of this room.

        Do NOT override this method to change the number of contents found, or
        the odds of finding each content type.  See Room.numcontents() and
        Room.randomcontent()

        """
        self.contents = []
        for i in range(self.numcontents(level)):
            content = self.randomcontent(level)
            if content == 'Creatures':
                self.add_creatures(level, difficulty)
            elif content == 'Containers':
                self.contents.append(ContainerSet(level))
            elif content == 'Empty':
                continue  # empty room
            elif content == 'Treasure':
                num = bonus5(level)
                self.contents.append("You see %s (distribute randomly)" %
                                     s(num, 'unguarded treasure'))
            elif content == 'Special':
                self.contents.append(SpecialArtifact(level))
            else:
                raise 'Unknown result from randomcontent(): %s' % content

    def numcontents(self, level):
        """Return the number of distinct content groups.

        Override this method to change the odds of finding multiple types of
        content within the same room (two character groups fighting, containers
        AND characters, etc).

        """
        return int(random.uniform(0, 11)/10 + 1)  # rarely 2, usually 1

    def randomcontent(self, level):
        """Return a random content type.

        Return values: Creatures, Containers, Empty, Treasure, Special

        Override this method to change the odds of finding each type.

        """
        roll = random.randint(1, 100)
        if roll <= 70:
            return 'Creatures'
        elif roll <= 85:
            return 'Containers'
        elif roll <= 90:
            return 'Empty'
        elif roll <= 98:
            return 'Treasure'
        else:
            return 'Special'

    ## (Creatures) ##

    def add_creatures(self, level, difficulty):
        """Add a creature group of a random type to the Room.

        Do NOT override this method to change the power or type of creatures
        found; see Room.maxCP() and Room.randomcreaturetype()

        """
        type = self.randomcreaturetype(level)
        if type == 'PC':
            self.contents.append(PCParty(level, self.maxCP(level, difficulty)))
        elif type == 'NPC':
            self.contents.append(NPCParty(level, self.maxCP(level, difficulty)))
        elif type == 'Trainable':
            self.contents.append(TrainableParty(level, 
                                                self.maxCP(level, difficulty)))
        elif type == 'Nontrainable':
            self.contents.append(NonTrainableParty(level, 
                                                   self.maxCP(level, difficulty)))
        elif type == 'Rare':
            self.contents.append(SpecialParty(level, 
                                              self.maxCP(level, difficulty)))
        else:
            raise 'Unknown result from randomcreaturetype(): $s' % type

    def maxCP(self, level, difficulty):
        """Return the maximum Creature Power that should be generated.

        Override this method to create rooms with differing difficulties.

        """
        base = math.sqrt(level) * 30 * (random.random() + 0.8)
        return base * (difficulty / 4)

    def randomcreaturetype(self, level):
        """Return a random creature type.

        Return values: PC, Trainable, Nontrainable, Rare

        Override this method to change the odds of finding each type.

        """
        roll = random.randint(1, 100)
        if roll <= 18:
            return 'PC'
        elif roll <= 33:
            return 'Trainable'
        elif roll <= 90:
            return 'Nontrainable'
        else:
            return 'Rare'


class SecretRoom (Room):
    """A SecretRoom is a Room that was hidden; containers are most likely."""
    def __init__(self, level, num, difficulty=2):
        Room.__init__(self, level, num, difficulty)
        self.name = "Secret Room %s" % num
        self._finddoor(level)

    def _finddoor(self, level):
        notice = self._getdiff(level)
        self.name += " (%dvIQ to notice)" % notice

    def _getdiff(self, level):
        roll = random.randint(1, 6) if level < 3 else random.randint(1, 8)
        num = 1 if level == 1 else 0
        if roll <= num: return 3
        num += 1
        if roll <= num: return 4
        num += 1 if level > 1 else 2
        if roll <= num: return 5
        num += 1 if level != 2 else 2
        if roll <= num: return 6
        num += 1 if level != 3 else 2
        if roll <= num: return 7
        num += 1 if level < 3 else 2
        if roll <= num: return 8
        return 9

    def randomcontent(self, level):
        """Determine the type of contents based on a random roll.

        Return values: Creatures, Containers, Empty, Treasure, Special

        """
        roll = random.randint(1, 100)
        if roll <= 12:
            return 'Creatures'
        elif roll <= 70:
            return 'Containers'
        elif roll <= 73:
            return 'Empty'
        elif roll <= 90:
            return 'Treasure'
        else:
            return 'Special'

