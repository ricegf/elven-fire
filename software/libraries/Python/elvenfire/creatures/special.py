import random

from elvenfire.utilities import wrapped
from elvenfire.creatures import CreatureError
from elvenfire.creatures.basics import Creature, StatSet


class SpecialCreature (Creature):

    #             Creature     Size/Type  ST  DX  IQ   ++   MA      Ht  Dmg   Psn  Miss  Psn Details
    #             -----------  ---------  --  --  --  ---   ------  --  ----- ---  ----- --- -------
    creatures = [('Dragon',    '1-hex',   10, 12, 10,   5,  '6/10', 1,  [2.5], 0,  [2.5], 0, 'Breath is treated as thrown weapon, at 1 fatigue per breath.'),
                 ('Dragon',    '2-hex',   15, 12, 12,   5,  '6/12', 2,  [3.5], 0,  [4.5], 0, 'Breath is treated as thrown weapon, at 1 fatigue per breath.'),
                 ('Dragon',    '3-hex',   20, 12, 14,  10,  '6/14', 2,  [4.0], 0,  [5.5], 0, 'Breath is treated as thrown weapon, at 2 fatigue per breath.'),
                 ('Dragon',    '4-hex',   25, 13, 16,  15,  '6/16', 3,  [5.0], 0,  [7.0], 0, 'Breath is treated as thrown weapon, at 3 fatigue per breath.'),
                 ('Dragon',    '5-hex',   30, 13, 16,  15,  '6/18', 4,  [5.5], 0,  [8.5], 0, 'Breath is treated as thrown weapon, at 3 fatigue per breath.'),
                 ('Dragon',    '6-hex',   40, 13, 18,  20,  '6/18', 4,  [6.5], 0,  [9.5], 0, 'Breath is treated as thrown weapon, at 4 fatigue per breath.'),
                 ('Dragon',    '7-hex',   50, 14, 20,  25,  '8/20', 5,  [7.0], 0, [11.0], 0, 'Breath is treated as thrown weapon, at 4 fatigue per breath.'),
                 ('Dragon',    '8-hex',   55, 14, 20,  25,  '8/20', 5,  [7.0], 0, [11.5], 0, 'Breath is treated as thrown weapon, at 4 fatigue per breath.'),
                 ('Dragon',    '9-hex',   60, 14, 20,  30,  '8/20', 5,  [7.5], 0, [11.5], 0, 'Breath is treated as thrown weapon, at 4 fatigue per breath.'),
                 ('Dragon',    '10-hex',  70, 14, 22,  35,  '8/22', 5,  [7.5], 0, [12.0], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '11-hex',  75, 14, 22,  35,  '8/22', 6,  [8.0], 0, [12.5], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '12-hex',  85, 14, 22,  40,  '8/22', 6,  [8.0], 0, [12.5], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '13-hex',  90, 14, 22,  45,  '8/24', 6,  [8.5], 0, [13.0], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '14-hex', 100, 14, 24,  50,  '8/24', 6,  [9.0], 0, [13.5], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '15-hex', 110, 14, 24,  55,  '8/24', 7,  [9.5], 0, [13.5], 0, 'Breath is treated as thrown weapon, at 6 fatigue per breath.'),
                 ('Dragon',    '16-hex', 125, 14, 24,  60,  '8/24', 7, [10.0], 0, [14.0], 0, 'Breath is treated as thrown weapon, at 6 fatigue per breath.'),
                 ('Dragon',    '17-hex', 140, 14, 24,  70,  '8/26', 7, [10.5], 0, [14.5], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '18-hex', 160, 14, 24,  75,  '6/26', 7, [11.0], 0, [14.5], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '19-hex', 180, 15, 24,  80,  '6/26', 8, [12.0], 0, [15.0], 0, 'Breath is treated as thrown weapon, at 5 fatigue per breath.'),
                 ('Dragon',    '20-hex', 190, 15, 24,  90,  '6/28', 8, [13.0], 0, [15.5], 0, 'Breath is treated as thrown weapon, at 6 fatigue per breath.'),
                 ('Dragon',    '21-hex', 200, 15, 25, 100,  '6/28', 9, [15.0], 0, [16.5], 0, 'Breath is treated as thrown weapon, at 6 fatigue per breath.'),

                 ('Elemental', 'Earth',   20, 11,  8,  15,      8,  3,  [7.0], 0, [],     0, 'Immune to fire; water storm causes d6/turn.'),
                 ('Elemental', 'Stony',   20, 11,  8,  15,      8,  4,  [9.0], 0, [],     0, 'Immune to fire, water, and boulders.'),
                 ('Elemental', 'Metal',   20, 11,  8,  15,      8,  5, [10/5], 0, [],     0, 'Immune to fire, water, and boulders; lightning/electricity does double damage.'),
                 ('Elemental', 'Ice',     20, 12,  8,  15, '10/16', 0,  [5.5], 0, [],     0, 'Affected by normal weapons; artifacts do half damage.  Fire does double damage.  Regain 14 St/turn in Water Storm.  Can swim.'),
                 ('Elemental', 'Water',   20, 12,  8,  15, '10/16', 0,  [3.5], 0, [],     0, 'Immune to normal weapons; artifacts do half damage.  Fire does double damage.  Regain 14 St/turn in Water Storm.  Can swim.  Attacks by drowning (4vDx or take 3.5 [d6] from water inhalation).'),
                 ('Elemental', 'Steam',   20, 12,  8,  15, '10/16', 0,  [3.5], 0, [],     0, 'Immune to normal weapons; artifacts do half damage.  Fire does double damage.  Regain 14 St/turn in Water Storm.  Can swim.  Fights HTH only; armor protects for only the first turn.'),
                 ('Elemental', 'Air',     20, 12,  8,  15,     20,  0,  [3.5], 0, [],     0, 'Immune to any weapon, fire, or lightning.  Affected by other mental abilities normally.  If ST>30, then can attack by whirlwind ([ST/10]vSt or be lifted and dropped).  Otherwise, elemental is blurred (Dx-2 to attack).'),
                 ('Elemental', 'Fire',    20, 13,  8,  15,     10,  0,  [5.5], 0, [],     0, 'Uses fireballs per Etheral Bow as if IQ=16 [d8/ST]; spending 3 MA/hex creates a 12-turn hex of fire.  Immune to fire and normal weapons; artifact weapons do half damage.  A liter of water does 3.5 [d6] damage, and a water storm does 14 [4d6] per turn.  Water elemental does double damage.'),

                 ('Giant',     '1-hex',   20,  9,  7,  12,     10,  0,  [9.0], 0, [],     0, 'Max DX and IQ of 10; usually fight with clubs and without armor.'),
                 ('Giant',     '3-hex',   25,  9,  7,  13,     10,  0, [10.5], 0, [],     0, 'Max DX and IQ of 10; usually fight with clubs and without armor.'),
                 ('Giant',     '6-hex',   45, 10,  7,  20,     10,  0, [13.0], 0, [],     0, 'Max DX and IQ of 10; usually fight with clubs and without armor.'),
                 ('Giant',     '10-hex',  75,  9,  7,  30,     10,  0, [15.0], 0, [],     0, 'Max DX and IQ of 10; usually fight with clubs and without armor.'),
                 ('Giant',     '15-hex', 125,  8,  7,  46,     10,  0, [20.0], 0, [],     0, 'Max DX and IQ of 10; usually fight with clubs and without armor.'),

                 ('Hydra',     '1-hex',   12, 10,  6,   9,      8,  0,  [2.5], 9, [],     0, 'Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '2-hex',   20, 11,  7,  12,      8,  0,2*[3.5], 9, [],     0, '2 heads; 2 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '3-hex',   25, 11,  7,  14,      8,  0,3*[4.0], 9, [],     0, '3 heads; 3 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '4-hex',   30, 12,  8,  16,      8,  0,4*[4.5], 9, [],     0, '4 heads; 4 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '5-hex',   40, 12,  9,  20,      8,  0,5*[5.5], 9, [],     0, '5 heads; 5 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '6-hex',   50, 12,  9,  23,      8,  0,6*[6.0], 9, [],     0, '6 heads; 6 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '7-hex',   60, 13, 10,  27,      8,  0,7*[6.5], 7, [],     0, '7 heads; 7 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '8-hex',   65, 13, 10,  29,      8,  0,8*[6.5], 7, [],     0, '8 heads; 8 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '9-hex',   69, 13, 10,  30,      8,  0,9*[7.0], 7, [],     0, '9 heads; 9 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '10-hex',  72, 13, 11,  32,      8,  0,10*[7.0],7, [],     0, '10 heads; 10 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '11-hex',  78, 13, 11,  34,      8,  0,11*[7.0],7, [],     0, '11 heads; 11 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '12-hex',  83, 13, 11,  35,      8,  0,12*[7.0],7, [],     0, '12 heads; 12 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '13-hex',  86, 13, 11,  36,      8,  0,13*[7.0],7, [],     0, '13 heads; 13 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),
                 ('Hydra',     '14-hex',  90, 12, 12,  38,      8,  0,14*[9.0],5, [],     0, '14 heads; 14 attacks/turn.  Heads do not grow back when cut off.  Poison glands can be converted into weapon poison by a Chemist (2 doses per head).'),

                 ('Hymenopteran', 'Basic',       6, 10, 12,  6,  8, 0,  [2.5], 0, [],     0, 'One "commander" bug is required to control about 30 other bugs (except Myrmidons and Plunges).  Bugs without a Basic to control them simply mill around blindly, accomplishing nothing.  Basics tend to ride Spyders near the rear of the battle line, and avoid combat whenever possible.'),
                 ('Hymenopteran', 'Spyder',      8, 10,  6,  6, 12, 1,  [3.5], 0, [],     0, 'This 2-hex bug rarely fights, but is ridden by Basics into combat.  They never panic.'),
                 ('Hymenopteran', 'Low Render', 10, 11,  6,  6, 10, 0,  [5.0], 0, [],     0, 'A standard small warrior bug.'),
                 ('Hymenopteran', 'Termagants', 10, 11,  6,  6, 12, 0,  [5.0], 0, [],     0, 'Small warrior bug; will use a sword if it can find one.'),
                 ('Hymenopteran', 'Phlanx',     16, 10,  6,  8, 12, 2,  [7.0], 0, [],     0, '2-hex warrior bug'),
                 ('Hymenopteran', 'Gantuas',    24, 10,  6, 12, 10, 3, [10.0], 0, [],     0, '3-hex warrior bug that can crush with its claws and legs.'),
                 ('Hymenopteran', 'Myrmidon',   12, 12,  8,  6, 10, 0,  [7.0], 0, [7.0],  0, "man-sized warrior that always uses human weapons to fight, and doesn't require a Basic for control."),
                 ('Hymenopteran', 'Plunges',     8, 16,  8,  6, '6/14',0,[3.5],0, [],     0, 'This bug flies and does an extra 3.5 [d6] damage when diving.  It also does not require a Basic.'),
                 ('Hymenopteran', 'Workers',    20,  8,  8,  8,  8, 0,  [2.5], 0, [],     0, 'Workers will collect 3 bodies (about 250 kg), then return to the nest.  They will fight only to defend the nest.'),

                 ('Octopus',   '1-hex',   18, 15, 10,  14,   '8/8', 2,3*[8.0], 0, [10.5], 0, 'Uses 3 weapons at once (or two-handed weapon and shield, or other combinatino up to 3 hands worth). The octopus has no rear hex.'),
                 ('Octopus',   '2-hex',   28, 15, 10,  17,   '8/8', 2,3*[9.5], 0,3*[5.5], 0, 'Uses 3 weapons at once (or two-handed weapon and shield, or other combinatino up to 3 hands worth). The octopus has no rear hex.'),
                 ('Octopus',   '3-hex',   35, 16, 11,  20,  '10/8', 3,3*[10.5],0,3*[5.5], 0, 'Uses 3 weapons at once (or two-handed weapon and shield, or other combinatino up to 3 hands worth). The octopus has no rear hex.'),
                 ('Octopus',   '4-hex',   42, 17, 11,  23, '10/10', 3,3*[12.0],0,3*[5.5], 0, 'Uses 3 weapons at once (or two-handed weapon and shield, or other combinatino up to 3 hands worth). The octopus has no rear hex.'),
                 ('Octopus',   '5-hex',   47, 17, 12,  25, '12/10', 4,3*[15.0],0, [17.5], 0, 'Uses 3 weapons at once (or two-handed weapon and shield, or other combinatino up to 3 hands worth). The octopus has no rear hex.'),
                 ('Octopus',   '6-hex',   50, 16, 14,  26,  '10/8', 5,3*[15.5],0, [22.5], 0, 'Uses 3 weapons at once (or two-handed weapon and shield, or other combinatino up to 3 hands worth). The octopus has no rear hex.'),

                 ## *** No plants or nuisance creatures!!

                ]


    dragons = {'Red' : 'Breathes fire, or uses Fire 3 ability.  Flaming weapons do half damage; Frosted do double.',
               'Blue' : 'Spits ice balls, or uses Ice Storm 3 ability.  Frosted weapons do half damage; Flaming do double.',
               'Green' : 'Breathes ammonia gas.  Non-artifact armor does not protect, but Flight/Swim 3 ability does.',
               'Brown' : 'Spits rocks per Boulder ability.',
               'Purple' : 'Breathes lightning bolts, which do double damage to creatures in metal armor; not affected by lightning.',
               'Grey' : 'Breath causes no damage, but acts exactly as Sleep 3.',
               'Yellow' : 'Breathes acid, which corrodes armor worn by victim to nothing in 12 turns (artifacts get 3vDx to avoid this fate).',
               'Black' : 'Breath causes no damage, but rather acts as Create: Shadow 3 ability.',
              }

    hydras = {'Normal' : '',
              'Spitting' : 'Can opt to spit poison at a distance instead of biting with each head.',
              'Pyro' : 'Optionally, can breathe fireballs from each head (treat as Fireball 5).',
             }

    def __init__(self, type=None, size=None, element=None):
        self.element = None
        listing = self._picklisting(type, size)
        (self.subtype, self.name) = listing[:2]
        (ST, DX, IQ, PP, MA) = listing[2:7]
        (hits, dmg, psn, altdmg, altpsn) = listing[7:12]
        self.stats = StatSet(ST, DX, IQ, PP, hits, dmg, psn, altdmg, altpsn, MA)
        self.details = listing[12]
        Creature.__init__(self, self.name, self.stats, self.details)
        self._setspecials(element)

    def _picklisting(self, type, size):
        mylist = self.creatures
        if type is not None:
            mylist = [L for L in self.creatures if L[0] == type]
            if not mylist:
                raise CreatureError('Invalid creature type: %s' % type)
        if size is not None:
            for L in mylist:
                if L[1] == size:
                    return L
            else:
                if type is not None:
                    raise CreatureError("Invalid creature size '%s' for type '%s'" % (size, type))
                raise CreatureError("Invalid creature size: %s" % size)
        return random.choice(mylist)

    def _setspecials(self, element):
        if self.subtype == 'Dragon':
            self.element = element if element is not None else random.choice([color for color in self.dragons.keys()])
            self.details += '  ' + self.dragons[self.element]
        elif self.subtype == 'Hydra':
            self.element = element if element is not None else random.choice([type for type in self.hydras.keys()])
            self.details += '  ' + self.hydras[self.element]
            if self.element == 'Spitting':
                self.stats.altdamage = self.stats.damage
                self.stats.altpoison = self.stats.poison
            elif self.element == 'Pyro':
                self.stats.altdamage = [12.5] if self.name in ['1-hex', '2-hex', '3-hex', '14-hex'] else [17.5]

    def fullname(self):
        val = self.name
        if self.subtype is not None:
            val = "%s: %s" % (self.subtype, val)
        if self.element is not None:
            val = "%s %s" % (self.element, val)
        return val

    def __str__(self):
        val = "%s  %s" % (self.fullname(), self.stats)
        if self.details:
            val += wrapped("\n\n  %s" % self.details, indent=2)
        return val
        