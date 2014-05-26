
import random

from elvenfire import ELFError


class AbilityError (ELFError):
    pass


class _Ability:

    """Abstract class: an ability consisting of a name and an ability cost

    Attributes:
      self.name   -- name of Ability
      self.desc   -- (optional) long-hand description of the Ability
      self.AC     -- final AC of this Ability

    To implement, define the following:
      _randomize() -- randomly select and set self.name (by default, will
                      choose randomly from self.typelist, if it exists)
      _lookup()    -- set self.AC (and optionally self.desc) based on
                      the current value of self.name

    """

    def __init__(self, name=None):
        self.name = name
        if self.name is None:
            self._randomize()
        elif 'typelist' in dir(self):
            if self.name not in self.typelist:
                raise AbilityError("Invalid ability name '%s'" % self.name)
        self._lookup()

    def _randomize(self):
        """Set self.name to a random ability."""
        if 'typelist' in dir(self):
            self.name = random.choice(self.typelist)
        else:
            raise NotImplementedError()

    def _lookup(self):
        """Set self.desc and self.AC based on self.name."""
        raise NotImplementedError()

    def __str__(self):
        """Return name of ability."""
        return self.name

    def description(self):
        """Return a long-hand description of the ability."""
        if 'desc' in dir(self):
            return self.desc
        return str(self)

    def __cmp__(self, other):
        """Sort by self.AC"""
        if self.AC < other.AC:
            return -1
        elif self.AC > other.AC:
            return 1
        else:
            return 0

    def __lt__(self, other):
        return self.AC < other.AC

    def __eq__(self, other):
        return self.name == other.name
        # AC should always match if name does

    # retain hashability - must be implemented to complement __eq__
    def __hash__(self):
        return hash(self.name)

    def duplicate(self, other):
        """Return boolean indicating if Ability name matches.

        For a base-class ability, this will return the same result as the ==
        operator; however, subclasses may alter the implementation.

        To be clear:
          __eq__(other)    -- are the two Ability objects referencing the exact
                              same ability?
          __hash__()       -- implemented to match __eq__, such that two
                              objects that are equal always have the same hash.
          duplicate(other) -- are the two Ability objects functionally
                              equivalent, such that they should not both appear
                              on the same item/character?
          worsethan(other) -- given that other is a duplicate of this Ability,
                              is other "better"?

        """
        return self.name == other.name

    def worsethan(self, other):
        """Return boolean indicating if other is "better" than self.

        Assumes self.duplicate(other) is True.

        For a base-class Ability, this function has no meaning; however,
        subclasses should implement it to complement duplicate(other).

        Return False for equivalent objects.

        """
        return False  # doesn't matter - there is no "better" for duplicates


