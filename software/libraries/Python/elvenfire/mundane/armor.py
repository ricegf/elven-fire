import random

from elvenfire.utilities import wrapped
from elvenfire.mundane import ItemError

class MundaneArmor:

    """Armor or shield, with no special enhancements.

    Class attributes:
      armortypes  -- list of all available armor types
      shieldtypes -- list of all available shields
      wearers     -- list of available armor shapes (e.g. 'Mount')

    """

    armortypes = ['Cloth Armor', 'Fine Plate Armor', 'Leather Armor', 
                  'Chainmail', 'Scale Armor', 'Half-plate Armor', 'Plate Armor']

    shieldtypes = ['Spike Shield', 'Tower Shield', 'Main-Gauche',
                   'Small Shield', 'Large Shield']

    #                                    Ht  Dx  MA  Wt  Cost  Details
    #                                    --  --  --  --  ----  -------
    lookuptypes = {'Cloth Armor'      : ( 1,  1,  0,  7,   50, ''),
                   'Leather Armor'    : ( 2,  2, 20,  8,  100, ''),
                   'Chainmail'        : ( 3,  3, 40, 15,  200, ''),
                   'Scale Armor'      : ( 3,  4, 40, 15,  250, '4 vs blunt weapon attacks, 3 vs all other'),
                   'Half-plate Armor' : ( 4,  5, 40, 20,  300, ''),
                   'Plate Armor'      : ( 5,  6, 40, 25,  500, ''),
                   'Fine Plate Armor' : ( 6,  4, 40, 25, 5000, 'must be custom-fit to wearer'),
                   'Small Shield'     : ( 1,  0,  0,  5,   30, ''),
                   'Spike Shield'     : ( 1,  0,  0,  6,   40, 'DCl 1.5 as weapon'),
                   'Large Shield'     : ( 2,  1,  0, 10,   50, ''),
                   'Tower Shield'     : ( 3,  2,  0, 15,   70, 'Can set in ground (requires 1 round), then treat as wall hex'),
                   'Main-Gauche'      : ( 0,  0,  0, 0.3,  20, 'Used in off-hand as extra attack (DCl StD+3) or to put attacker at Dx-1'),
                  }

    wearers = ['Character', 'Mount']

    def __init__(self, type=None, wearer=None):
        self.type = type
        self.wearer = wearer
        self._settype()
        self._lookuptype()

    def __str__(self):
        val = "%-20s  HT: %s  DX-%s  MA-%2s%%" % (self.name, self.hit, self.DX,
                                                  self.MA)
        if self.desc:
            val += "\n" + wrapped("   " + self.desc, indent=3)
        return val

    def _settype(self):

        # Determine/validate type
        if self.type is None:
            armor = self.armortypes[:2] + 2 * self.armortypes[2:]  # set odds
            shield = self.shieldtypes[:3] + 2 * self.shieldtypes[3:]
            if self.wearer is None:
                self.type = random.choice(armor + shield)
            else:
                self.type = random.choice(armor)
        elif self.type not in (self.armortypes + self.shieldtypes):
            raise ItemError('Unrecognized armor/shield type: %s' % 
                            self.type)

        # Determine/validate armor wearer
        if self.type in self.armortypes:
            if self.wearer is None:
                roll = random.randint(1, 6)
                self.wearer = self.wearers[0] if roll > 1 else self.wearers[1]
            elif self.wearer not in self.wearers:
                raise ItemError('Unrecognized armor wearer: %s' %
                                self.wearer)
        elif self.wearer is not None and self.wearer != 'Character':
            raise ItemError('Shields cannot be used by %ss!' % self.wearer)

        # Update information
        self.name = self.type
        if self.wearer == 'Mount':
            self.name += ' (%s)' % self.wearer

    def _lookuptype(self):
        if self.type not in self.lookuptypes:
            raise ItemError("%s has not been fully defined!" % self.type)
        (self.hit, self.DX, self.MA, self.weight, 
         self.cost, self.desc) = self.lookuptypes[self.type]
