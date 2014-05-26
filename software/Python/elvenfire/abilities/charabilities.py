import random

from elvenfire import bonus5
from elvenfire import languages, randomlanguage
from elvenfire.abilities import AbilityError
from elvenfire.abilities.itemabilities import _Ability


def EtherealBowDmg(IQ):
    if IQ <= 8: return 0
    elif IQ <= 11: return 2.5
    elif IQ <= 13: return 3.5
    elif IQ <= 16: return 4.5
    elif IQ <= 19: return 5.5
    else: return 6.5


class _CharacterAbility (_Ability):

    """Abstract class: a character-learnable ability: physical or mental.

    Additional Attributes:
      self.IIQ     -- effective IIQ of ability
      self.baseAC  -- base Ability Cost for this Ability (used to calculate AC)
      self.element -- optional specifier for element or type of ability

    To implement, set the following class attributes:
      abilities    -- {name : baseAC} for all available abilities
      abilitydescs -- {name : (IIQ1_desc, IIQ2_desc, IIQ3_desc, IIQ4_desc, IIQ5_desc)}
                      to establish long-style descriptions of each ability.
      elements     -- {name : [valid_elements]} only as needed
      maxIIQexceptions -- {name : max IIQ} only as needed

    Optionally, override the following to customize weights:
      _randomAbility()
      _randomIIQ()
      _randomElement()

    """

    abilities = {}
    abilitydescs = {}
    elements = {}
    maxIIQexceptions = {}

    def __init__(self, name=None, IIQ=None, element=None):
        """Define all attributes, calculating AC from baseAC and IIQ."""
        self.name = name
        self.IIQ = IIQ
        self.element = element

        # Determine ability name
        if self.name is None:
            self._randomAbility()
            if self.name in self.maxIIQexceptions and self.IIQ is not None:
                if self.IIQ > self.maxIIQexceptions[self.name]:
                    self.__init__(name, IIQ, element)
        elif (self.name not in self.abilities and 
              (self.name + 's') in self.abilities):
            self.name += 's'
        elif self.name not in self.abilities:
            raise AbilityError("Unrecognized character ability '%s'" %
                               self.name)

        # Determine ability IIQ
        if self.IIQ is None:
            self._randomIIQ()
        elif not (isinstance(self.IIQ, int) and 1 <= self.IIQ <= 5):
            raise AbilityError("Invalid IIQ: %s" % self.IIQ)

        # Watch for invalid IIQs
        if (self.name in self.maxIIQexceptions.keys() and
            self.IIQ > self.maxIIQexceptions[self.name]):
            self.IIQ = self.maxIIQexceptions[self.name]

        # Determine the element (if any)
        if self.name in self.elements.keys():
            if self.element is None:
                self._randomElement()
            elif self.element not in self.elements[self.name]:
                raise AbilityError("Invalid element: %s" % self.element)
        elif self.element is not None:
            raise AbilityError("Ability '%s' does not take an element!" %
                               self.name)                 

        # Determine value
        self._lookupAC()
        self._computeAC()

    def __str__(self):
        if self.element is not None:
            return "%s: %s %s" % (self.name, self.element, self.IIQ)
        return "%s %s" % (self.name, self.IIQ)

    def description(self, withname=True):
        """Return long-hand description of the ability."""
        if self.name in self.abilitydescs:
            if withname:
                return "%s: %s" % (str(self), 
                                   self.abilitydescs[self.name][self.IIQ-1])
            else:
                return self.abilitydescs[self.name][self.IIQ-1]
        return str(self)

    def _randomAbility(self):
        """Set self.name and self.baseAC to a random ability."""
        self.name, self.baseAC = random.choice([i for i in self.abilities.items()])

    def _randomIIQ(self):
        """Set self.IIQ to a random (Bonus5) IIQ value."""
        self.IIQ = bonus5()

    def _randomElement(self):
        """Set self.element to a random value for the given ability."""
        self.element = random.choice(self.elements[self.name])

    def _lookupAC(self):
        """Set self.baseAC according to self.name."""
        self.baseAC = self.abilities[self.name]

    def _computeAC(self):
        """Set self.AC based on self.IIQ and self.baseAC."""
        multipliers = (1, 2, 3, 6, 12)
        self.AC = self.baseAC * multipliers[self.IIQ-1]

    def __eq__(self, other):
        """Return boolean indicating if ability name and IIQ are identical."""
        return str(self) == str(other)

    def __hash__(self):
        """Return hash of the ability name and IIQ."""
        return hash(str(self))

    def duplicate(self, other):
        """Return boolean indicating if ability names are identical."""
        if not isinstance(other, _CharacterAbility):
            return False
        return self.name == other.name

    def worsethan(self, other):
        """Return boolean indicating if other has a higher IIQ."""
        other.IIQ > self.IIQ


class PhysicalAbility (_CharacterAbility):

    """A physical Ability."""

    abilities = {'Sword' : 500, 'Ax/Club/Mace' : 500, 
                 'Pole Weapons' : 500, 'Unusual Weapons' : 500,
                 'Thrown Weapons' : 500, 'Drawn Bows' : 500,
                 'Cross Bows' : 500, 'Animal Handler' : 1000,
                 'Armor' : 500, 'Chemist' : 500, 'Leadership' : 500, 
                 'Literacy' : 500, 'Physical Fitness' : 500,
                 'Physicker' : 1000, 'Stealth' : 500, 
                 'Unarmed Combat' : 500}

    maxIIQexceptions = {'Pole Weapons' : 4, 'Leadership' : 3}

    elements = {'Unusual Weapons' : ["Boomerang", "Bola", "Sha-Ken", "Cestus",
                                     "QuarterStaff", "Lasso", "Whip", "Nunchuks",
                                     "Blowgun"],
                'Literacy' : languages}

    abilitydescs = {'Sword' : (
                         'Ability to use the knife or a single-handed weapon',
                         'Ability to use any sword, including 2-handed',
                         'Add +1 to normal damage',
                         '+1 damage; critical hits (double damage on 7/6/5,' +
                         ' triple on 4, quadruple on 3)',
                         '+1 damage; critical hits; use two single-handed' +
                         ' weapons, one in each hand. You may attack with' +
                         ' both, use one to parry (attacker DX-2), or parry' +
                         ' with both (attacker DX-4)'),
                    'Ax/Club/Mace' : (
                         'Ability to use a single-handed weapon',
                         'Ability to use any weapon, including 2-handed',
                         'Add +1 to normal damage',
                         '+1 damage; critical hits (double damage on 7/6/5,' +
                         ' triple on 4, quadruple on 3)',
                         '+1 damage; critical hits; perform sweep attacks' +
                         ' with no Dx penalty'),
                    'Pole Weapons' : (
                         'Ability to use the javelin or spear',
                         'Ability to use any pole weapon except the Naginata',
                         'Ability to use any pole weapon as well as a spear' +
                         ' thrower; throw javelins and spears at Dx+1',
                         '+1 damage; Dx+2 when throwing javelins or spears'),  ## *** No pole weapons 5
                    'Unusual Weapons' : (
                         'Ability to use the unusual weapon of choice',
                         'Dx+1 with chosen weapon',
                         'Dx+2 or critical hits at Dx-1',
                         'Dx+3 or critial hits; increase range by 25%',
                         'Dx+5 or Dx+2 with critical hits; increase range' +
                         ' when thrown by 50%'),
                    'Thrown Weapons' : (
                         'Ability to throw weapons without penalty; ready and' +
                         ' throw in a single turn',
                         'Throw weapon at Dx+1; throw 2 weapons/turn if adjDx' +
                         ' > 20',
                         'Dx+2; +1 damage; throw 2/turn if adjDx>20',
                         'Dx+2; +1 damage; throw 2/turn if adjDx>20; Critical' +
                         ' hits (double damage on 7/6/5, triple on 4,' +
                         ' quadruple on 3)',
                         'Dx+3; +2 damage; critical hits; throw 2/turn if' +
                         ' adjDx>20'),
                    'Drawn Bows' : (
                         'Ability to use the sling or short bow',
                         'Ability to use any drawn bow',
                         'Dx+1 or critical hit at Dx-2',
                         'Dx+3 or critical hit; increase range by 25%; Dx-1' +
                         ' to fire an additional arrow per round; can set' +
                         ' IQ/5 arrows in one combat phase, then fire all' +
                         ' simultaneously in the next at Dx-2 (but with' +
                         ' thrown weapon ranges)',
                         'Dx+5 or critical hit at Dx+2; increase range by' +
                         ' 50%; may fire additional arrow per round with no' +
                         ' penalty; can set IQ/5 arrows in one combat phase,' +
                         ' then fire all simultaneously in the next with no' +
                         ' Dx penalty (but with thrown weapon ranges)'),
                    'Cross Bows' : (
                         'Ability to use any single crossbow except cranequin',
                         'Ability to use any crossbow; all but cranequin are' +
                         ' at Dx+1',
                         'DX+2 or critical hit',
                         'DX+3 or critical hit at Dx+1; increase range by 25%',
                         'DX+5 or critical hit at Dx+3; increase range by 50%'),
                    'Animal Handler' : (
                         'Ability to manage / train a normal number of animals',
                         'Ability to ride a normal riding animal without' +
                         ' falling off; 3vDx to avoid falling if attacking' +
                         ' or attacked.',
                         'No saving rolls when attacking or being attacked' +
                         ' while riding; may ride rare animals; +2 to all' +
                         ' obedience rolls; heal 1 hit on an animal (takes' +
                         ' 5 minutes and a first aid kit)',
                         'No obedience or saving rolls required; may ride any' +
                         ' riding animal; heal 2 hits on animals; confuse' +
                         ' an animal with 3vs(your IQ - their IQ), forcing' +
                         ' the animal to end each movement at least 2 hexes' +
                         ' further away from you; mimic any normal animal' +
                         ' sound, causing animal to hesitate and not attack' +
                         ' for first round - or for second if not attacked',
                         'No obedience or saving rolls; ride any mount,' +
                         ' including aerial, without penalty; heal 3 hits' +
                         ' on animals; confuse an animal with 3vs(your IQ -' +
                         ' their IQ), forcing the animal to end each movement' +
                         ' at least 2 hexes further away from you; mimic' +
                         ' any normal animal sound, causing the animal to' +
                         ' hesitate and not attack for first round - or for' +
                         ' second if not attacked first'),
                    'Armor' : (
                         'Ability to use any shield without penalty',
                         'Recognize the value of armor or weapons; repair' +
                         ' normal armor or weapons (1/2 time and 1/4 money' +
                         'of new creation',
                         'Create/repair normal armor and weapons',
                         'Create fine or silver armor and weapons',
                         'Create artifact armor and weapons'),
                    'Chemist' : (
                         'Create simple healing potions and poisons',
                         'Make any simple potions and intermediate poisons',
                         'Make any simple or intermediate potions',
                         'Make any simple or intermediate potions, and' +
                         ' advanced poisons',
                         'Make any potion or poison'),
                    'Leadership' : (
                         "+1 to initiative; 5vIQ to predict opponents' move",
                         "+2 to initiative; 4vIQ to predict opponents' move",
                         "+2 to initiative; 3vIQ to predict opponents' move;" +  ## *** no Leadership 4 or 5
                         " +1 to reaction roll with opposite sex; 3vIQ to" +
                         " befriend given a neutral reaction roll (4vIQ if" +
                         " in combat; 5vIQ if a prisoner) - add difference" +
                         " from neutral reaction roll"),
                    'Literacy' : (
                         'Read and write Common, plus 1 language for each IQ' +
                         ' point over 11',
                         'Read and write Common, plus 2 languages for each' +
                         ' IQ point over 11; copy books or write book pages' +
                         ' from known abilities, binding up to 5 pages per' +
                         ' book',
                         'Read and write Common, plus 3 languages for each' +
                         ' IQ point over 11; copy books or write book pages' +
                         ' from known abilities, binding up to 10 pages per' +
                         ' book; write scrolls up to IIQ 3 from book or' +
                         ' known ability',
                         'Read and write Common, plus 4 languages for each' +
                         ' IQ point over 11; copy books or write book pages' +
                         ' from known abilities, binding up to 15 pages per' +
                         ' book; write any scroll from book or known ability',
                         'Read and write Common, plus 4 languages for each' +
                         ' IQ point over 11; write any book or scroll from' +
                         ' an existing book or known ability; cure 1 hit on' +
                         ' a humanoid or animal (in addition to Physicker' +
                         ' or Animal Handler)'),
                    'Physical Fitness' : (
                         'Swim; -50% chance to fall when climbing',
                         '+1 Hit; +1 MA; climb rope at 1m/turn; swim; -50%' +
                         ' chance to fall when climbing',
                         '+2 Hit; +2 MA; climb rope at 1m/turn; swim; -75%' +
                         ' chance to fall when climbing',
                         '+3 Hit; +3 MA; climb rope at 2m/turn; swim; -75%' +
                         ' chance to fall when climbing; -25% physical' +
                         ' saving rolls',
                         '+3 Hit; +4 MA; climb rope at 2m/turn; swim; never' +
                         ' fall when climbing; -40% physical saving rolls'),
                    'Physicker' : (
                         'Heal 1 hit on a humanoid given 5 minutes and a' +
                         ' first aid kit',
                         'Heal 2 hits on a humanoid; 4vIQ to identify and' +
                         ' administer antidote to a continuing poison',
                         'Heal 3 hits on a humanoid; 3vIQ to cure continuing' +
                         ' poison; 4vIQ to create first aid kit; prepare' +
                         ' simple poisons and healing potions',
                         'Heal 3 hits on a humanoid; no roll to cure' +
                         ' continuing poison; 4vIQ to create first aid kit;' +
                         ' prepare simple or intermediate poisons and healing' +
                         ' potions',
                         'Heal 4 hits on a humanoid; no roll to cure' +
                         ' continuing poison; 4vIQ to create first aid kit;' +
                         ' prepare any poison or healing potion'),
                    'Stealth' : (
                         '-1d6 to notice anything; -1d6 to saving roll when' +
                         ' moving silently; able to pick a lock with the' +
                         " lock's Pick number vs IQ",
                         '-2d6 to detect traps; -1d6 to avoid; Pick-1vIQ to' +
                         ' pick a lock; 4vIQ to detect invisible or unseen' +
                         ' creatures; -1d6 to notice anything; -1d6 to saving' +
                         ' roll when moving silently',
                         '-2d6 to detect traps; -1d6 to avoid; 1/2 dice to' +
                         ' remove; Pick-2vIQ to pick a lock; 3vDx to peek' +
                         ' into room; 4vDx to duck into hiding place; 4vIQ to' +
                         ' detect invisible or unseen creatures; -1d6 to' +
                         ' notice anything; -1d6 to saving roll when moving' +
                         ' silently; set a trap on successful roll to' +
                         ' remove; create a lock up to Pick 5; carry Master' +  ## *** table has IIQ 1 create lock??
                         ' Key with Pick 5 or less',
                         '-3d6 to detect traps; -2d6 to avoid; 1/2 dice to' +
                         ' remove; Pick-2vIQ to pick a lock; 3vDx to peek' +
                         ' into room; 4vDx to duck into hiding place; 4vIQ to' +
                         ' detect invisible or unseen creatures; -1d6 to' +
                         ' notice anything; -1d6 to saving roll when moving' +
                         ' silently; set a trap on successful roll to' +
                         ' remove; create a lock up to Pick 7; carry Master' +
                         ' Key with Pick 7 or less; 3vIQ to pass when' +
                         ' disguised; throw voice (4vIQ or face direction of' +
                         ' voice as start of encounter; may not move or' +
                         ' turn during first round); 4vDx to sneak through' +
                         ' occupied room in leather armor or less',
                         '-3d6 to detect traps; -3d6 to avoid; 1/3 dice to' +
                         ' remove; Pick-3vIQ to pick a lock; 3vDx to peek' +
                         ' into room; 4vDx to duck into hiding place; 4vIQ to' +
                         ' detect invisible or unseen creatures; -1d6 to' +
                         ' notice anything; -1d6 to saving roll when moving' +
                         ' silently; set any trap on 3vDx; create any lock;' +
                         ' carry any Master Key ; 3vIQ to pass when' +
                         ' disguised; throw voice (4vIQ or face direction' +
                         ' of voice as start of encounter; may not move or' +
                         ' turn during first round); 4vDx to sneak through' +
                         ' occupied room in leather armor or less'),
                    'Unarmed Combat' : (
                         '+1 damage using hands',
                         '+2 damage using hands; shield rush using only hands',
                         '+3 damage using hands; victim must make 5vDx or' +
                         ' fall; attacker Dx-2; no side hex; treat rear hex' +
                         ' as side',
                         '+4 damage using hands; victim must make 5vDx or' +
                         ' fall; attacker Dx-4; no side or rear hex',
                         '+5 damage using hands; victim must make 5vDx or' +
                         ' fall; attacker Dx-6; no side or rear hex;' +
                         ' critical hits at Dx-2')}

    def _randomElement(self):
        if self.name == "Literacy":
            self.element = randomlanguage()
        else:
            _CharacterAbility._randomElement(self)


class MentalAbility (_CharacterAbility):

    """A mental Ability.

    New attributes:
      element -- used only for Proof/Storm/Create abilities

    New class attributes:
      EtherealBow -- tuple containing all Ethereal Bow abilities
      elements    -- tuple containing all valid Storm/Proof elements
      createables  -- tuple containing all valid Create elements

    """

    EtherealBow = ('Lightning Bolt', 'Ether Arrow', 'Iceball',
                   'Fireball', 'Boulder')

    elements = {'Proof' : ['Fire', 'Ice', 'Water', 'Electrical'],
                'Create' : ['Fire', 'Shadow', 'Wall']}
    elements['Sensitize'] = elements['Proof']
    elements['Destroy'] = elements['Create']


    abilities = {'Lightning Bolt' : 5000, 'Ether Arrow' : 5000,
                 'Iceball' : 5000, 'Fireball' : 5000, 'Boulder' : 5000,
                 'Aid' : 1000, 'Drain' : 500, 'Avert' : 2000,
                 'Attract' : 1000,  'Beacon' : 7000,
                 'Control Animal' : 2000, 'Create' : 1500,
                 'Destroy' : 750, 'Create Artifact' : 1000,
                 'Destroy Artifact' : 500, 'Flight / Swim' : 5000,
                 'Ground' : 2000, 'Healing' : 1000, 'Lock' : 500,
                 'Knock' : 1000, 'Proof' : 4000, 'Sensitize' : 2000,
                 'Rope' : 1000,  'Untie' : 500, 'Sleep' : 1000,
                 'Awake' : 500, 'Speed' : 1000, 'Slow' : 500,
                 'Stone Flesh' : 3000, 'Storm' : 4000, 'Calm' : 2000,
                 'Summon' : 10000, 'Release' : 5000, 'Teleport' : 7000,
                 'Recall' : 3500, 'Vision' : 1000, 'Blind' : 500}

    abilitydescs = {'Fireball' : (
                         'double damage vs ice; half damage vs fire;' +
                         'Ability to fire the missile',
                         'double damage vs ice; half damage vs fire;' +
                         'Dx+1 with chosen missile',
                         'double damage vs ice; half damage vs fire;' +
                         'Dx+2 or critical hit',
                         'double damage vs ice; half damage vs fire;' +
                         'Dx+3 or critical hit at Dx+1; +25% range; create' +
                         ' rod from known ability or book page',
                         'double damage vs ice; half damage vs fire;' +
                         'Dx+5 or critical hit at Dx+3; +50% range; create' +
                         ' rod from known ability or book page'),
                    'Lightning Bolt' : (
                         'double damage vs metal armor;' +
                         'Ability to fire the missile',
                         'double damage vs metal armor;' +
                         'Dx+1 with chosen missile',
                         'double damage vs metal armor;' +
                         'Dx+2 or critical hit',
                         'double damage vs metal armor;' +
                         'Dx+3 or critical hit at Dx+1; +25% range; create' +
                         ' rod from known ability or book page',
                         'double damage vs metal armor;' +
                         'Dx+5 or critical hit at Dx+3; +50% range; create' +
                         ' rod from known ability or book page'),
                    'Ether Arrow' : (
                         'double damage vs target that absorbs <2 hits;' +
                         'Ability to fire the missile',
                         'double damage vs target that absorbs <2 hits;' +
                         'Dx+1 with chosen missile',
                         'double damage vs target that absorbs <2 hits;' +
                         'Dx+2 or critical hit',
                         'double damage vs target that absorbs <2 hits;' +
                         'Dx+3 or critical hit at Dx+1; +25% range; create' +
                         ' rod from known ability or book page',
                         'double damage vs target that absorbs <2 hits;' +
                         'Dx+5 or critical hit at Dx+3; +50% range; create' +
                         ' rod from known ability or book page'),
                    'Iceball' : (
                         'double damage vs fire; half damage vs ice;' +
                         'Ability to fire the missile',
                         'double damage vs fire; half damage vs ice;' +
                         'Dx+1 with chosen missile',
                         'double damage vs fire; half damage vs ice;' +
                         'Dx+2 or critical hit',
                         'double damage vs fire; half damage vs ice;' +
                         'Dx+3 or critical hit at Dx+1; +25% range; create' +
                         ' rod from known ability or book page',
                         'double damage vs fire; half damage vs ice;' +
                         'Dx+5 or critical hit at Dx+3; +50% range; create' +
                         ' rod from known ability or book page'),
                    'Boulder' : (
                         'if target takes > 1/3 ST damage, 3vDx or falls;' +
                         'Ability to fire the missile',
                         'if target takes > 1/3 ST damage, 3vDx or falls;' +
                         'Dx+1 with chosen missile',
                         'if target takes > 1/3 ST damage, 3vDx or falls;' +
                         'Dx+2 or critical hit',
                         'if target takes > 1/3 ST damage, 3vDx or falls;' +
                         'Dx+3 or critical hit at Dx+1; +25% range; create' +
                         ' rod from known ability or book page',
                         'if target takes > 1/3 ST damage, 3vDx or falls;' +
                         'Dx+5 or critical hit at Dx+3; +50% range; create' +
                         ' rod from known ability or book page'),
                    'Aid' : (
                         'max transfer 2 points; lasts 2 turns',
                         'max transfer 5 points; lasts 3 turns',
                         'max transfer 10 point; lasts 5 turns',
                         'no maximum; lasts 7 turns; may transfer up to 4 MA;' +
                         ' create ST Battery up to 10 points',
                         'no maximum; lasts 10 turns; may transfer up to 6 MA;' +  
                         ' create ST Battery up to 20 points'),
                    'Drain' : (
                         'max transfer 2 points; lasts 2 turns',
                         'max transfer 5 points; lasts 3 turns',
                         'max transfer 10 point; lasts 5 turns',
                         'no maximum; lasts 7 turns; may transfer up to 4 MA',
                         'no maximum; lasts 10 turns; may transfer up to 6 MA'),
                    'Avert' : (
                         'move 2 hexes away per turn',
                         'move 1 MH away the first turn, then 2 hexes/turn',
                         'move 1 MH away per turn; may not attack you',
                         'must flee at full speed every turn, plus one turn' +
                         ' after the spell is released; may not attack you',
                         'may be cast on up to 5 characters; must flee at' +
                         ' full speed every turn, plus one turn after the' +
                         ' spell is released; may not attack you'),
                    'Attract' : (
                         'move 2 hexes toward you per turn',
                         'move 1 MH toward you the first turn, then 2/turn',
                         'move 1 MH toward you per turn; may not attack you',
                         'must approach at full speed every turn; may not' +
                         ' attack you unless first attacked',
                         'must approach at full speed every turn; may not' +
                         ' attack you under any circumstances; when target' +
                         ' reaches you, it must stay at (your choice of) 3,' +
                         ' 2, or 1 hex(es) from you (and frontal if you so' +
                         ' choose)'),
                    'Beacon' : (
                         'maintain one beacon; transfer 100 kg of cargo;' +
                         ' creator must travel',
                         'maintain 2 beacons; transfer 200 kg of cargo' +
                         ' and/or 1 willing passenger; creator must travel',
                         'maintain 3 beacons; transfer 300 kg of cargo' +
                         ' and/or 3 willing passengers',
                         'maintain 5 beacons; transfer 500 kg of cargo' +
                         ' and/or 5 willing passengers',
                         'maintain unlimited beacons; transfer unlimited' +
                         ' cargo and/or willing passengers; transfer one' +
                         ' unwilling creature if it fails 3vIQ saving roll'),
                    'Control Animal' : (
                         'Control weak animals (IQ<=5, ST<13) that miss 3vIQ',
                         'Control normal animals (ST<17) that miss 3vIQ',
                         'Control any normal animal that misses 3vIQ',
                         'Control humanoid that misses 3vIQ',
                         'Control rare creature that misses 3vIQ'),
                    'Create' : (
                         '1 ST per hex; max 1 hex',
                         '1 ST per hex; max 3 hexes',
                         '1 ST per 2 hexes; max (1/2 IQ) hexes',
                         '1 ST per 2 hexes; max IQ hexes (cannot exceed 14)',
                         '1 ST per 3 hexes; max 14 hexes'),
                    'Destroy' : (
                         '1 ST per 2 hexes; max 1 hex',
                         '1 ST per 2 hexes; max 3 hexes',
                         '1 ST per 4 hexes; max (1/2 IQ) hexes',
                         '1 ST per 4 hexes; max IQ hexes (cannot exceed 14)',
                         '1 ST per 6 hexes; max 14 hexes'),
                    'Create Artifact' : (
                         'Sell lesser artifact at 10% above negotiated price',
                         'Sell any artifact at 20% above negotiated price',
                         '+25% artifact sale price; create lesser artifact;' +
                         ' 3vIQ or item is cursed',
                         '+25% artifact sale price; create any artifact;' +
                         ' 3vIQ or item is cursed',
                         '+25% artifact sale price; create any artifact'),
                    'Destroy Artifact' : (
                         '4vIQ to remove ability of lesser artifact',
                         '4vIQ to remove any artifact ability',
                         '3vIQ to remove any artifact ability; 4vIQ to remove' +
                         ' curse from lesser artifact',
                         '3vIQ remove artifact ability; 4vIQ remove curse',
                         '3vIQ remove any artifact ability or curse'),
                    'Flight / Swim' : (
                         'Normal flying/swimming creature may do so with any' +
                         ' weight he can carry',
                         'Non-flying/swimming creature may do so at Dx-4',
                         'Non-flying/swimming creature may do so at Dx-2;' +
                         ' may breathe anywhere for 12 turns',
                         'Non-flying/swimming creature may do so with any' +
                         ' weight he can carry at no Dx penalty; may' +
                         ' breathe anywhere for 12 turns',
                         'Cast on up to 3 creatures at once; non-flying/' +
                         'swimming creature may do so with any weight he' +
                         ' can carry at no Dx penalty; may breathe anywhere' +
                         ' for 12 turns'),
                    'Ground' : (
                         'Normal flying/swimming creature loses the ability,' +
                         ' being returned safely to the ground',
                         'Normal flying/swimming creature loses the ability,' +
                         ' being returned quickly to the ground for d6 damage',
                         'Normal flying/swimming creature loses the ability,' +
                         ' taking d6 damage; Flight/Swim spell is canceled,' +
                         ' returning creature safely to ground',
                         'Normal flying/swimming creature or creature under' +
                         ' Flight/Swim loses the ability, taking d6 damage',
                         'May be cast on up to 3 creatures at once; normal' +
                         ' flying/swimming creature or creature under' +
                         ' Flight/Swim loses the ability, taking d6 damage'),
                    'Healing' : (
                         'Heal 1 character hp for 2 ST',
                         'Heal 1 character hp or minor vision impairment' +
                         ' for 2 ST',
                         'Heal 2 character hp, 1 animal hp, or minor vision' +
                         ' impairment for 2 ST/pt',
                         'Heal 3 character hp at 1 ST/pt; heal 1 animal hp,' +
                         ' minor vision impairment, blindness, or' +
                         ' intermediate poison for 2 ST',
                         'Heal 4 character hp or 2 animal hp at 1 ST/pt;' +
                         ' heal minor vision impairment, blindness, or' +
                         ' poison for 2 ST; create intermediate healing' +
                         ' potions and antidotes'),
                    'Lock' : (
                         'Place a simple mental lock',
                         'Place a simple or intermediate mental lock',
                         'Place any mental lock on a door/lid',
                         'Mentally lock an item to the room it occupies',
                         'Mentally lock an item to the hex it occupies'),
                    'Knock' : (
                         'Mentally open a simple lock',
                         'Mentally open a simple or intermediate lock',
                         'Mentally open any door/lid lock',
                         'Remove IIQ=4 (room) mental lock',
                         'Remove IIQ=5 (hex) mental lock'),
                    'Proof' : (
                         '-1 dam from selected element',
                         '-2 dam from selected element',
                         '-3 dam from selected element; 3vIQ to create a' +
                         ' permanent moving "hole" in storm directly overhead',
                         '-4 dam from selected element; 3vIQ to prevent a' +
                         ' storm of chosen element from forming overhead',
                         'cannot be hurt by chosen element; 3vIQ to prevent' +
                         ' a storm of chosen element forming anywhere in' +
                         ' room or line of sight; etheral arrows of chosen' +
                         ' element will be returned to sender'),
                    'Sensitize' : (
                         '+1 dam from selected element',
                         '+2 dam from selected element',
                         '+3 dam from selected element; cancel storm "hole"' +
                         ' from IIQ 3 Proof',
                         '+4 dam from selected element; override storm' +
                         ' prevention from IIQ 4 Proof; 4vIQ to sensitize' +
                         ' to different element (at +3 damage)',
                         '+5 or double dam (whichever is greater) from chosen' +
                         ' element; cancel effects of any Proof; 4vIQ to' +
                         ' sensitize to different element (at +4 damage)'),     ## *** how does 'cancel effect' work??
                    'Rope' : (
                         'Good for ST <= 16',
                         'Good for ST <= 26',
                         'Good for ST <= 36',
                         'Good for ST <= 50',
                         'Good for all ST; double rope for <=50; triple <=25'),
                    'Untie' : (
                         'Good for ST <= 16',
                         'Good for ST <= 26',
                         'Good for ST <= 36',
                         'Good for ST <= 50',
                         'Good for all ST; double rope for <=50; triple <=25'),
                    'Sleep' : (
                         'Sleep any creature with ST<20',
                         'Sleep for ST<50; freeze for ST<20',
                         'Sleep for any ST; sleep entire MH of ST<40 each;' +
                         ' freeze for ST<50',
                         'Sleep any character or MH; freeze for any ST;' +
                         ' freeze entire MH of ST<40 each',
                         'Sleep or freeze any character or MH; may "play' +
                         ' dead", pretending to be asleep or frozen - ' +
                         ' 4vIQ to disbelieve, or "sleeper" may not be' +
                         ' attacked until s/he is the last one standing.'),
                    'Awake' : (
                         'Awaken any creature with ST<20',
                         'Awaken for ST<50; unfreeze for ST<20',
                         'Awaken for any ST; awaken entire MH of ST<40 each;' +
                         ' unfreeze for ST<50',
                         'Awaken any character or MH; unfreeze for any ST;' +
                         ' unfreeze entire MH of ST<40 each; 3vIQ to' +
                         ' disbelieve when "playing dead" (Sleep IIQ 5)',
                         'Awaken or unfreeze any character or MH; 3vIQ to' +
                         ' disbelieve when "playing dead" (Sleep IIQ 5)'),
                    'Speed' : (
                         "Double or halve target's MA for 4 turns",
                         "Double or halve target's MA for 6 turns; knock" +
                         " target down, doing no damage",
                         "Double or halve target's MA for 6 turns; stop" +
                         " victim completely for 4 turns; knock target" +
                         " down, doing d6 damage",
                         "Double or halve target's MA for 6 turns; stop" +
                         " victim completely for 6 turns; knock target" +
                         " down, doing d6 damage; create 7 hexes of" +
                         " sticky or slippery floor (lasts 12 turns)",
                         "Double or halve target's MA for 6 turns; stop" +
                         " victim completely for 6 turns; knock target" +
                         " down, doing d6 damage; create 7 hexes of" +
                         " sticky or slippery floor (lasts 12 turns)" +
                         " that only applies to enemies"),
                    'Slow' : (
                         "Remove effects of Speed 1 (4 turns)",
                         "Remove effects of Speed 2 (6 turns; knockdown)",
                         "Remove effects of Speed 3 (stop; d6 knockdown)",
                         "Remove effects of Speed 4 (sticky/slippery floor)",
                         "Remove effects of Speed 5 (sticky/slippery floor" +
                         " that only affects enemies)"),
                    'Stone Flesh' : (
                         'Resist 1-5 hits (based on IQ)',
                         'Resist 1-5 hits (based on IQ); reverse missiles',
                         'Resist 1-5 hits (based on IQ); reverse missiles;' +
                         ' avoid critical hits',
                         'Resist 1-5 hits (based on IQ); reverse missiles;' +
                         ' avoid critical hits; do d6 damage with touch',
                         'Resist 1-5 hits (based on IQ); reverse missiles;' +
                         ' avoid critical hits; do 2d6 damage with touch'),
                    'Storm' : (
                         '1 hex; 1 ST; stationary',
                         '3 hexes; 1 ST/hex; Storm MA=1',
                         'max (half IQ) hexes; 1 ST/2 hexes; Storm MA=2',
                         'max IQ hexes (cannot exceed 14); 1 ST/2 hexes;' +
                         ' Storm MA=4',
                         'max 14 hexes; 1 ST/3 hexes; Storm MA=IQ (max 12)'),
                    'Calm' : (
                         'Calm IIQ 1 Storm (1 hex; stationary); 4vIQ to calm' +
                         ' IIQ 2-4',
                         'Calm IIQ 2 Storm (3 hex; MA=1); 4vIQ to calm IIQ 3-4',
                         'Calm IIQ 3 Storm (MA=2); 4vIQ to calm IIQ 4',
                         'Calm IIQ 4 Storm (MA=4); 4vIQ to calm IIQ 5',
                         'Calm any storm of selected element'),
                    'Summon' : (
                         'Summon creatures (based on IQ) at Power/3 ST,' +
                         ' +1 for called/cloned or -2 for image',
                         'Summon creatures (based on IQ) at Power/4 ST,' +
                         ' +1 for called/cloned or -2 for image',
                         'Summon creatures (based on IQ) at Power/5 ST,' +
                         ' +1 for called/cloned or -2 for image',
                         'Summon creatures (based on IQ) at Power/6 ST,' +
                         ' +1 for called/cloned or -2 for image',
                         'Summon creatures (based on IQ) at Power/8 ST,' +
                         ' +1 for called/cloned or -2 for image'),
                    'Release' : (
                         'Requires IQ to summon twice the power of target;' +
                         ' requires 4vIQ to succeed',
                         'Requires minimum IQ to summon the target;' +
                         ' requires 4vIQ to succeed',
                         'Requires minimum IQ to summon the target;' +
                         ' requires 3vIQ to succeed',
                         'Requires IQ to summon half the power of the target;' +
                         ' requires 3vIQ roll, or 2vIQ if IQ is the power',
                         'Requires IQ to summon 1/4 the power of the target;' +
                         ' requires 3vIQ roll, or 2vIQ if IQ is half the' +
                         ' power, or automatic if IQ is equal to power'),
                    'Teleport' : (
                         'Range of 1 MH; 2 ST/MH',
                         'Range of 2 MH; 1 ST/MH',
                         'Range of 3 MH; 1 ST/MH',
                         'Range of 4 MH; 1 ST/2 MH',
                         'Range of 6 MH or room size or line of sight' +
                         ' (whichever is greatest); 1 ST/2 MH; may take' +
                         ' passengers from adjacent hexes for additional 1 ST' +
                         ' per passenger per MH'),
                    'Recall' : (
                         'Recall an opponent with IQ less than yours; 3vIQ' +
                         ' saving roll',
                         'Recall an opponent with IQ <= yours; 4vIQ saving' +
                         ' roll',
                         'Recall an opponent with IQ <= yours + 2; 4vIQ' +
                         ' saving roll',
                         'Recall an opponent with IQ <= yours + 4; 5vIQ' +
                         ' saving roll',
                         'Recall any opponent who misses a 5vIQ saving roll'),
                    'Vision' : (
                         'Create light or see in darkness for 5 hours',
                         'Create light or see in darkness for 5 hours; see' +
                         ' around corners, or see contents of room before' +
                         ' entering',
                         'Create light or see in darkness for 5 hours; see' +
                         ' around corners, or see contents of room before' +
                         ' entering; see through blur, shadow, invisibility,' +
                         ' or insubstantiality for 5 hours; cast blur (Dx-4)' +
                         ' on yourself',
                         'Create light or see in darkness for 5 hours; see' +
                         ' around corners, or see contents of room before' +
                         ' entering; see through blur, shadow, invisibility,' +
                         ' or insubstantiality for 5 hours; cast blur (Dx-4)' +
                         ' on yourself or other creatures; cast invisibility' +
                         ' (Dx-6) or insubstantiality (Dx-4; half damage)' +
                         ' on yourself; heal minor vision impairments',
                         'Create light or see in darkness for 5 hours; see' +
                         ' around corners, or see contents of room before' +
                         ' entering; see through blur, shadow, invisibility,' +
                         ' or insubstantiality for 5 hours; cast blur (Dx-4),' +
                         ' invisibility (Dx-6), or insubstantiality (Dx-4;' +
                         ' half damage)on yourself or other creatures; heal' +
                         ' any vision impairments; see through the eyes of' +
                         ' a controlled creature for 5 hours'),
                    'Blind' : (
                         'Remove Vision 1 effects (create light/see in dark)',
                         'Remove Vision 2 effects (see around corners)',
                         'Remove Vision 3 effects (blur; see through any);' +
                         " minorly impair one character's vision (Dx-2)" +
                         " for 3 hours",
                         'Remove Vision 4 effects; majorly impair one' +
                         " character's vision (Dx-4) for 6 hours",
                         'Remove Vision 5 effects; blind one character (Dx-6)' +
                         " for 12 hours")}

    def __init__(self, name=None, IIQ=None, element=None):
        if name == 'Ethereal Bow':
            name = random.choice(self.EtherealBow)
        _CharacterAbility.__init__(self, name, IIQ, element)


class MentalAbilityWithOpposites (MentalAbility):

    """A MentalAbility that takes opposites into account...

    Extends MentalAbility to allow "Speed [+ Slow]"-style ability pairs.

    Instead of accessing the abilities attribute directly for this class,
    use the getabilities() method to return the "name -> value" mapping.

    """

    pairs = {'Aid' : 'Drain', 'Avert' : 'Attract', 
             'Create' : 'Destroy', 'Create Artifact' : 
             'Destroy Artifact', 'Flight / Swim' : 'Ground',
             'Knock' : 'Lock', 'Proof' : 'Sensitize', 'Rope' : 'Untie',
             'Sleep' : 'Awake', 'Speed' : 'Slow', 'Storm' : 'Calm',
             'Summon' : 'Release', 'Teleport' : 'Recall', 
             'Vision' : 'Blind'}

    def getabilities():
        """Return list of all abilities."""
        list = MentalAbility.abilities.copy()
        for primary, opposite in MentalAbilityWithOpposites.pairs.items():
            name = '%s [+ %s]' % (primary, opposite)
            value = (MentalAbility.abilities[primary] +
                     MentalAbility.abilities[opposite])
            list[name] = value
        return list

    def __init__(self, name=None, IIQ=None, element=None, opposite=None):
        """Set class attributes to include pairs.

        self.abilities = {name : baseAC}, including each "primary [+ opposite]"
        self.pairs = {primary : opposite}

        """
        self.opposite = opposite  # used for random ability generation

        # Build self.abilities [and abilitydescs] from MentalAbility and pairs
        self.abilities = MentalAbility.abilities.copy()  # list without pairs
        for primary, opposite in self.pairs.items():
            pname = '%s [+ %s]' % (primary, opposite)
            value = self.abilities[primary] + self.abilities[opposite]
            self.abilities[pname] = value
            if pname not in self.abilitydescs:
                if primary in self.abilitydescs and \
                   opposite in self.abilitydescs:
                    zipped = zip(self.abilitydescs[primary],
                                 self.abilitydescs[opposite])
                    self.abilitydescs[pname] = ['%s -- OR -- %s' % (p, o) 
                                                for p, o in zipped]
            if primary in self.elements:
                self.elements[pname] = self.elements[primary]

        # Allow opposite= specifier
        if self.opposite and name is not None:
            if name not in self.pairs:
                raise AbilityError("%s has no opposite!" % name)
            name += ' [+ %s]' % self.pairs[name]

        # Set ability
        MentalAbility.__init__(self, name, IIQ, element)

    def _randomAbility(self):
        """Set self.name and self.baseAC, with 1/4 chance of opposite."""
        list = MentalAbility().abilities.copy()   # back to single abilities
        for primary, opposite in self.pairs.items():
            del list[opposite]             # .. without any opposites
        name = random.choice([k for k in list.keys()])
        if name in self.pairs:           # .. add opposite 1/4 of the time
            if self.opposite is None:
                self.opposite = random.randint(1, 4) == 1
            if self.opposite:
                name = '%s [+ %s]' % (name, self.pairs[name])
        self.name = name

    def duplicate(self, other):
        """Return boolean indicating if one ability includes the other."""
        if not isinstance(other, MentalAbility):
            return False
        if MentalAbility.duplicate(self, other):
            return True
        if (self.name in other.name or other.name in self.name):
            if (self.element is None or self.element == other.element):
                return (self.IIQ == other.IIQ)
        return False

    def worsethan(self, other):
        """Return boolean indicating if other is the "better" ability."""
        return other.name not in self.name  # i.e. other is longer name [+]


def PhysicalOrMentalAbility(name=None, IIQ=None, element=None):

    """An Ability that can be either physical or mental, based on a roll."""

    if name is None:
        roll = random.randint(1, 6)
        if roll <= 4:
            return MentalAbilityWithOpposites(name, IIQ, element)
        else:
            return PhysicalAbility(name, IIQ, element)
    elif name in PhysicalAbility.abilities.keys():
        return PhysicalAbility(name, IIQ, element)
    else:
        return MentalAbilityWithOpposites(name, IIQ, element)


def UniversityAbility(name=None, IIQ=None, element=None):

    """A physical or mental ability determined by University rules.

    The standard University Course Catalog table has the following:
      2% chance of each ability
      3% chance of Pole Weapons"""

    threes = ['Pole Weapons', 'Cross Bows', 'Armor', 'Healing', 'Leadership',
              'Literacy', 'Physicker', 'Summon']

    fours = ['Sword', 'Ax/Club/Mace', 'Thrown Weapons', 'Drawn Bows',
             'Animal Handler']

    if name is None:
        abilities = list(PhysicalAbility.abilities.keys()) + list(MentalAbility.abilities.keys())
        for a in MentalAbilityWithOpposites.pairs.values():
            abilities.remove(a)
        abilities = abilities * 2 + threes + fours * 2
        name = random.choice(abilities)
        if name in MentalAbilityWithOpposites.pairs:
            if random.randint(1, 4) == 1:
                name = MentalAbilityWithOpposites.pairs[name]

    if name in PhysicalAbility.abilities:
        return PhysicalAbility(name, IIQ, element)
    else:
        return MentalAbilityWithOpposites(name, IIQ, element)


