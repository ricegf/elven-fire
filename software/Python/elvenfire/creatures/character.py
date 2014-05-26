import random

from elvenfire import bonus5
from elvenfire.utilities import wrapped
from elvenfire.creatures.basics import StatSet, Creature
from elvenfire.artifacts.combat import Weapon, Armor
from elvenfire.artifacts.special import SpecialArtifact, STBattery
from elvenfire.abilities.charabilities import *
from elvenfire.creatures.trainable import TrainableAnimal


class Character (Creature):

    """A creature capable of learning character abilities (PC or NPC).

    New attributes:
        abilities -- current Physical/Mental Abilities known
        inventory -- weapons, armor, and artifacts on the character
        equipped  -- items that are currently ready for use
        pets      -- trainable animals kept with Animal Handler

    """

    raceoptions = {}

    #                            ST  DX  IQ
    genderoptions = {'Male' :   ( 0,  0,  0),
                     'Female' : (-1, +1,  0)}

    def __init__(self, name=None, race=None, gender=None, charlevel=0):
        if race is None:
            race = random.choice([k for k in self.raceoptions.keys()])
        if gender is None:
            gender = random.choice([k for k in self.genderoptions.keys()])
        if name is None:
            name = race

        self.name = name
        self.race = race
        self.gender = gender

        stats = self._randomizestats(race, gender, charlevel)
        Creature.__init__(self, name, stats, self.details)

        self.abilities = []
        self.inventory = []
        self.equipped = []
        self.pets = []

        # 10% chance of "pure wizard" for IQ >= 14
        if self.stats.IQ >= 14 and random.randint(1, 10) == 1:
            self._wizardize()
        else:
            self._randomizeequipment()
            self._randomizeabilities()

        self._setpets()

    def __str__(self):
        val = ''
        if self.name != self.race:
            val += '%s\n' % self.name
        val = "%s (%s) %s\n" % (self.race, self.gender, self.stats)
        if self.details:
            temp = 'Native Abilities: %s' % self.details
            val += wrapped(temp, indent=18) + '\n'
        val += '\n\nInventory:  (E indicates Equipped)\n'
        for item in self.inventory:
            val += ('-E-' if item in self.equipped else '---') + str(item)
            val += '\n'
        val += '\n\nAbilities:\n'
        for abil in self.abilities:
            temp = '  %-30s - %s\n' % (abil, abil.description(withname=False))
            val += wrapped(temp, indent=35)
        if self.pets:
            val += '\n\nPets:\n'
            for pet in self.pets:
                val += "  %-30s  %s\n" % (pet.fullname(), pet.stats)
                if pet.details:
                    val += wrapped('    %s\n' % pet.details, indent=4)
        return val

    def _randomizestats(self, race, gender, charlevel):
        (ST, DX, IQ, PP, MA, Cash, Details) = self.raceoptions[race]
        (gST, gDX, gIQ) = self.genderoptions[gender]
        ST += gST
        DX += gDX
        IQ += gIQ
        self.bank = Cash
        self.details = Details
        stat = StatSet(ST, DX, IQ, PP, 0, [],  # no hits or damage yet
                       randomize=False)
        stat.randomstats(PP + charlevel, 
                         (1, 1, 1))  # equal opportunity for all stats
        if self.race == 'Prootwaddle':
            stat.enforcemaxIQ(6)
        return stat

    def _wizardize(self):
        remainingIIQ = self.stats.IQ

        # 75% chance of Ethereal Bow
        if random.randint(1, 4) <= 3:
            remainingIIQ = self._addability(remainingIIQ, 'Ethereal Bow')

        # 50% chance of Literacy
        if random.randint(1, 2) == 1:
            remainingIIQ = self._addability(remainingIIQ, 'Literacy')

        # Rest are mental abilities
        while remainingIIQ > 0:
            remainingIIQ = self._addability(remainingIIQ, mental=True)

        # 50% chance of ST Battery
        if random.randint(1, 2) == 1:
            item = STBattery()
            self.inventory.append(item)
            self.equipped.append(item)

        # 1% chance of something special
        if random.randint(1, 100) == 1:
            item = SpecialArtifact()
            self.inventory.append(item)
            self.equipped.append(item)


    def _randomizeequipment(self):

        # Determine primary weapon (10% chance of artifact)
        artifact = (random.randint(1, 10) == 1)
        primary = Weapon(artifact=artifact, maxST=self.stats.ST)
        self.stats.damage = [primary.DCl]
        if primary.changling:
            self.stats.altdamage = [primary.secondaryweapon.DCl]

        # 25% chance of secondary weapon
        secondary = None
        if (random.randint(1, 4) == 1 and not primary.changling):
            artifact = (random.randint(1, 10) == 1)
            while True:
                secondary = Weapon(artifact=artifact, secondary=True, 
                                   maxST=self.stats.ST)
                if ('Bow' in primary.style) != ('Bow' in secondary.style):
                    break
            self.stats.altdamage = [secondary.DCl]

        # 33% chance of armor
        armor = None
        if (random.randint(1, 3) == 1):
            artifact = (random.randint(1, 10) == 1)
            armor = Armor(artifact=artifact, wearer='Character')
            self.stats.hits += armor.hit

        # 33% chance of shield
        shield = None
        if (random.randint(1, 3) == 1 and not primary.twohanded):
            artifact = (random.randint(1, 10) == 1)
            shield = Armor(artifact=artifact, 
                           type=random.choice(Armor.shieldtypes))
            self.stats.hits += shield.hit

        equip = [i for i in (primary, secondary, armor, shield)
                   if i is not None]
        self.inventory.extend(equip)
        if secondary is not None: equip.remove(secondary)
        self.equipped.extend(equip)

    def _addability(self, remaining, name=None, IIQ=None, mental=False,
                                                          physical=False):
        if IIQ is None: IIQ = bonus5()
        if IIQ > remaining: IIQ = remaining
        if self.stats.IQ < 8: physical = True
        if name == 'Ax/Mace/Hammer': name = 'Ax/Club/Mace'
        if mental:
            ability = MentalAbility(name, IIQ)
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
                elif name is not None:
                    return remaining
                else:
                    return self._addability(remaining, name, IIQ, 
                                            mental, physical)

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

    def _randomizeabilities(self):

        remainingIIQ = self.stats.IQ

        # Add "required" abilities
        for item in self.inventory:
            if remainingIIQ <= 0:
                break

            # Weapon ability
            if isinstance(item, Weapon):
                remainingIIQ = self._addability(remainingIIQ, item.style,
                                                physical=True)

                # Check for changling secondary
                if item.changling:
                    if item.changling:
                        a = item.secondaryweapon.style
                        remainingIIQ = self._addability(remainingIIQ, a,
                                                        physical=True)

                # Thrown weapons?
                if item.throwable:
                    remainingIIQ = self._addability(remainingIIQ, 
                                                    'Thrown Weapons',
                                                    physical=True)

            # Shield requires Armor 1
            if isinstance(item, Armor) and item.type in Armor.shieldtypes:
                remainingIIQ = self._addability(remainingIIQ, 'Armor',
                                                physical=True)

        # Fill remaining ability slots
        while remainingIIQ > 0:
            remainingIIQ = self._addability(remainingIIQ)

    def _setpets(self):
        abilitynames = [a.name for a in self.abilities]
        if 'Animal Handler' not in abilitynames:
            return

        availableIQ = self.stats.IQ
        while availableIQ >= 4:
            animal = TrainableAnimal()
            if animal.stats.IQ == 5:
                needed = 10
            elif animal.stats.IQ == 6:
                needed = 6
            else:
                needed = 4
            if availableIQ >= needed:
                self.pets.append(animal)
                availableIQ -= needed


class PlayerCharacter (Character):

    #                                 ST  DX  IQ  ++  MA  Cash  Details
    raceoptions = {'Human'         : ( 8,  8,  8,  8, 10,  800, ''),
                   'Centaur'       : (14, 10,  8,  2, 12,  450, '2-hex; kick attack to rear hex (DCl 4.5)'),
                   'Dwarf'         : (10,  6,  8,  8, 10,  450, 'Dam+1 with ax/mace/hammer; carry double weight'),
                   'Elf'           : ( 6, 10,  8,  8, 12,  450, '+2 MA with non-metal armor'),
                   'Gnoll'         : ( 6, 10,  8,  6, 10,  300, 'Dam+3 with knives/swords'),
                   'Halfling'      : ( 4, 12,  8,  6, 10,  300, '+1 reaction; Dx+3/Dam+1 with physical missile weapons'),
                   'Kobold'        : ( 6, 10, 10,  6, 10,  700, 'available IIQ = IQ + 1'),
                   'Orc'           : ( 8,  8,  8,  8, 10,  150, 'surly and nasty'),
                   'Reptile Man'   : (14,  8,  8,  8, 10,  250, 'tail dmg = 1d6 (rear hex); IQ>16 enables chameleon ability (Dx-4 to hit)'),
                   'Batling'       : ( 6, 10,  8,  6, 10,  450, 'double MA when flying; no Dx penalty in dark or shadow; additional Dx-2 to hit when flying'),
                   'Pixie'         : ( 6, 10,  8,  6, 10,  450, 'double MA when flying; Dx-1 to hit with missile/thrown weapon; IIQ = IQ + 1; max St=10; Dx+3/Dam+1 with Etheral Bow'),
                   'Shape Shifter' : ( 8,  8,  8,  8, 10,  450, 'change into anything (but damage from "natural" attack is HTH+3); if disbelieved, reverts to human form'),
                   'Prootwaddle'   : (10, 10,  6,  4, 10,  150, 'moronic; max IQ=6'),
                   'Gillemrian'    : (10,  8, 10,  4, 10,  400, 'has gills and lungs, cannot drown; Swim 4 at all times; reptile'),
                   'Crushling'     : (10, 10,  6,  4, 10,  400, 'Dx+2 with crushing weapons'),
                   'Anthro Tiger'  : ( 9, 12,  9,  4, 10,  200, 'See in natural dark; +1 dmg with hands; affected by control animal'),
                  }

