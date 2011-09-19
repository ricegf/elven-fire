import random
import math

from elvenfire.creatures import CreatureError


def StDmg(ST):
    if ST < 8: return 0.5
    elif ST < 11: return 1.0
    elif ST < 17: return 1.0 + (ST-10) / 2
    elif ST < 25: return 4.0 + math.ceil((ST-16) / 2) / 2
    elif ST < 31: return 6.0 + math.ceil((ST-24) / 3) / 2
    else: return 7.0 + math.ceil((ST-30) / 5) / 2


class StatSet:

    """A set of statistics for a creature.

    Attributes:
      baseST, baseDX, baseIQ -- starting stats for this creature type
      maxplus                -- the maximum number of additional attributes
      pluspoints             -- the actual number of additional attributes
      ST, DX, IQ             -- actual stats for this creature
      hits                   -- the number of hits absorbed by skin/armor
      damage                 -- a list of DCl values, one per attack
      altdamage              -- a list of DCl values, one per missile attack
      poison                 -- total DCl value of poison on regular damage
      altpoison              -- total DCl value of poison on missile damage

    Public Methods:
      StatSet()  -- initialize and generate random level, ST, DX, and IQ
      power()    -- calculate and return the creature's power
      points()   -- return ST + DX + IQ
      level()    -- calculate and return the creature's "effective level",
                    the number of times they generated enough experience to
                    level up (using 2x per attribute over 2*base, etc)

    """

    def __init__(self, baseST, baseDX, baseIQ, maxplus, hits, damage,
                       poison=0, altdamage=None, altpoison=0, MA=10,
                       randomize=True):
        self.baseST = baseST
        self.baseDX = baseDX
        self.baseIQ = baseIQ
        self.maxplus = maxplus
        self.hits = hits
        self.damage = damage
        self.poison = poison
        self.altdamage = altdamage if altdamage is not None else []
        self.altpoison = altpoison
        self.MA = MA
        if randomize:
            self.randomstats()

    def _randomplus(self):
        """Return a random number between 0 and self.maxplus."""
        if self.maxplus == 0:
            return 0
        return int(random.triangular(0, self.maxplus, .25 * self.maxplus))

    def randomstats(self, pluspoints=None, statweights=None):
        """Set self.ST, self.DX, and self.IQ semi-randomly."""
        self.pluspoints = pluspoints
        if self.pluspoints is None:
            self.pluspoints = self._randomplus()

        if statweights is None:
            statweights = (25, 5, 1)

        stats = [self.baseST, self.baseDX, self.baseIQ]
        for i in range(self.pluspoints):
            stat = random.choice([0] * statweights[0] + 
                                 [1] * statweights[1] + 
                                 [2] * statweights[2])
            stats[stat] += 1
        (self.ST, self.DX, self.IQ) = stats

    def enforcemaxIQ(self, max):
        while self.IQ > max:
            if random.random() < 0.5:
                self.ST += 1
            else:
                self.DX += 1
            self.IQ -= 1
        

    def points(self):
        """Return ST + DX + IQ total."""
        return self.ST + self.DX + self.IQ

    def _translate(self, dmg):
        """Return specified damage as a number."""
        if isinstance(dmg, int) or isinstance(dmg, float):
            return dmg
        if dmg.startswith('StD'):
            base = StDmg(self.ST)
            i = dmg.find('+')
            if i != -1:
                base += float(dmg[i+1:])
            return base
        raise CreatureError('Cannot translate damage "%s"' % dmg)

    def _translatedamage(self):
        """Translate any 'StD+3' entries to float."""
        for i, dmg in enumerate(self.damage):
            self.damage[i] = self._translate(dmg)
        for i, dmg in enumerate(self.altdamage):
            self.altdamage[i] = self._translate(dmg)

    def power(self):
        """Calculate and return the power of this creature."""
        self._translatedamage()
        # Offensive Combat Power
        OCP = (3 * (sum(self.damage) + self.poison) + 
               (sum(self.altdamage) + self.altpoison)) / 4
        # Defensive Combat Power
        DCP = self.hits + self.ST / 4
        # Final Combat Power
        return math.sqrt(OCP**2 + DCP**2)

    def level(self):
        """Calculate the "effective level" of the creature."""
        level = 0
        bases = (self.baseST, self.baseDX, self.baseIQ)
        stats = (self.ST, self.DX, self.IQ)
        for base, now in zip(bases, stats):
            over = now - base
            while over > 0:
                level += over
                over -= base
        return level

    def __str__(self):
        if isinstance(self.damage, str) or '__iter__' not in dir(self.damage):
            dmgstr = str(self.damage)
        else:
            dmgstr = ', '.join(map(str, self.damage))
        val = "ST: %s DX: %s IQ: %s MA: %s Hit: %s" % (self.ST, self.DX,
                                                       self.IQ, self.MA,
                                                       self.hits)
        val += " Dam: %s" % dmgstr
        if self.poison:
            val += ' + %s psn' % self.poison
        if self.altdamage:
            dmgstr = ', '.join(map(str, self.altdamage))
            val += " Miss: %s" % dmgstr
            if self.altpoison:
                val += ' + %s psn' % self.altpoison
        return val
                

class Creature:

    """Base creature class, containing only the name, stats, and details."""

    def __init__(self, name, stats, details=''):
        self.name = name
        self.stats = stats
        self.details = details

    def power(self):
        """Calculate and return the power of this creature."""
        return self.stats.power()

    def __str__(self):
        val = "%s  %s" % (self.name, self.stats)
        if self.details:
            val += "\n\n%s" % self.details
        return val


