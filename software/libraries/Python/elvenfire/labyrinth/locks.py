import random

from elvenfire import bonus5
from elvenfire.labyrinth import s


class Lock:

    """A lock, with all necessary die rolls for interaction."""

    def __init__(self, level):
        """Determine picklevel, strength, and whether the key is present."""
        self.picklevel = 1 + bonus5(level) + bonus5(level)
        exponent = 1.0 + 3.0 * random.random()
        self.strength = int(6.0 + (level + 1)**exponent)
        self.keyhere = (random.randint(1,50) == 1)

    def __str__(self):
        """Return a description suitable for explanation to the players."""
        val = "  This lock requires %svIQ to pick" % self.picklevel
        val += " or %s to break open." % s(self.strength, 'hit')
        if self.keyhere:
            val += "\n    Surprisingly, the key is on the floor next to it."
        return val
