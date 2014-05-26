import random
import math

from elvenfire import bonus5
from elvenfire.labyrinth import s, ea
from elvenfire.labyrinth.traps import Trap
from elvenfire.labyrinth.locks import Lock


class ContainerSet:

    """A set of one or more container(s) of a single type."""

    def __init__(self, level, num=None):
        """Determine number and type of container(s)."""
        self.num = num
        if self.num is None:
            self.num = int(4 - math.sqrt(random.uniform(0, 16))) + 1
        type = random.randint(1, 100)

        # Double number of containers on 100
        while type == 100:
            self.num *= 2
            type = random.randint(1, 100)

        if type <= 4:
            self.desc = "%s on the floor" % s(self.num, 'bag')
            self.percentage = 15
            self.containers = [Bag(i, level) for i in range(self.num)]
        elif type <= 10:
            self.desc = "%s hanging on the wall" % s(self.num, 'bag')
            self.percentage = 25
            self.containers = [Bag(i, level) for i in range(self.num)]
        elif type <= 13:
            self.desc = s(self.num, 'unlocked coffer')
            self.percentage = 60
            self.containers = [Coffer(i, level, 
                                      locked=False) for i in range(self.num)]
        elif type <= 20:
            self.desc = s(self.num, 'locked coffer')
            self.percentage = 60
            self.containers = [Coffer(i, level, 
                                      locked=True) for i in range(self.num)]
        elif type <= 23:
            self.desc = s(self.num, 'open wooden chest')
            self.percentage = 80
            self.containers = [Chest(i, level, type="wooden", 
                                     locked=False) for i in range(self.num)]
        elif type <= 27:
            self.desc = s(self.num, 'unlocked wooden chest')
            self.percentage = 75
            self.containers = [Chest(i, level, type="wooden", 
                                     locked=False) for i in range(self.num)]
        elif type <= 35:
            self.desc = s(self.num, 'locked wooden chest')
            self.percentage = 75
            self.containers = [Chest(i, level, type="wooden", 
                                     locked=True) for i in range(self.num)]
        elif type <= 38:
            self.desc = s(self.num, 'open iron chest')
            self.percentage = 90
            self.containers = [Chest(i, level, type="iron", 
                                     locked=False) for i in range(self.num)]
        elif type <= 41:
            self.desc = s(self.num, 'unlocked iron chest')
            self.percentage = 85
            self.containers = [Chest(i, level, type="iron", 
                                     locked=False) for i in range(self.num)]
        elif type <= 60:
            self.desc = s(self.num, 'locked iron chest')
            self.percentage = 80
            self.containers = [Chest(i, level, type="iron", 
                                     locked=True) for i in range(self.num)]
        elif type <= 92:
            haslid = random.randint(1, 10) > 7
            if haslid:
                lidtext = "lid"
            else:
                lidtext = "no lid"
            style = random.choice(('ceramic pot', 'metal urn', 'stone jar'))
            self.desc = "%s with %s" % (s(self.num, style), lidtext)
            self.percentage = 50 if haslid else 60
            self.containers = [Pot(i, level, type=style, 
                                   lid=haslid) for i in range(self.num)]
        else:
            if num is None:
                self.num = bonus5(level)  # few unguarded treasures...
            self.desc = "%s lying invitingly on the floor" % \
                        s(self.num, 'treasure')
            self.percentage = 20
            self.containers = [UnguardedTreasure(i, level, locked=False)
                               for i in range(self.num)]

    def __str__(self):
        """Return a description suitable for explanation to the players."""
        val = "You see %s" % self.desc
        val += " (%s%% chance of trap%s)\n" % (self.percentage, ea(self.num))
        val += "\n".join(map(str, self.containers))
        return val

    def determine_traps(self):
        """Determine whether each container is in fact trapped.

        This will typically be done during gameplay based on the listed
        percentages.  However, this method may be used to pre-determine traps
        if so desired.

        """
        for container in self.containers:
            roll = random.randint(1, 100)
            container.is_trapped = (roll <= self.percentage)


class Container:

    """Abstract class for single containers."""

    def __init__(self, num, level, getlock=False, gettrap=True):
        self.num = num
        self.name = "Container"
        self.trap = None
        self.is_trapped = None  # None indicates nondeterminate (must roll)
        if gettrap:
            self.trap = Trap.newtrap(level)
        self.lock = None
        if getlock:
            self.lock = Lock(level)
        self.strength = None
        self.num_treasures = None

    def __str__(self):
        """Return a description suitable for explanation to the players."""
        val = "%s %s" % (self.name, self.num+1)
        if self.strength is not None:
            val += " requires %s to smash" % s(self.strength, 'hit')
        if self.strength is not None and self.num_treasures is not None:
            val += " and"
        if self.num_treasures is not None:
            val += " contains %s" % s(self.num_treasures, 'treasure')
        if self.lock is not None:
            val += "\n" + str(self.lock)
        if self.is_trapped == True:
            val += "\n%s %s is trapped!" % (self.name, self.num)
        elif self.is_trapped == False:
            val += "\n%s %s is not trapped." % (self.name, self.num)
            self.trap = None
        if self.trap is not None:
            val += "\n" + str(self.trap)
        return val


class Bag (Container):

    def __init__(self, num, level):
        Container.__init__(self, num, level)
        self.name = "Bag"
        self.num_treasures = 1


class Coffer (Container):

    def __init__(self, num, level, locked):
        Container.__init__(self, num, level, getlock=locked)
        self.name = "Coffer"
        self.strength = (40 * level) + random.randint(1, 20 * level)
        self.num_treasures = random.randint(level, level + 1)


class Chest (Container):

    def __init__(self, num, level, type, locked):
        Container.__init__(self, num, level, getlock=locked)
        self.name = "Chest"
        if type == 'wooden':
            self.strength = (20 * level) + random.randint(1, 5 * level)
            self.num_treasures = random.randint(level, level + 3)
        elif type == 'iron':
            self.strength = (60 * level) + random.randint(1, 30 * level)
            self.num_treasures = random.randint(level, level + 5)
        else:
            raise '%s chest not implemented!' % type


class Pot (Container):

    def __init__(self, num, level, type, lid):
        Container.__init__(self, num, level)
        self.name = type.rsplit(' ')[0].capitalize()  # last word only
        if type == 'ceramic pot':
            self.strength = random.randint(1, 4 * level)
        elif type == 'metal urn':
            self.strength = 10 + random.randint(1, 8 * level)
        elif type == 'stone jar':
            self.strength = 20 + random.randint(1, 12 * level)
        else:
            raise "'%s' type of Pot not implemented!" % type
        self.num_treasures = random.randint(1, 2);


class UnguardedTreasure (Container):

    def __init__(self, num, level, locked):
        Container.__init__(self, num, level, getlock=locked)
        self.name = "Unguarded Treasure"
        self.num_treasures = 1

    def __str__(self):
        """Return a description suitable for explanation to the players."""
        if self.lock is None:
            val = "Treasure %s is not locked." % (self.num + 1)
        else:
            val = "Treasure %s is locked!" % (self.num + 1)
            val += "\n" + str(self.lock)
        val += "\n" + str(self.trap)
        return val

