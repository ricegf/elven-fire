import random

from elvenfire import bonus5
from elvenfire.utilities import wrapped
from elvenfire.creatures import CreatureError
from elvenfire.creatures.basics import Creature, StatSet
from elvenfire.abilities.charabilities import *
from elvenfire.labyrinth.traps import Trap


class NonTrainableCreature (Creature):

    #           Type                Name                   ST  DX  IQ  ++      MA  Ht  Dmg         Psn Miss   Psn Details
    #           ------------------  ---------------------  --  --  --  --      --  --  ----------- --- ------ --- -------
    animals = [('Giant Ant',        'Black',               12, 11,  1,  8,     12,  1,  [3.5],       0, [],     0, 'Bites with pincers; will grab any dead or unconscious creature and carry back to hive. Incredible lifting ability; can carry 100xSt in weight.'),
               ('Giant Ant',        'Carpenter',           12, 11,  1,  8,     12,  1,  [4.5],       0, [],     0, 'Bites with pincers; will grab any dead or unconscious creature and carry back to hive. Incredible lifting ability; can carry 100xSt in weight. Burrows into and shreds large wooden objects.'),
               ('Giant Ant',        'Red',                 12, 11,  1,  8,     12,  1,  [2.5],       5, [],     0, 'Bites with pincers; will grab any dead or unconscious creature and carry back to hive. Incredible lifting ability; can carry 100xSt in weight. 4vSt to resist additional damage from poison.'),
               ('Giant Ant',        'Soldier',             12, 12,  1,  8,     12,  2,  [6.5],       0, [],     0, 'Bites with pincers; will grab any dead or unconscious creature and carry back to hive. Incredible lifting ability; can carry 100xSt in weight. Will instinctively coordinate attack with other soldier ants; will attack non-soldier ants in preference to anything else.'),
               ( None,              'Apep',                40, 11,  8, 19,      6,  3,  [7.0],       0, [],     0, '6-hex snake that is perpetually in shadow (Dx-7 to hit).'),
               ('Basilisk',         '1-hex',               10,  8,  8,  8,     12,  0,  [3.5],       0, [],     0, 'May bite or attempt Sleep 2 at no ST cost (ST < 50 to sleep for d6 hours or until hit; ST < 20 frozen for 2d6 turns or until Awoken).'),
               ('Basilisk',         '2-hex',               20,  9,  8, 12,     12,  0,  [4.5],       0, [],     0, 'May bite or attempt Sleep 3 at no ST cost (any character, or a MH of ST < 40, to sleep for d6 hours or until hit; ST < 50 frozen for 2d6 turns or until Awoken).'),
               ('Basilisk',         '3-hex',               30, 11,  9, 16,     14,  0,  [6.5],       0, [],     0, 'May bite or attempt Sleep 4 at no ST cost (any character or MH to sleep for d6 hours or until hit; any character frozen for 2d6 turns or until Awoken).'),
               ('Basilisk',         '4-hex',               40, 14, 10, 21,     18,  0, [10.5],       0, [],     0, 'May bite or attempt Sleep 5 at no ST cost (any character or MH to sleep for d6 hours or until hit; any character or MH frozen for 2d6 turns or until Awoken).'),
               ('Giant Beetle',     'Bombadier',           20, 10,  1, 10,     10,  2,  [5.0],       0, [],     0, "Fires acid cloud once per day into rear or side hexes (3vDx to dodge or take 6.5 damage; armor doesn't help)."),
               ('Giant Beetle',     'Boring',              24, 10,  1, 11,      8,  1,  [4.5],       0, [],     0, 'Burrows into and shreds large wooden objects'),
               ('Giant Beetle',     'Rhinoceros',          36, 10,  1, 15,      8,  3, [10.5],       0, [],     0, 'Treat horn as pole weapon'),
               ('Giant Beetle',     'Stone (1-hex)',       30, 10,  2, 14,      6,  5,  [5.0],       0, [],     0, 'Creature with stony guts, like a gargoyle; loves Am Bushes, whose victims they enjoy for lunch.'),
               ('Giant Beetle',     'Stone (2-hex)',       50, 10,  2, 20,      4,  8, [10.5],       0, [],     0, 'Oversized creature with stony guts, like a gargoyle; loves Am Bushes, whose victims they enjoy for lunch.'),
               ('Giant Beetle',     'Water',               16, 10,  1,  9, '8/16',  1,  [3.5],       0, [],     0, 'When in water, will grab opponent and drag to bottom (5vSt to break free per turn; 4vSt if Physical Fitness 1 or Flight / Swim 3; 2vSt if both).'),
               ('Beholder',         'Black',               26, 16, 16, 19, '12/24', 0,  [9.0],       0, [],     0, 'Large floating eye which attacks ONLY using mental abilities; any mental attack against a beholder fails on 4vIQ; must fly; selects from all mental abilities equally'),
               ('Beholder',         'Blue',                26, 16, 16, 19, '12/24', 0,  [9.0],       0, [],     0, 'Large floating eye which attacks ONLY using mental abilities; any mental attack against a beholder fails on 4vIQ; must fly; usually found near water; selects primarily from water-based abilities'),
               ('Beholder',         'Green',               26, 16, 16, 19, '12/24', 0,  [9.0],       0, [],     0, 'Large floating eye which attacks ONLY using mental abilities; any mental attack against a beholder fails on 4vIQ; must fly; usually found near forests; favors Ethereal Bow'),
               ('Beholder',         'Brown',               26, 16, 16, 19, '12/24', 0,  [9.0],       0, [],     0, 'Large floating eye which attacks ONLY using mental abilities; any mental attack against a beholder fails on 4vIQ; must fly; usually found near deserts; favor Summon abilities'),
               ('Beholder',         'Albino',              26, 16, 20, 20, '12/24', 0, [13.0],       0, [],     0, 'Large floating eye which attacks ONLY using mental abilities; any mental attack against a beholder fails on 4vIQ; must fly; always has Vision 5; very evil'),
               ('Beholder',         'of the Deep',         26, 16, 16, 19, '12/24', 0,  [5.0],       0, [],     0, "Large floating eye which attacks ONLY using mental abilities; any mental attack against a beholder fails on 4vIQ; lives only underwater; in addition to mental abilities, has a stinger 'tail' with which it can stun nearby prey (5vSt or frozen for 3 turns)"),
               ('Boar',             'Giant',               32, 10,  5, 15,      14, 1,  [9.0],       0, [],     0, ''),
               ('Boar',             'Warthog',             14, 10,  5,  9,      12, 0,  [4.5],       0, [],     0, ''),
               ('Boar',             'Wild',                12, 10,  1,  9,      12, 1,  [5.0],       0, [],     0, ''),
               ('Carrion Crawler',  '1-tendril',           15, 10,  1,  8,      14, 0,  [0.5] *  1,  7, [],     0, '3-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '2-tendril',           15, 10,  1,  8,      14, 0,  [0.5] *  2,  7, [],     0, '3-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '3-tendril',           16, 10,  1,  9,      14, 0,  [0.5] *  3,  7, [],     0, '3-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '4-tendril',           16, 11,  1,  9,      14, 0,  [0.5] *  4,  7, [],     0, '4-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '5-tendril',           17, 11,  1,  9,      14, 0,  [0.5] *  5,  7, [],     0, '4-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '6-tendril',           18, 12,  1, 10,      14, 0,  [0.5] *  6,  7, [],     0, '4-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '7-tendril',           19, 12,  1, 10,      16, 0,  [0.5] *  7,  7, [],     0, '5-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '8-tendril',           21, 13,  1, 11,      16, 0,  [0.5] *  8,  7, [],     0, '5-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '9-tendril',           24, 14,  1, 13,      16, 0,  [0.5] *  9,  7, [],     0, '5-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '10-tendril',          28, 15,  1, 14,      18, 1,  [0.5] * 10,  7, [],     0, '6-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '11-tendril',          34, 16,  1, 17,      18, 1,  [0.5] * 11,  7, [],     0, '6-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Carrion Crawler',  '12-tendril',          44, 15,  1, 20,      20, 1,  [0.5] * 12, 11, [],     0, '6-hex; looks like a giant caterpillar, with one or more tendrils on its head with which it attacks (once per tendril per turn). Also has large, round mouth with teeth to grind up the dead slowly but quite thoroughly, leaving only metal and gems behind.'),
               ('Centipede',        'Giant',                4,  6,  1,  3,      14, 0,  [0.5],      11, [],     0, 'On a hit with its tail-mounted stinger (side or rear hex only), it injects poison (4vSt to avoid damage); poison sac may be collected by Chemist and converted to DCl 5 [2d4] weapon poison by Chemist; typical yield is 3 doses per centipede.'),
               ( None,              'Cockatrice',          18, 11,  5, 11, '6/18',  1,  [1.0],       0, [],     0, 'Any hit freezes victim (broken by separation from cockatrice); when not under attack, cockatrice will suck all blood from victim (loses 1 St per turn).'),
               ('Crab',             'Giant',                8,  8,  3,  6, '8/12',  5,  [4.5] * 2,   0, [],     0, 'Attacks once per claw; on a hit, victim must make 3vDx or be caught. Once caught, victim is unable to attack and suffers 3.5 [d6] damage per turn until his escape (4vDx).  Crab may also scurry back under water, carrying the victim along.'),
               ('Crocodile',        'Normal',               8, 10,  3,  7, '8/12',  2,  [4.5],       0, [],     0, 'May also sweep with tail in rear or side hex without Dx penalty; if hit, victim must make 4vDx or fall down (no damage).  Can swim.'),
               ('Crocodile',        'Giant',               16, 10,  5, 10, '8/12',  2,  [6.5],       0, [],     0, 'May also sweep with tail in rear or side hex without Dx penalty; if hit, victim must make 5vDx or fall down (no damage).  OR, tail may be used as club at Dx-2, doing 4.5 [d8] damage.  Can swim.'),
               ( None,              'Djinni',              24, 12, 14, 16, '8/24',  0,  [5.0],       0, [],     0, 'In one turn becomes a small tornado: loses 2 St/turn in fatigue but does 9 [2d8] per attack and moves much faster. When not tornado, can use mental abilities.'),
               ( None,              'Doppleganger',        12, 12, 12, 12,      10, 0,  [5.5],       0, [],     0, 'Immune to Sleep; can change to different form in one turn (at 1 St cost), but attributes remain unchanged.'),
               ( None,              'Giant Eagle',         18, 12,  6, 12, '8/24',  2,  [7.0],       0, [],     0, 'Does extra d6 damage on a dive attack with its bill, or may grasp with its claws and lift up to 120 kg and carry prey to its nest (4vSt to wiggle free, but remember the eagle is flying after the first round).  Climbs 10m per turn for 5 turns (d6 damage per 10m height on falling). After 5 turns, character is lost.'),
               ('Eel',              'Electric',            10, 10,  4,  8,      12, 1,  [7.0],       0, [],     0, 'Cannot leave the water; double damage on anyone wearing metal armor.'),
               ('Eel',              'Feather',              4, 10,  1,  5,       0, 0,  [1.0],     5.5, [],     0, 'Cannot leave the water; drift with the current, but if touched will sting. 3vSt to avoid poison, and must make 3vDx to get free or remain engaged next turn.'),
               ('Eel',              'Giant',               20, 10,  4, 11,      12, 2, [10.0],       0, [],     0, 'Cannot leave the water.'),
               ('Eel',              'Giant Electric',      20, 10,  4, 11,      12, 2, [15.0],       0, [],     0, 'Cannot leave the water; double damage on anyone wearing metal armor.'),
               ('Frog',             'Giant',               14, 11,  1,  8,       6, 0,  [2.5],       0, [],     0, "This greenish creature, the size of a very fat elephant, can walk at its normal MA or it can leap during its movement phase and then attack the same turn. It can leap over objects up to 5 meters high landing 3 hexes away, or over shorter objects and landing up to 8 hexes away, and face any direction upon landing. Its favorite tactic is to hide in tall weeds near water and attempt to snatch a quick meal. It attacks with its long tongue up to 4 hexes away, and (if target fails 3vDx) grasps the target tightly. Once grasped, the victim must make 4vSt to be dropped on the ground on a randomly selected hex in the tongue's path. If the St saving roll is missed, the victim will be swallowed whole. Once swallowed, the victim loses 1 St/turn until dead or is cut out by companions. The frog will flee at maximum speed once it has eaten, or if seriously injured."),
               ('Frog',             'Killer',              20, 12,  1, 11,       6, 0,  [4.5],       0, [],     0, "This greenish creature, the size of a very fat elephant, can walk at its normal MA or it can leap during its movement phase and then attack the same turn. It can leap over objects up to 5 meters high landing 3 hexes away, or over shorter objects and landing up to 8 hexes away, and face any direction upon landing. Its favorite tactic is to hide in tall weeds near water and attempt to snatch a quick meal. It is much bumpier than a giant frog, and has a horned extension on its upper lip with which it rams its chosen prey.  Once the victim is dead, the killer frog will grasp it with its tongue and swallow it whole."),
               ('Frog',             'Poisonous',            9, 11,  1,  7,       6, 0,  [2.5],       0, [],     0, "This greenish creature, the size of a very fat elephant, can walk at its normal MA or it can leap during its movement phase and then attack the same turn. It can leap over objects up to 5 meters high landing 3 hexes away, or over shorter objects and landing up to 8 hexes away, and face any direction upon landing. Its favorite tactic is to hide in tall weeds near water and attempt to snatch a quick meal. It attacks by licking its victim (up to 4 hexes away), delivering a potent sleeping potion.  If the victim fails 4vSt, they fall immediately into a deep sleep for 12 turns.  The saliva glands of the poisonous frog can be used by a Chemist to produce two molotails of sleeping gas."),
               ( None,              'Fuzzball',             1,  1,  1,  1,      12, 0, [13.0],       0, [],     0, "The fuzzball, which looks like a orange fuzzy beach ball 3/4 meter in diameter, is a unique creature which never eats.  It rolls silently across open areas of leand and floats large distances across water.  It spends its lifespan of 3-4 months searching for another living creature.  Once it senses life, it will approach at maximum speed and with minimum noise; upon touching the victim, it explodes, doing 13 [2d12] in the victim's hex and 7 [2d6] in each adjacent hex.  In addition, the megahex is filled with an orange jelly-like substance with many small seeds; any animal killed within the megahex is consumed by the seed over the course of an hour or so, at which point the seed has grown into a new fuzzball.  Any damage inflicted on the fuzzball causes it to explode in place."),
               ( None,              'Gargoyle',            16, 11,  8, 11, '10/24', 3,  [7.0],       0, [],     0, 'Max IQ=10; gargoyles can fly via a form of levitation, and favor hand-to-hand combat.'),
               ( None,              'Ghoul',               10, 11,  8,  9,      10, 0,  [0.5],       0, [],     0, 'Eat dead things; rarely use weapon; will attack source of light; mostly attacks with HTH.'),
               ( None,              'Giant Goat',          25, 13,  5, 14,      24, 0,  [9.0],       0, [],     0, 'Favors rocky hills; may charge if not engaged.'),
               ( None,              'Goblin',               6,  8, 10,  8,      10, 0,  [3.5],       0, [3.5],  0, 'Never lie; love money'),
               ('Golem',            'Clay',                10, 12,  1,  7,      12, 0,  [4.5],       0, [],     0, 'Created by mankind using a wish (see Wish Ring); created with "programming" intact, and will follow those instructions until destroyed.  The instructions can only be changed by a wish or similar powerful adjustment.'),
               ('Golem',            'Stone',               28, 12,  1, 13,      12, 3,  [9.0],       0, [],     0, 'Created by mankind using a wish (see Wish Ring); created with "programming" intact, and will follow those instructions until destroyed.  The instructions can only be changed by a wish or similar powerful adjustment.'),
               ('Golem',            'Iron',                40, 12,  1, 17,      12, 5, [13.0],       0, [],     0, 'Created by mankind using a wish (see Wish Ring); created with "programming" intact, and will follow those instructions until destroyed.  The instructions can only be changed by a wish or similar powerful adjustment.'),
               ('Golem',            'Silver',              24, 12,  1, 12,      12, 1,  [5.0],       0, [],     0, 'Created by mankind using a wish (see Wish Ring); created with "programming" intact, and will follow those instructions until destroyed.  The instructions can only be changed by a wish or similar powerful adjustment.  Although capable of fighting melee, typically use one of several mental abilities.'),
               ('Golem',            'Gold',                32, 12,  1, 15,      12, 0,  [7.0],       0, [],     0, 'Created by mankind using a wish (see Wish Ring); created with "programming" intact, and will follow those instructions until destroyed.  The instructions can only be changed by a wish or similar powerful adjustment.  Although capable of fighting melee, typically use one of several mental abilities.  Immune to mental attacks, and artifact weapon bonuses do not apply.'),
               ('Goo',              'Large',           100000,  1,  1,  0,       2, 0,  [1.0],       0, [],     0, 'Flows onto victim, and will suffocate in 1 turn.  Its small nucleus requires 7vDx to hit, but any damage will kill it.'),
               ('Goo',              'Medium',           25000,  1,  1,  0,       3, 0,  [1.0],       0, [],     0, 'Flows onto victim, and will suffocate in 1 turn.  Its small nucleus requires 6vDx to hit, but any damage will kill it.'),
               ('Goo',              'Small',             5000,  1,  1,  0,       4, 0,  [1.0],       0, [],     0, 'Flows onto victim, and will suffocate in 2 turns.  Its small nucleus requires 5vDx to hit, but any damage will kill it.'),
               ( None,              'Harpy',               10, 12, 12, 11, '10/16', 0,  [7.0],       0, [7.0],  0, 'Before engaging in physical combat, harpies sing, causing anyone failing 4vIQ to stop and listen enraptured (unmoving for 6 turns or until hit). Rarely, an exceptional harpy will have a higher IQ and some mental abilities (such as Avert). Can fly.'),
               ( None,              'Hobgoblin',           12,  6,  6,  8,      10, 0,  [7.0],       0, [7.0],  0, 'Big dumb goblin; max IQ=8'),
               ('Hyena',            'Normal',              10, 13,  6,  9,      14, 1,  [4.5],       0, [],     0, 'Pack animals; run down weak or injured animals.  Cautious, and will rarely attack except with overwhelming odds.'),
               ('Hyena',            'Giant',               22, 12,  6, 13,      18, 1,  [9.0],       0, [],     0, 'Pack animals; run down weak or injured animals.  Cautious, and will rarely attack except with overwhelming odds.'),
               ( None,              'Invisible Stalker',   20, 12, 10, 14,      14, 2, [10.5],       0, [],     0, 'This creature moves silently and invisibly, and loves to pick off stragglers from a group of adventurers. Noticing this creature requires 6vIQ (5vIQ if victim has Stealth 1). Attacks on an invisible stalker are at DX-6 due to its invisibility and stealth.'),
               ( None,              'IQ Sapper',            4, 14, 16, 11,  '6/18', 0,  [2.5],       0, [],     0, "The IQ sapper is a small bat-like creature which extracts intellect from its victims. Once the victim's IQ is reduced below 4, attacks become impossible due to lack of coordination; at 0 or below, the victim falls unconscious. Fortunately, IQ returns at the rate of 1 per hour, with no lasting damage."),
               ('Lizard',           'Fire',                27, 13,  5, 15,      16, 2,  [6.0],       0, [7.5],  0, 'Breath as thrown weapon, inflicting 2.5 per point of fatigue up to 3. Fire does half damage.'),
               ('Lizard',           'Chameleon',           22, 12,  5, 13,      20, 2,  [6.0],       0, [],     0, 'In one turn can become almost invisible (4vIQ to notice, Dx-2 to hit) by blending with the background.  Generally prefers to run rather than fight; rarely has great treasure.'),
               ('Manticore',        'Gray',                20, 14,  6, 13,      14, 1,  [5.5],       0, [4.5]*3,0, 'Gray, leather-skinned creatures with spiked tails (spikes act as small crossbow bolts).  Usually have about as many spikes as St, and can either fire up to 3 or bite each round.'),
               ('Manticore',        'Red',                 16, 14,  6, 12,      12, 3,  [5.0],       0, [2.5]*3,6.5*3,'Small, red-striped, leather-skinned creatures with spiked tails (spikes act as small crossbow bolts).  Usually have about as many spikes as St, and can either fire up to 3 or bite each round.  Each spike oozes poisonous gel; if a spike inflicts damage, civtim must make 4vSt or take an additional 6.5 [d12] damage.  A Chemist can make weapon poison from fresh (collected the same week) spikes (1 dose per spike, does 4.5 [d8] damage).'),
               ( None,              'Merman',               6, 10,  8,  8, '10/6',  2,  [3.5],       0, [0.5],  0, 'Dx-4 on land; prefer knives, poles, and nets.'),
               ( None,              'Medusa',              12, 12, 14, 12,      10, 1,  [7.0],       0, [7.0],  0, 'Exceptionally ugly woman with poisonous asps for hair; sometimes may use a weapon, but generally freezes opponent at no fatigue cost. Asps may bit in melee, inflicting d4 damage, plus d8 poison damage if victim fails 3vSt.  Multiple asps may strike, but all are at Dx-2 for each additional asp attacking.'),
               ( None,              'Mind Mirror',         12, 12, 10, 11,      12, 0,  [7.0],       0, [7.0],  0, "Blends almost perfectly into its surroundings (6vIQ to detect). At an opportune moment it adjusts to become a mirror image of one of the nearby creatures (any Character or Trainable Animal). Treat as an illusion, except: (1) unless the mind mirror was detected in advance, characters won't know which is real; (2) disbelief requires 5vIQ, and that's assuming you're disbelieving the mind mirror and not the character it mirrored.  Mind mirrors attack only when necessary; they prefer to collect treasure (3vDx to extract up to 24 coins) and then disappear (4vIQ to catch slipping away)."),
               ( None,              'Neanderthal',         16, 10,  7, 11,      10, 0,  [6.5],       0, [5.5],  0, 'Typically use club, spear, and long bow.  Quite fond of Dwarves.'),
               ( None,              'Ogre',                25,  9,  6, 13,      10, 0, [10.5],       0, [9.5],  0, 'Use giant club; will fight for meat.'),
               ('Owl',              'Normal',               4, 12,  5,  7,  '4/12', 0,  [1.4],       0, [],     0, ''),
               ('Owl',              'Giant',               18, 12,  5, 11,  '8/16', 1,  [4.5],       0, [],     0, 'Often attack by surprise (4vIQ to detect), swooping down and attacking with claws.  If the attack succeeds, no damage is done, but the victim (up to about 100kg) is carried away.  This typically results in a one-on-one with the owl.  Significant treasure may be found among the remains - but the hard part is to find the rest of your party (victim must work through labyrinth to rejoin party - if they are willing!)'),
               ('Rhinoceros',       'Normal',              25, 10,  5, 13,      20, 2,  [7.0],       0, [],     0, 'Treat its horn as a pole weapon, except it can only attack in adjacent hexes.'),
               ('Rhinoceros',       'Wooly',               35, 12,  5, 17,      24, 3,  [9.0],       0, [],     0, 'Treat its horn as a pole weapon, except it can only attack in adjacent hexes.'),
               ( None,              'Sasquatch',           18, 14, 10, 14,      12, 2,  [8.5],       0, [7.5],  0, 'Shy.  Always has Stealth 5 and Leadership 2.  Typically use clubs for combat.  High probability (80%) of traps in room (d4 traps at random locations).'),
               ( None,              'Satyr',               12, 12, 12, 12,      12, 1,  [7.0],       0, [7.0],  0, "All who hear a satyr's pipes must make 4vIQ or be controlled.  Almost always have enchanted weapons."),
               ( None,              'Giant Scorpion',      20, 12,  1, 11,      12, 1,  [2.5],       7, [],     0, 'Grabs on hit (4vSt to break free, Dx-4 while held).'),
               ( None,              'Shadowight',           5,  8,  8,  7,      10, 0,  [3.5],       0, [3.5],  0, 'Like a solid shadow.  Fire and light do double damage.  Can also use mental abilities.'),
               ( None,              'Skeleton',            16, 12,  0,  9,      10, 2, [11.5],       0, [10.5], 0, 'This is an old zombie whose flesh has rotted away; missiles always miss, passing harmlessly between the ribs.  However, damage > 8 in one blow will shatter and destroy.'),
               ('Snake',            'Constrictor',          6, 12,  4,  7,       6, 0,  [2.5],       0, [],     0, 'This snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 3.5 [d6] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            'Large Constrictor',   12, 12,  6, 10,       6, 0,  [4.5],       0, [],     0, 'This snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 4.5 [d8] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            'Giant Constrictor',   20, 12,  6, 12,       6, 0,  [7.0],       0, [],     0, 'This 2-hex snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 5.5 [d10] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            '3-hex Constrictor',   30, 11,  6, 15,       8, 0, [10.5],       0, [],     0, 'This 3-hex snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 10.5 [d20] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            '4-hex Constrictor',   45, 11,  6, 20,       8, 0, [14.0],       0, [],     0, 'This 4-hex snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 14 [4d6] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            '5-hex Constrictor',   70, 11,  6, 29,      10, 0, [18.5],       0, [],     0, 'This 5-hex snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 17.5 [5d6] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            '6-hex Constrictor',  110, 11,  6, 42,      10, 0, [23.0],       0, [],     0, 'This 6-hex snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 21 [6d6] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            '7-hex Constrictor',  150, 10,  6, 55,      12, 0, [30.0],       0, [],     0, 'This 7-hex snake will encircle its victim on a hit (treat as Rope 4) and begin to squeeze, doing 24.5 [7d6] damage per turn.  Likes to swallow victim whole, but only once dead.'),
               ('Snake',            'Poisonous',            6, 12,  4,  7,       6, 0,  [2.5],    3.5,  [],     0, ''),
               ('Snake',            'Large Poisonous',     12, 12,  6, 10,       6, 0,  [4.5],    4.5,  [],     0, ''),
               ('Snake',            'Giant Poisonous',     20, 12,  6, 12,       6, 0,  [7.0],    5.5,  [],     0, '2-hex'),
               ('Snake',            '3-hex Poisonous',     30, 11,  6, 15,       8, 0, [10.5],    6.5,  [],     0, ''),
               ('Snake',            '4-hex Poisonous',     45, 11,  6, 20,       8, 0, [14.0],    8.0,  [],     0, ''),
               ('Snake',            '5-hex Poisonous',     70, 11,  6, 29,      10, 0, [18.5],   10.5,  [],     0, ''),
               ('Snake',            '6-hex Poisonous',    110, 11,  6, 42,      10, 0, [23.0],   13.5,  [],     0, ''),
               ('Snake',            '7-hex Poisonous',    150, 10,  6, 55,      12, 0, [30.0],   16.5,  [],     0, ''),
               ('Snake',            'Spitting',             6, 12,  4,  7,       6, 0,  [2.5],    7.0,  [],     0, 'This snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Snake',            'Large Spitting',      12, 12,  6, 10,       6, 0,  [4.5],    8.5,  [],     0, 'This snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Snake',            'Giant Spitting',      20, 12,  6, 12,       6, 0,  [7.0],   10.0,  [],     0, 'This 2-hex snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Snake',            '3-hex Spitting',      30, 11,  6, 15,       8, 0, [10.5],   12.0,  [],     0, 'This 3-hex snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Snake',            '4-hex Spitting',      45, 11,  6, 20,       8, 0, [14.0],   14.5,  [],     0, 'This 4-hex snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Snake',            '5-hex Spitting',      70, 11,  6, 29,      10, 0, [18.5],   18.0,  [],     0, 'This 5-hex snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Snake',            '6-hex Spitting',     110, 11,  6, 42,      10, 0, [23.0],   22.5,  [],     0, 'This 6-hex snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Snake',            '7-hex Spitting',     150, 10,  6, 55,      12, 0, [30.0],   27.0,  [],     0, 'This 7-hex snake spits (at no St cost) as well as bites.  Treat spit as thrown weapon: victim must make 3vDx to avoid poison to the eyes or take additional damage and become blind.  (Blindness may be healed by a Physicker within 3 hours, or by a Universal Antidote within a day, or by a wish.)'),
               ('Spider',           'Giant',               16, 10,  1,  9,      12, 0,  [7.0],    7.0,  [],     0, "3vIQ to see web; 4vSt to escape web (treat as Rope 4 or Rope 5).  A spider's web is St 20 when attacked with sharp weapons."),
               ('Spider',           'Blink',               16, 10,  1,  9,      12, 0,  [7.0],    7.0,  [],     0, "3vIQ to see web; 4vSt to escape web (treat as Rope 4 or Rope 5).  A spider's web is St 20 when attacked with sharp weapons.  Can teleport (1 St/MH, or free if within web) and attack on same turn."),
               ('Spider',           'Phase',               18, 10,  1,  9,      14, 0,  [7.0],    7.0,  [],     0, "3vIQ to see web; 4vSt to escape web (treat as Rope 4 or Rope 5).  A spider's web is St 20 when attacked with sharp weapons.  Looks blurry due to being slightly out of phase with our dimension; attacks are at Dx-4."),
               ('Spider',           'Widow',               20, 10,  1, 10,      14, 0,  [7.0],   14.0,  [],     0, "3vIQ to see web; 4vSt to escape web (treat as Rope 4 or Rope 5).  A spider's web is St 20 when attacked with sharp weapons."),
               ('Spider',           'Water',               18, 10,  1,  9, '12/24', 0,  [7.0],    7.0,  [],     0, "3vIQ to see web; 4vSt to escape web (treat as Rope 4 or Rope 5).  A spider's web is St 20 when attacked with sharp weapons.  When on the water, may 'skim' along the top quite fast.  Webs are underwater as well"),
               ( None,              'Giant Tick',          14, 10,  1,  8,      12, 4,  [3.5],       0, [],     0, 'On successful hit, a 50% chance exists that tick will "attach" and begin draining blood (additional 2.5 [d4] per turn until tick dies or victim has < 5 St remaining).  While attached, tick cannot attack anyone else.  The back end of a tick is soft, thus side attacks face only 2 hits of protection, and rear attacks no protection.'),
               ( None,              'Troll',               30, 10,  8, 16,       8, 0,  [6.5],       0, [],     0, 'Regenerates 1 hit/turn, except for fire damage.'),
               ( None,              'Dragon Turtle',       12,  9,  5,  8,  '8/24', 4,  [5.5],       0, [9.0],  0, 'Breathes fire for 9 [2d8] damage, at cost of 1 St per breath.  Can swim.'),
               ('Wasp',             'Giant',               10, 12,  1,  7,  '8/24', 0,  [1.0],       9, [],     0, '3vSt to avoid poison.  Can fly.'),
               ('Wasp',             'Giant Red',           12, 12,  1,  8,  '8/24', 0,  [1.0],      13, [],     0, 'Can fly.'),
               ( None,              'Wight',               24, 14,  8, 15,      12, 3,  [9.5],       0, [7.0],  0, 'Only hurt by ethereal bow or enhanced weapons.'),
               ('Worm',             'Giant',               15, 10,  1,  8,       8, 0,  [6.0],       0, [],     0, "Critical hits don't apply - worms' critical parts are dispersed and redundant.  Most worms thrash when injured; treat as a d6 attack to any surrounding hex, though the creature really isn't aiming."),
               ('Worm',             'Earth',               15, 10,  1,  8,       8, 0,  [6.0],       0, [],     0, "Critical hits don't apply - worms' critical parts are dispersed and redundant.  Most worms thrash when injured; treat as a d6 attack to any surrounding hex, though the creature really isn't aiming.  Prefer to live underground; fear water."),
               ('Worm',             'Glow',                15, 10,  1,  8,       8, 0,  [6.0],       0, [],     0, "Critical hits don't apply - worms' critical parts are dispersed and redundant.  Most worms thrash when injured; treat as a d6 attack to any surrounding hex, though the creature really isn't aiming.  Prefer to live underground; fear water.  When injured or threatened, glow white-hot.  This will temporarily blind attackers (Dx-4) and may damage metal weapons (50% of non-enhanced weapons that hit worm will reduce their damage ability by 1)."),
               ('Worm',             'Green',               15, 10,  1,  8,       8, 0,  [6.0],       0, [],     0, "Critical hits don't apply - worms' critical parts are dispersed and redundant.  Most worms thrash when injured; treat as a d6 attack to any surrounding hex, though the creature really isn't aiming.  When not injured, will attempt to swallow living creature nearest its mouth (4vDx to dodge).  If swallowed, victim takes 2 hits/turn (armor doesn't help) until dead or cut out of one of its stomachs.  Victim cannot move inside, but can use any talents or abilities which do not require movement (such as fire)."),
               ('Worm',             'Brown',               15, 10,  1,  8,       8, 0,  [6.0],       0, [],     0, "Critical hits don't apply - worms' critical parts are dispersed and redundant.  Most worms thrash when injured; treat as a d6 attack to any surrounding hex, though the creature really isn't aiming.  Hitting a brown worm with a normal metal weapon is a bad idea; after 12 turns, the weapon will be rusted beyond use.  Also, normal metal armor will rust to powder within 24 turns of being hit by a thrashing brown worm."),
               ('Worm',             'Spiked',              15, 10,  1,  8,       8, 0,  [6.0],     5.5, [],     0, "Critical hits don't apply - worms' critical parts are dispersed and redundant.  Most worms thrash when injured; treat as a d6 attack to any surrounding hex, though the creature really isn't aiming.  When injured, tries to sting whatever is nearest its tail (as a free second attack after thrashing) with poison."),
               ( None,              'Wraith',              12, 10,  8, 10,       1, 0,  [],          0, [],     0, 'Insubstantial; can only attack or be attacked using mental abilities.'),
               ( None,              'Wyvern',              16, 12, 12, 13, '6/12',  2,  [6.0],     7.5, [],     0, 'Like a 2-hex dragon without claws or breath, but with a poisonous stinger.  Capable of flying.'),
               ( None,              'Yeti',                24, 14, 10, 16,      12, 3, [10.0],       0, [],     0, 'This is a MEAN Sasquatch.  Always has Stealth 5 and Leadership 2.  Typically use clubs for combat.  High probability (80%) of traps in room (d4 traps at random locations).'),
               ( None,              'Zombie',              16, 10,  0,  8,      10, 0, [11.5],       0, [10.5], 0, 'Fire inflicts double damage.'),
              ]

    def __init__(self, name=None, subtype=None):
        self._getinfo(name, subtype)
        Creature.__init__(self, self.name, self.stats, self.details)
        self._handlespecial()

    def _getinfo(self, name, subtype):
        listing = self._pickcreature(name, subtype)
        (self.subtype, self.name) = listing[:2]
        (ST, DX, IQ, PP, MA) = listing[2:7]
        (hit, damage, poison, altdamage, altpoison) = listing[7:12]
        self.stats = StatSet(ST, DX, IQ, PP, hit, damage, poison,
                             altdamage, altpoison, MA)
        self.details = listing[12]

    def _pickcreature(self, name, subtype):
        mylist = self.animals
        if subtype is not None:
            mylist = [L for L in self.animals if L[0] == subtype]
            if not mylist:
                raise CreatureError("Invalid non-trainable creature" +
                                    " type %s" % subtype)
        if name is not None:
            for listing in mylist:
                if listing[1] == name:
                    return listing
            else:
                if subtype is not None:
                    raise CreatureError("Invalid non-trainable creature" +
                                        " %s: %s" % (subtype, name)) 
                raise CreatureError("Invalid non-trainable creature %s" %
                                    name)
        return random.choice(mylist)

    def _handlespecial(self):
        self.abilities = []
        self.traps = []
        if self.subtype == 'Beholder':
            remainingIIQ = self.stats.IQ

            # Blue Beholders favor water-based abilities
            if self.name == 'Blue':
                waterabilities = ['Iceball', 'Flight / Swim', 'Ground', 'Proof', 'Sensitize', 'Storm', 'Calm']
                proofelements = ['Water']
                stormelements = ['Water', 'Ice']
                while remainingIIQ > 0 and waterabilities:
                    ability = random.choice(waterabilities)
                    waterabilities.remove(ability)
                    if ability == 'Proof' or ability == 'Sensitize':
                        remainingIIQ = self._addability(remainingIIQ, ability, mental=True,
                                                                      element=random.choice(proofelements))
                    elif ability == 'Storm' or ability == 'Calm':
                        remainingIIQ = self._addability(remainingIIQ, ability, mental=True,
                                                                      element=random.choice(stormelements))
                    else:
                        remainingIIQ = self._addability(remainingIIQ, ability)

            # Green Beholders favor Ethereal Bow
            elif self.name == 'Green':
                IIQ = max([bonus5() for i in range(10)])  # raise chances of higher IIQ
                remainingIIQ = self._addability(remainingIIQ, 'Ethereal Bow', IIQ)

            # Brown Beholders favor Summon
            elif self.name == 'Brown':
                IIQ = max([bonus5() for i in range(10)])  # raise chances of higher IIQ
                remainingIIQ = self._addability(remainingIIQ, 'Summon', IIQ)

            # Albino Beholders always have Vision 5
            elif self.name == 'Albino':
                remainingIIQ = self._addability(remainingIIQ, 'Vision', 5)

            # Fill remaining space with any mental abilities
            while remainingIIQ > 0:
                remainingIIQ = self._addability(remainingIIQ, mental=True)

        elif self.name == 'Djinni' or self.name == 'Shadowight' or self.name == 'Wraith':
            remainingIIQ = self.stats.IQ
            while remainingIIQ > 0:
                remainingIIQ = self._addability(remainingIIQ, mental=True)

        elif self.subtype == 'Golem' and (self.name == 'Silver' or self.name == 'Gold'):
            for i in range(random.randint(3, 5)):
                self._addability(5, mental=True)

        elif self.name == 'Sasquatch' or self.name == 'Yeti':
            self._addability(5, 'Stealth', 5)
            self._addability(2, 'Leadership', 2)
            if random.random() < .80:
                self.traps = [Trap.newtrap(1) for i in range(random.randint(1, 4))]

    def _addability(self, remaining, name=None, IIQ=None, element=None,
                                     mental=False, physical=False):
        if IIQ is None: IIQ = bonus5()
        if IIQ > remaining: IIQ = remaining
        if self.stats.IQ < 8: physical = True
        if name == 'Ax/Mace/Hammer': name = 'Ax/Club/Mace'
        if mental:
            ability = MentalAbility(name, IIQ, element=element)
        elif physical:
            ability = PhysicalAbility(name, IIQ)
        else:
            ability = PhysicalOrMentalAbility(name, IIQ)

        # Duplicate check
        for a in self.abilities:
            if a.duplicate(ability):
                if a.worsethan(ability):
                    self.abilities.remove(a)
                    remaining += a.IIQ
                    if '[+' in str(a):
                        remaining += 1
                else:
                    return remaining

        # Save DCl for Etheral Bow abilities
        if ability.name in MentalAbility.EtherealBow:
            perpoint = EtherealBowDmg(self.stats.IQ)
            total = perpoint * ability.IIQ
            if ((not self.stats.altdamage) or 
                (total > sum(self.stats.altdamage))):
                self.stats.altdamage = [total]

        # Record ability
        self.abilities.append(ability)
        remaining -= ability.IIQ
        if '[+' in str(ability):
            remaining -= 1
        return remaining

    def fullname(self):
        """Return name including subtype, if any."""
        if self.subtype is not None:
            return "%s: %s" % (self.subtype, self.name)
        return self.name

    def __str__(self):
        val = "%s  %s" % (self.fullname(), self.stats)
        if self.details:
            val += wrapped("\n\n  %s" % self.details, indent=2)
        if self.abilities:
            val += "\n\nAbilities:\n"
            for a in self.abilities:
                temp = '  %-30s - %s\n' % (a, a.description(withname=False))
                val += wrapped(temp, indent=35)
        if self.traps:
            val += "\n\nTraps:\n"
            for t in self.traps:
                val += "  %s\n" % t
        return val

