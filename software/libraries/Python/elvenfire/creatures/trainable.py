import random

from elvenfire.utilities import wrapped
from elvenfire.creatures import CreatureError
from elvenfire.creatures.basics import Creature, StatSet


class TrainableAnimal (Creature):

    #           Type        Name             ST  DX IQ  ++  Ht Dam          Cost Upk Avl  Details/Notes
    #           ----------- ---------------- --  -- --  --  -- ------------ ---- --- ---  -------------
    animals = [('Ape',      'Baboon',        14, 12, 6, 10, 0, [5.5,],      1500, 15,  3, ''),
               ('Ape',      'Chimp',         14, 12, 7, 11, 0, [4.5,],      5000, 15,  4, ''),
               ('Ape',      'Great',         20, 12, 7, 13, 0, [7.0,],      6000, 20,  3, ''),
               ('Ape',      'Monkey',         2, 13, 5,  6, 0, [2.5,],       230, 10, 12, ''),
               ('Bear',     'Black',         20, 11, 6, 12, 2, [7.0,],      1200, 40, 14, ''),
               ('Bear',     'Cave',          30, 10, 5, 15, 2, [10.0,],      500, 50,  8, '2-hex'),
               ('Bear',     'Kodiak',        30, 11, 6, 12, 2, [9.0,],      1500, 40,  5, ''),
               ('Bird',     'Diatryma',      22, 13, 5, 13, 7, [4.5,],       450, 25,  7, 'May have second attack with DX-4 on both'),
               ( None,      'Camel',         24, 12, 5, 13, 0, [4.5,],       350, 20, 18, '2-hex; bites when rider rolls automatic miss (d4 damage)'),
               ('Cat',      'House',          4, 14, 5,  7, 0, [2.5,],        50,  5, 20, 'DX-3 to hit'),
               ('Cat',      'Jaguar',        12, 14, 6, 10, 1, [4.5,],      1000, 20, 12, ''),
               ('Cat',      'Leopard',       12, 14, 5, 10, 1, [5.5,],       350, 20, 11, 'In HTH, gets second attack (2d4 damage)'),
               ('Cat',      'Lion',          24, 14, 5, 14, 1, [6.5,],       500, 30, 10, '2-hex'),
               ('Cat',      'Sabertooth',    30, 13, 5, 16, 1, [10.5, 7.5],  800, 40,  5, '2-hex'),
               ('Cat',      'Tiger',         24, 15, 6, 15, 1, [7.0,],      1400, 30,  8, '2-hex'),
               ('Dog',      'Typical',        6, 13, 6,  8, 0, [3.5,],       600, 10, 20, ''),
               ('Dog',      'Yapper',         3, 13, 6,  7, 0, [2.5,],       100,  5, 20, ''),
               ('Dog',      'War',           10, 14, 7, 10, 1, [4.5,],      2500, 20, 18, 'No obedience roll when fully trained'),
               ('Dog',      'Blink War',     10, 14, 7, 10, 1, [4.5,],     25000, 20,  2, 'Can teleport (1 ST/MH) and attack in same turn'),
               ( None,      'Donkey',        14, 15, 6, 11, 0, [3.5,],       800, 20, 19, '2-hex; no obedience roll required'),
               ( None,      'Dragonet',       4, 14, 6,  0, 0, [3.5,],      1500, 20,  3, 'price is for an egg; animals not available'),
               ('Elephant', 'Typical',       50, 13, 6, 23, 2, [10.5, 6.5], 2250, 75, 16, '2-hex; 2nd attack is at a range of 2 hexes'),
               ('Elephant', 'War',           40, 13, 7, 20, 2, [12.5,],     8000, 70, 13, '2-hex; no obedience roll when trained, except with fire or rats'),
               ('Horse',    'Draft',         26, 12, 5, 14, 0, [6.5,],       350, 20, 20, '2-hex'),
               ('Horse',    'Light',         22, 13, 5, 13, 0, [3.5,],       400, 20, 20, '2-hex'),
               ('Horse',    'Nag',           14, 11, 5, 10, 0, [3.5,],        50, 20, 20, '2-hex'),
               ('Horse',    'Riding',        22, 12, 5, 13, 0, [4.5,],       450, 20, 19, '2-hex'),
               ('Horse',    'War',           24, 13, 6,  0, 0, [8,],        4000, 30, 13, '2-hex; no obedience roll when trained; loyal to one master (trainer) for life'),
               ( None,      'Indricotherium',40, 12, 5, 19, 2, [10.5,],      800, 90,  7, '8 to 10 hexes'),
               ('Lizard',   'Riding',        20, 13, 5, 12, 2, [8,],         500, 90, 15, '2-hex; bites when rider rolls automatic miss (d4 damage)'),
               ('Lizard',   'Saurian',       30, 11, 5, 15, 3, [7,],         750, 60, 12, '3-hex; d6 bite when rider rolls automatic miss'),
               ('Lizard',   'Walker',        20, 12, 5, 12, 1, [3.5,],       450, 20, 10, '2-hex'),
               ('Lizard',   'War',           25, 13, 6,  0, 3, [9,],        4500, 20, 13, '2-hex; no obedience roll when trained; loyal to one master (trainer) for life'),
               ('Lizard',   'War Chameleon', 24, 13, 6, 14, 3, [9,],        7000, 20,  2, '2-hex; no obedience roll when trained; loyal to one master (trainer) for life;\n DX-4 to hit'),
               ( None,      'Mule',          22, 14, 6, 14, 0, [4.5],        800, 20, 20, '2-hex; no obedience roll in combat; 4vIQ to obey when NOT in combat'),
               ( None,      'Oxen',          30, 11, 5, 15, 1, [7,],         500, 25, 20, '2-hex; especially susceptible to panic (3vIQ)'),
               ( None,      'Pegasus',       22, 13, 6, 13, 0, [4.5,],     12000, 20,  1, '2-hex; can fly; level-headed in a fight'),
               ( None,      'Slinker',        2, 14, 6,  7, 0, [2.5,],       900, 10, 18, 'Stealth 5 ability; DX-3 to hit'),
               ( None,      'Unicorn',       20, 13, 5, 12, 0, [3.5, 5.5], 10000, 20,  1, '2-hex; only ridden by a virgin maiden; 2nd attack is pole weapon'),
               ('Wolf',     'Grey',          10, 14, 6, 10, 1, [4.5,],       600, 10, 20, ''),
               ('Wolf',     'Dire',          16, 12, 5, 11, 1, [7.5,],       800, 10, 18, ''),

               ('Roc',      '3-hex',         32, 12, 5, 16, 2, [5.0],       1350, 80,  2, 'This bird flies normally and attacks by pecking.  Rocs typically like the mountains.'),
               ('Roc',      '4-hex',         40, 12, 5, 19, 2, [7.0],       1450,100,  2, 'This bird flies normally and attacks by pecking.  Rocs typically like the mountains.'),
               ('Roc',      '5-hex',         48, 13, 5, 22, 3, [9.0],       1650,120,  2, 'This bird flies normally and attacks by pecking.  Rocs typically like the mountains.'),
               ('Roc',      '6-hex',         60, 13, 5, 26, 3, [13.0],      1950,150,  2, 'This bird flies normally and attacks by pecking.  Rocs typically like the mountains.'),
               ('Roc',      '7-hex',         74, 13, 5, 30, 3, [17.0],      2450,200,  1, 'This bird flies normally and attacks by pecking.  Rocs typically like the mountains.'),
               ('Roc',      '8-hex',         90, 12, 5, 35, 4, [25.0],      4950,300,  1, 'This bird flies normally and attacks by pecking.  Rocs typically like the mountains.'),
              ]

    def __init__(self, name=None, subtype=None):
        self._getinfo(name, subtype)
        Creature.__init__(self, self.name, self.stats, self.details)

    def _getinfo(self, name, subtype):
        if name is None:
            available = False
            while not available:
                listing = self._pickcreature(name, subtype)
                roll = random.randint(1, 20)
                available = (roll <= listing[10])
        else:
            listing = self._pickcreature(name, subtype)
        (self.subtype, self.name) = listing[:2]
        (ST, DX, IQ, PP, hit, damage) = listing[2:8]
        self.stats = StatSet(ST, DX, IQ, PP, hit, damage)
        (self.basevalue, self.upkeep, self.availability) = listing[8:11]
        self.details = listing[11]

    def _pickcreature(self, name, subtype):
        mylist = self.animals
        if subtype is not None:
            mylist = [L for L in self.animals if L[0] == subtype]
            if not mylist:
                raise CreatureError("Invalid trainable animal type %s" % 
                                    subtype)
        if name is not None:
            for listing in mylist:
                if listing[1] == name:
                    return listing
            else:
                if subtype is not None:
                    raise CreatureError("Invalid trainable animal %s: %s" %
                                        (subtype, name)) 
                raise CreatureError("Invalid trainable animal %s" % name)
        return random.choice(mylist)

    def value(self):
        return int(self.basevalue + (0.1 * self.basevalue) * self.stats.level())

    def fullname(self):
        """Return name including subtype, if any."""
        if self.subtype is not None:
            return "%s: %s" % (self.subtype, self.name)
        return self.name

    def __str__(self):
        val = self.fullname()
        val += "\n  %s Upkeep: %s/wk" % (self.stats, self.upkeep)
        if self.details:
            val += "\n\n  %s" % wrapped(self.details, indent=2)
        return val


