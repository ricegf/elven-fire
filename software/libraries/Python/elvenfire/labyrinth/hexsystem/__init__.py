import math

# Directions, based on sides of a hexagon
UP = 0
UPRIGHT = 1
DOWNRIGHT = 2
DOWN = 4
DOWNLEFT = 8
UPLEFT = 16


class HexLoc:

    """An (a, b, c) location in terms of hexes.

    a is considered "up and to the left", b is "up", and c is "up and to the
    right".  Once normalized, either a or c must be equal to zero, and the
    other a non-negative integer.  b can be any valid integer.

    """

    def __init__(self, a, b, c, normalize=False):
        self.a = a
        self.b = b
        self.c = c
        if normalize:
            self.normalize()

    def __eq__(self, other):
        """Return boolean indicating if self and other share a location."""
        normal_self = self.normalized()
        normal_other = other.normalized()
        return (normal_self.a == normal_other.a and
                normal_self.b == normal_other.b and
                normal_self.c == normal_other.c)

    def __hash__(self):
        (a, b, c) = self._normalize()
        return hash(a * 1000) & hash(b * 100) & hash(c * 10)

    def __repr__(self):
        return "HexLoc(%s, %s, %s)" % (self.a, self.b, self.c)

    def __str__(self):
        return repr(self)

    def xy(self, size=10):
        """Return location as (x, y) values."""
        (a, b, c) = self._normalize()
        height = math.sin(math.radians(60)) * size * 2  # edge to edge
        x = size * 1.5 * (c - a)  # (c * math.sqrt(3) - a * math.sqrt(3))
        y = height * (b + a / 2 + c / 2)
        return (x, y)

    ## Normalization ##

    def _positize(self, a=None, b=None, c=None):
        """Return (a, b, c) such that a >= 0 and c >= 0."""
        if a is None: a = self.a
        if b is None: b = self.b
        if c is None: c = self.c
        if a < 0 or c < 0:
            diff = min(a, c)
            a += diff
            c += diff
            b -= diff
        return (a, b, c)

    def _normalize(self, a=None, b=None, c=None):
        """Return normalized values of (a, b, c)."""
        if a is None: a = self.a
        if b is None: b = self.b
        if c is None: c = self.c
        a_sign = 0 if a == 0 else math.copysign(1, a)  # cmp(a, 0)
        c_sign = 0 if c == 0 else math.copysign(1, c)  # cmp(c, 0)
        if (a_sign == c_sign and a_sign != 0):  # both positive/both negative
            diff = min(a, c)  # By taking the minimum, we get the most
            a -= diff         #   negative or the least positive, thus
            c -= diff         #   guaranteeing that we will end up with
            b += diff         #   0 for either a or c.
        return (a, b, c)

    def normalize(self):
        """Normalize self for easy use and comparison.

        There should be one and only one way to express a normalized location,
        such that:
          a >= 0
          c >= 0
          Either a or c must be zero.

        """
        (self.a, self.b, self.c) = self._normalize()

    def normalized(self):
        """Return a NEW object representing the same place, normalized."""
        return self.__class__(self.a, self.b, self.c, normalize=True)

    ## Relationship to Other Locations ##

    def neighbors(self):
        """Return a tuple of adjacent locations (normalized)."""
        return (self.__class__(self.a, self.b + 1, self.c, True),  # up
                self.__class__(self.a, self.b, self.c + 1, True),  # up & right
                self.__class__(self.a - 1, self.b, self.c, True),  # down & right
                self.__class__(self.a, self.b - 1, self.c, True),  # down
                self.__class__(self.a, self.b, self.c - 1, True),  # down & left
                self.__class__(self.a + 1, self.b, self.c, True))  # up & left

    def within(self, size):
        """Return boolean indicating if self is within geomorph of given size.

        Geomorph is assumed to be centered at (0, 0, 0).

        """
        (a, b, c) = self._normalize()
        if not (-size <= a <= size and
                -size <= b <= size and
                -size <= b <= size):
            return False
        return sum([a, b, c]) <= size

    def rotate(self, direction, normalize=True):
        """Rotate self around (0, 0, 0)."""
        if direction & (UPRIGHT | DOWNLEFT):
            (self.a, self.b, self.c) = (self.c, self.a, self.b)
        elif direction & (UPLEFT | DOWNRIGHT):
            (self.a, self.b, self.c) = (self.b, self.c, self.a)
        if direction & (DOWN | DOWNLEFT | DOWNRIGHT):
            (self.a, self.b, self.c) = (-self.a, -self.b, -self.c)
        if normalize:
            self.normalize()

    def hexpoints(self, hexsize=10):
        """Return a list of seven (x, y) pairs representing the corners.
 
        The first pair in the list represents the left side of the top edge.
        Subsequent pairs progress clockwise, and the final pair is a duplicate
        of the first.
 
        hexsize is the 'radius' of the hexagon - the distance from the center
        to any corner.  Due to equilateral triangle rules, this is equal to
        the length of any side.
 
        """
 
        (xcenter, ycenter) = self.xy(hexsize)
        toedge = math.tan(math.radians(60)) * (hexsize / 2)  # distance from center to edge
 
        return [(xcenter - hexsize / 2, ycenter + toedge),  # topleft
                (xcenter + hexsize / 2, ycenter + toedge),  # topright
                (xcenter + hexsize, ycenter),               # right
                (xcenter + hexsize / 2, ycenter - toedge),  # bottomright
                (xcenter - hexsize / 2, ycenter - toedge),  # bottomleft
                (xcenter - hexsize, ycenter),               # left
                (xcenter - hexsize / 2, ycenter + toedge)]  # topleft

