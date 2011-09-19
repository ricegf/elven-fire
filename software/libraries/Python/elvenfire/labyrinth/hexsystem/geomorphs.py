
import math

from elvenfire.labyrinth.hexsystem import HexLoc, UPLEFT


# Hex contents (typically indicated by color)
EMPTY = 0  # white or gray
HALLWAY = 1  # yellow
SECRET = 2   # red
ROOM_A = 4   # green
ROOM_B = 8   # blue


class GeomorphHex:

    """A single hex within a Geomorph.

    Attributes:
        type   -- chosen from contents above
        loc    -- HexLocation within the Geomorph
        doors  -- None or bitmask made up of directions containing doors
        secret -- None or bitmask made up of directions containing secret doors

    """

    def __init__(self, loc, type=EMPTY, doors=None, secretdoors=None):
        self.loc = loc
        self.type = type
        self.doors = doors
        self.secret = secretdoors

    def neighbors(self, geomorph):
        """Return a list of neighbor hexes within this geomorph."""
        return [geomorph.hexes[loc] for loc in self.loc.neighbors()
                                    if loc.within(geomorph.size)]

    def getroom(self, geomorph):
        """Return a list of GeomorphHex objects making up a single room.

        That is, the group of contiguous hexes of the same type containing
        self.

        It is assumed that geomorph.seen was initialized to an empty list
        before this function was called on the first hex.

        """
        if self in geomorph.seen: return []  # already counted self!
        hexes = [self]
        geomorph.seen.append(self)
        for n in self.neighbors():
            if n not in geomorph.seen and n.type == self.type:
                hexes += n.getroom(geomorph)
        return hexes

    def _rotatedoors(self, doors, direction):
        """Return doors rotated to specified direction."""
        if doors is not None:
            doors = doors << math.log(direction, 2)
            while doors > UPLEFT:
                doors = doors >> math.log(UPLEFT, 2)
        return doors

    def rotate(self, direction, includeloc=True):
        """Rotate hex such that the side previously UP is now direction.

        If includeloc is True, then the hex will also be rotated around
        (0, 0, 0) to the same direction.

        """
        if includeloc:
            self.loc.rotate(direction)
        self.doors = self._rotatedoors(self.doors, direction)
        self.secret = self._rotatedoors(self.secret, direction)


class Geomorph:

    """A set of hexes defining a portion of a labyrinth map.

    Geomorphs are designed to be interchangeable; any valid geomorph may be
    placed among any other valid geomorphs, at any rotation, to create a
    reasonable labyrinth map.

    To achieve this, valid geomorphs must have a HALLWAY hex in the center
    of each side, and the border hexes may not be of any type other than
    HALLWAY or EMPTY.

    Attributes:
      size  -- integer indicating number of hexes from center to any corner
      hexes -- map (HexLoc : GeomorphHex) of all contents
      seen  -- array used only when gathering room information

    """

    def __init__(self, size=5):

        self.size = size
        self.hexes = {}
        self.seen = []

        # Initialize all hexes to EMPTY
        for b in range(-size, size + 1):
            max = (size - b) if b >= 0 else size
            self._inithex(HexLoc(0, b, 0))
            for x in range(1, max + 1):
                self._inithex(HexLoc(x, b, 0))
                self._inithex(HexLoc(0, b, x))

        # Place HALLWAY hexes on each edge
        for hex in self.edgehexes():
            hex.type = HALLWAY

    def _inithex(self, loc):
        hex = GeomorphHex(loc)
        self.hexes[loc] = hex

    def edgehexes(self):
        """Return normalized list of hexes marking the center of each edge."""
        halfsize = int(self.size / 2)
        bighalf = self.size - halfsize  # bighalf == halfsize for even sizes
        locs = [HexLoc(bighalf, halfsize, 0),     # up & left
                HexLoc(0, bighalf, halfsize),     # up & right
                HexLoc(0, -halfsize, self.size),  # right
                HexLoc(0, -self.size, bighalf),   # down & right
                HexLoc(halfsize, -self.size, 0),  # down & left
                HexLoc(self.size, -bighalf, 0)]   # left
        return [self.hexes[L] for L in locs]

    def rotate(self, direction):
        """Rotate entire Geomorph such that what was UP is now direction."""
        oldhexes = self.hexes
        self.hexes = {}
        for hex in oldhexes.values():
            hex.rotate(direction)
            self.hexes[hex.loc] = hex

    def roomlist(self, type=ROOM_A|ROOM_B):
        """Return a list of arrays of hexes, where each array is a room."""
        self.seen = []
        rooms = []
        for hex in self.hexes.values():
            if hex.type & type and hex not in self.seen:
                rooms.append(hex.getroom(self))
        return rooms