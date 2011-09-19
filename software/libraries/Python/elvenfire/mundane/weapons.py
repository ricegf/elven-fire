import random

from elvenfire.utilities import wrapped
from elvenfire.mundane import ItemError

class MundaneWeapon:

    """A weapon with no special enhancements.

    Class attributes:
      stylelist    -- all available styles (e.g. 'Sword')
      pseudostyles -- are interpreted as styles by weaponlist(), but never
                      appear as the .style attribute

    New attributes:
      type       -- the specific type of this weapon (e.g. 'Broadsword')
      style      -- the style of this weapon (e.g. 'Sword')
      twohanded  -- boolean indicating if this is a two-handed weapon
      throwable  -- boolean indicating if this weapon can be thrown
      crushing   -- boolean indicating if this is a crushing weapon
      hand2hand  -- boolean indicating if this weapon can be used in HTH

    New public methods:
      weaponlist(style) -- all available weapons of that style
      isdistance()      -- boolean indicating if weapon can be used from afar

    """

    stylelist = ['Sword', 'Ax/Mace/Hammer', 'Drawn Bow', 'Cross Bow',
                 'Pole Weapon', 'Unusual Weapon']

    pseudostyles = ['Missile Weapon', 'Two-Handed', 'Thrown Weapon',
                    'Hand-to-Hand', 'Crushing']

    weaponlistings = [
    #        Name                 Class             ST  DCl     2Hand  Throw  Crush  HTH    Description
    #        -------------------  ----------------  --  ------  -----  -----  -----  -----  -----------------------------
            ('Grobes Messer',     'Sword',           0, 'StD+3', False, True,  False, True,  'Breaks on 3d6 = 18 or 17; drop on 16; +3 damage in HTH'),
            ('Dagger',            'Sword',           0, 'StD+3', False, True,  False, True,  '+3 damage in HTH'),
            ('Misericorde',       'Sword',           0, 'StD+3', False, True,  False, True,  'Breaks on 3d6 = 18 or 17; +6 damage in HTH vs chain or plate mail, +3 otherwise'),
            ('Dirk',              'Sword',           8,  3.5,    False, True,  False, False, 'Dx+1 when thrown'),
            ('Rapier',            'Sword',           9,  3.5,    False, False, False, False, ''),
            ('Anelace',           'Sword',           9,  4.0,    False, False, False, False, 'Long dagger'),
            ('Cutlass',           'Sword',          10,  5.0,    False, False, False, False, ''),
            ('Matchet',           'Sword',          11,  5.5,    False, False, False, False, 'Does 7 against plants and HIT=0 targets'),
            ('Shortsword',        'Sword',          11,  6.0,    False, False, False, False, ''),
            ('Broadsword',        'Sword',          12,  7.0,    False, False, False, False, ''),
            ('Cladibas',          'Sword',          13,  8.0,    False, False, False, False, ''),
            ('Cladibas',          'Sword',          13,  8.5,    True,  False, False, False, ''),
            ('Two Handed Sword',  'Sword',          14,  9.5,    True,  False, False, False, ''),
            ('Great Sword',       'Sword',          16, 11.5,    True,  False, False, False, ''),
            ('Club',              'Ax/Mace/Hammer',  0, 'StD+3', False, True,  True,  False, ''),
            ('Club',              'Ax/Mace/Hammer',  0, 'StD+4', True,  False, True,  False, ''),
            ('Hurlbat',           'Ax/Mace/Hammer',  9,  4.5,    False, True,  False, False, 'Thrown only; all streel throwing axe'),
            ('Hatchet',           'Ax/Mace/Hammer',  9,  3.5,    False, True,  False, False, ''),
            ('Doloire Hand Axe',  'Ax/Mace/Hammer', 10,  4.0,    False, True,  True,  False, 'Crush (3.5) with one side, cut (4) with other'),
            ('Hammer',            'Ax/Mace/Hammer', 10,  4.5,    False, True,  True,  False, ''),
            ('Francisca Th. Axe', 'Ax/Mace/Hammer', 11,  5.0,    False, True,  False, False, "Melee (5) or thrown (6.5); if thrown, 3vDx or target's shield is smashed"),
            ('Mace',              'Ax/Mace/Hammer', 11,  6.0,    False, True,  True,  False, ''),
            ('Small Ax',          'Ax/Mace/Hammer', 11,  5.5,    False, True,  False, False, ''),
            ('Military Pick',     'Ax/Mace/Hammer', 12,  7.0,    False, False, False, False, ''),
            ('Doloire Axe',       'Ax/Mace/Hammer', 13,  7.5,    True,  False, True,  False, 'Crush (7) with one side, cut (7.5) with other'),
            ('Morning Star',      'Ax/Mace/Hammer', 13,  8.0,    False, False, True,  False, ''),
            ('Great Hammer',      'Ax/Mace/Hammer', 14,  9.0,    True,  False, True,  False, ''),
            ('Battle Ax',         'Ax/Mace/Hammer', 15, 10.5,    True,  False, False, False, ''),
            ('Sling',             'Drawn Bow',       0,  1.5,    False, False, True,  False, ''),
            ('Small Bow',         'Drawn Bow',       9,  2.5,    True,  False, False, False, 'Additional arrow/round for each 5 adjDx above 10'),
            ('Horse Bow',         'Drawn Bow',      10,  3.5,    True,  False, False, False, 'Additional arrow/round for each 5 adjDx above 11'),
            ('Long Bow',          'Drawn Bow',      11,  5.5,    True,  False, False, False, 'Additional arrow/round for each 5 adjDx above 13; mounting the box requires one turn but gives Dx+2'),
            ('Recurve Bow',       'Drawn Bow',      12,  6.0,    True,  False, False, False, 'Additional arrow/round for each 4 adjDx above 13; Dx+1 on horseback; breaks on 3d6 = 17 or 18'),
            ('Light Crossbow',    'Cross Bow',      12,  7.0,    True,  False, False, False, '1/round if adjDx = 14 or greater; else half/round'),
            ('Dbl Light Crossbow','Cross Bow',      12,  7.0,    True,  False, False, False, '2/round if adjDx = 15 or greater; twice the reload time'),
            ('Heavy Crossbow',    'Cross Bow',      15, 10.5,    True,  False, False, False, '1/round if adjDx = 16 or greater; else half/round'),
            ('Dbl Heavy Crossbow','Cross Bow',      15, 10.5,    True,  False, False, False, '2/round if adjDx = 15 or greater; twice the reload time'),
            ('Scorpio',           'Cross Bow',      16, 13.0,    True,  False, False, False, 'half/round if adjDx = 14 or greater; else third/round; breaks on 3d6 = 18 or 17'), 
            ('Arbalest',          'Cross Bow',      18, 21.0,    True,  False, False, False, 'third/round if adjDx = 16 or greater; else fourth/round; breaks on 3d6 = 18 or 17'), 
            ('Javelin',           'Pole Weapon',     9,  2.5,    False, True,  False, False, ''),
            ('Plancon a picot',   'Pole Weapon',     9,  3.0,    True,  False, False, False, 'Spike on a bat'),
            ('Trident',           'Pole Weapon',    10,  3.5,    False, True,  False, False, 'Usually used with a net'), ##
            ('Spetum',            'Pole Weapon',    10,  3.5,    True,  False, False, False, 'Triple damage on 3d6 = 3 or 4; double on 5'),
            ('Spear',             'Pole Weapon',    11,  3.5,    False, True,  False, False, ''),
            ('Spear',             'Pole Weapon',    11,  4.5,    True,  False, False, False, ''),
            ('Ranseur',           'Pole Weapon',    11,  4.0,    True,  False, False, False, 'Disarm opponent on 3d6 = 3, 4, or 5'),
            ('Military Fork',     'Pole Weapon',    12,  4.5,    False, True,  False, False, '2-pronged, useful for raising poles; throw as a large spear'),
            ('Military Fork',     'Pole Weapon',    12,  5.5,    True,  False, False, False, '2-pronged, useful for raising poles; throw as a large spear'),
            ('Spear Thrower',     'Pole Weapon',    11,    0,    True,  False, False, False, 'Dx+4; +2 to damage with Javelin or Spear; may be used as a club'),
            ('Naginata',          'Pole Weapon',    10,  5.5,    True,  False, False, False, ''),
            ('Mattock',           'Pole Weapon',    12,  6.5,    True,  False, False, False, ''),
            ('Halberd',           'Pole Weapon',    13,  7.0,    True,  False, False, False, '3vDx or target horseman is unmounted'),
            ('Pike',              'Pole Weapon',    12,  8.0,    True,  False, False, False, '5 meters; usually used against horse; must be charged to use'),
            ('Pike Ax',           'Pole Weapon',    15,  9.0,    True,  False, False, False, ''),
            ('Calvary Lance',     'Pole Weapon',    13,  9.5,    False, False, False, False, '3.5-4.5 meters; requires horse; must charge or be charged to use'),
            ('Net',               'Unusual Weapon', 10, 'StD+3', False, False, False, False, 'Used with trident; thrown it entangles target (0.5 DCl/round), target falls, must make 3vDx to get free; net can be cut (St is 5)'), ##
            ('Boomerang',         'Unusual Weapon', 11,  7.0,    False, False, False, False, 'Does not return; thrown, but treat range like missile weapon'),
            ('Bola',              'Unusual Weapon',  9,  5.5,    False, False, False, False, 'Thrown - select target: Head (DCl 5.5, Dx-4, may not attack for one turn, flying creature crash-lands); Wings (flying creature falls, taking DCl 3.5, may fly again if target has hands or ST>20); Arms (drop weapon/shield for 2 turns); Legs (trip for 2 turns)'),
            ('Sha-Ken',           'Unusual Weapon',  0,  1.5,    False, False, False, False, 'May use Marksmanship rules; may throw 2-3 (Dx-2), 4-6 (Dx-4), 7-9 (Dx-6), 10-12 (Dx-8); 50% chance to break when hit wall'), ##
            ('Cestus',            'Unusual Weapon',  0, 'StD+3', False, False, False, False, 'Worn like a glove (cannot be dropped); may use two at Dx-3 (but only one in HTH)'),
            ('Quarterstaff',      'Unusual Weapon', 11,  5.5,    False, False, False, False, "May attack opponent's weapon at Dx-4; if hit, opponent must make 3vDx or drop"),
            ('Lasso',             'Unusual Weapon',  8,  5.5,    False, False, False, False, 'Range 3-15 hexes (use missile ranges); 6 turns to recoil if miss; if hit, select head (DCl 5.5), arm (drop weapon/shield), or body (trip); requires 3vDx to free IF target has hands or ST>20; lassoing a flying creature requires Dx-4'),
            ('Whip',              'Unusual Weapon',  8,  2.5,    False, False, False, False, 'Range 3-5 hexes only; may use Marksmanship rules, or use like lasso'),
            ('Nunchucks',         'Unusual Weapon',  8,  4.5,    False, False, False, False, 'May strike twice at Dx-4'),
            ('Blowgun',           'Unusual Weapon',  0,    0,    False, False, False, False, 'Dx-6 against plate armor, Dx-4 against any other armor; damage depends on poison; treat as thrown weapon')]

    def __init__(self, style=None, type=None, maxST=None):
        self._setweapontype(style, type, maxST)

    def __str__(self):
        val = self.type
        if self.twohanded: val += '#'
        if self.throwable: val += '*'
        if self.crushing:  val += '&'
        val = "%-20s DCl: %s" % (val, self.DCl)
        if self.desc:
            val += "\n" + wrapped("   " + self.desc, indent=3)
        return val

    def weaponlist(style=None):
        """Return a list of weapons matching the specified style."""
        return [i[0] for i in MundaneWeapon._longweaponlist(style)]

    def isdistance(self):
        """Return boolean indicating if this weapon is usable at a distance."""
        return ('Bow' in self.style or self.throwable)

    def _longweaponlist(style, maxST=None):
        if maxST is None: maxST = 99
        list = []
        for listing in MundaneWeapon.weaponlistings:
            (type, style_, maxST_, DCl, twohand, throw, crush, HTH, desc) = listing
            if ((style is None or style == style_) or
                (style == 'Two-Handed' and twohand) or
                (style == 'Thrown Weapon' and throw) or
                (style == 'Hand-to-Hand' and HTH) or
                (style == 'Crushing' and crush) or
                (style == 'Missile Weapon' and (style_ == 'Drawn Bow' or
                                                style_ == 'Cross Bow'))):
                if maxST >= maxST_:
                    list.append(listing)
        if not list:
            raise ItemError("No weapons found for style '%s'" % style)
        return list

    def _setweapontype(self, style=None, type=None, maxST=None):

        """Determine weapon type and set all relevant attributes."""

        if type is not None and type.startswith('Sha-Ken'):
            self.numstr = type[7:]
            type = type[:7]

        # Select weapon listing
        longlist = MundaneWeapon._longweaponlist(style, maxST)
        if type is None:
            listing = random.choice(longlist)
        else:
            for weapon in longlist:
                if weapon[0] == type or ('+' in type and weapon[0] in type):
                    listing = weapon
                    break
            else:
                msg = "No '%s' weapon found" % type
                if style is not None:
                    msg += " for style '%s'" % style
                raise ItemError(msg)

        # Gather information
        (self.type, self.style) = listing[:2]
        (self.reqST, self.DCl) = listing[2:4]
        (self.twohanded, self.throwable, self.crushing, 
         self.hand2hand) = listing[4:8]
        self.desc = listing[8]

        # Handle special cases
        if self.type == 'Trident' or self.type == 'Net':
            if ((type is not None and '+' in type) or
                random.randint(1, 4) <= 3):
                self.type = 'Trident [+ Net]'
        elif self.type == 'Sha-Ken':
            if 'numstr' in dir(self):
                self.type += ' %s' % self.numstr
            else:
                self.type += ' (%s)' % random.randint(1, 12)

