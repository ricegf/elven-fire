import random

from elvenfire.artifacts.written import randomlanguage
from elvenfire.labyrinth import s
from elvenfire.labyrinth.containers import ContainerSet


def TreasureType(level):
    return random.choice(('Greater Artifact', 'Lesser Artifact', 'Jewel',
                          'Gold Bar', 'Gold Coin', 'Silver Coin', 
                          'Copper Coin'))


class SpecialArtifact:

    """Special artifacts have unexpected, often permanent, effects."""

    def __init__(self, level):
        self.determine_type(level)
        self.level = level
        # effect will be rolled only on activation

    def __str__(self):
        """Return a description suitable for explanation to the players."""
        val = "Here there be something TRULY special!\n"
        val += "You see %s, which may be activated when you %s.\n" % \
               (self.type, self.activation)
        val += " (if successfully activated, roll d100 for the effects)"
        if 'container' in val:
            val += "\n\nContainer details:\n"
            val += str(ContainerSet(self.level, 1))
        return val

    def determine_type(self, level):
        """Determine the type of structure, and how it will be activated."""
        typeroll = random.randint(1, 100)
        activroll = random.randint(1, 6)
        if typeroll <= 8:
            self.type = 'an altar'
            if activroll <= 3:
                self.activation = 'pray (offer gp)'
            elif activroll == 4:
                self.activation = 'approach (3 hexes)'
            elif activroll == 5:
                self.activation = 'speak the password (5vIQ)'
            else:
                self.activation = 'touch it'
        elif typeroll <= 16:
            num = random.randint(1, 4)
            self.type = s(num, 'archway')
            if activroll <= 4:
                self.activation = 'stand underneath'
            elif activroll == 5:
                self.activation = 'touch it'
            else:
                dmg = random.randint(1, 20)
                self.activation = 'strike it (%s damage at once)' % dmg
        elif typeroll <= 24:
            self.type = 'a container (q.v.)'
            if activroll <= 4:
                self.activation = 'open/hold it'
            elif activroll == 5:
                self.activation = 'add an item (cannot remove later)'
            else:
                self.activation = 'speak ' + randomlanguage()
        elif typeroll <= 31:
            self.type = 'a dome'
            if activroll <= 3:
                self.activation = 'touch it'
            elif activroll <= 5:
                self.activation = 'approach (3 hexes)'
            else:
                dmg = random.randint(1, 12)
                self.activation = 'strike it (%s damage at once)' % dmg
        elif typeroll <= 39:
            self.type = 'a fireplace'
            if activroll <= 3:
                self.activation = 'light a normal fire'
            if activroll == 4:
                self.activation = 'light a magical fire'
            elif activroll == 5:
                self.activation = 'approach (3 hexes)'
            else:
                self.activation = 'touch it'
        elif typeroll <= 47:
            self.type = 'a fountain'
            activroll = random.randint(1, 4)
            if activroll == 1:
                self.activation = 'toss in a %s' % TreasureType(level)
            elif activroll == 3:
                self.activation = 'approach (3 hexes)'
            else:  # 2 || 4??
                self.activation = 'drink from it'
        elif typeroll <= 54:
            num = random.randint(1, 6)
            self.type = s(num, 'painting')
            if activroll <= 3:
                self.activation = 'touch it'
            if activroll == 4:
                self.activation = 'approach (3 hexes)'
            elif activroll == 5:
                self.activation = 'speak ' + randomlanguage()
            else:
                self.activation = 'understand it 4vIQ'
        elif typeroll <= 62:
            num = random.randint(1, 6)
            self.type = s(num, 'statue')
            if activroll == 1:
                self.activation = 'speak ' + randomlanguage()
            elif activroll == 2:
                self.activation = 'climb it (3vDx)'
            if activroll <= 4:
                self.activation = 'approach (3 hexes)'
            else:
                self.activation = 'touch it'
        elif typeroll <= 70:
            self.type = 'a pedestal'
            activroll = random.randint(1, 4)
            if activroll == 1:
                self.activation = 'place a ' + TreasureType(level) + ' upon it'
            elif activroll == 2:
                self.activation = 'stand on it'
            if activroll == 3:
                self.activation = 'approach (3 hexes)'
            else:
                self.activation = 'touch it'
        elif typeroll <= 78:
            num = random.randint(1, 6)
            self.type = s(num, 'pillar')
            if activroll <= 3:
                self.activation = 'touch it'
            elif activroll <= 5:
                self.activation = 'climb it'
            else:
                dmg = random.randint(1, 12)
                self.activation = 'strike it (%s damage at once)' % dmg
        elif typeroll <= 86:
            num = random.randint(1, 12)
            self.type = s(num, 'pool')
            activroll = random.randint(1, 4)
            if activroll == 1:
                self.activation = 'toss in a %s' % TreasureType(level)
            elif activroll == 3:
                self.activation = 'approach (3 hexes)'
            else:  # 2 || 4??
                self.activation = 'drink from it'
        elif typeroll <= 92:
            num = random.randint(1, 8)
            self.type = s(num, 'firepit')
            if activroll <= 3:
                self.activation = 'light a normal fire'
            if activroll == 4:
                self.activation = 'light a magical fire'
            elif activroll == 5:
                self.activation = 'approach (3 hexes)'
            else:
                self.activation = 'touch it (d4 damage)'
        elif typeroll <= 96:
            num = random.randint(1, 4)
            if num == 1:
                self.type = 'a tapestry'
            else:
                self.type = '%s tapestries' % num
            if activroll <= 3:
                self.activation = 'touch it'
            if activroll == 4:
                self.activation = 'approach (3 hexes)'
            elif activroll == 5:
                self.activation = 'speak ' + randomlanguage()
            else:
                self.activation = 'understand it 4vIQ'
        else:
            if random.random() <= 0.05:
                self.type = 'a wishing well'
            else:
                self.type = 'a well'
            if activroll <= 4:
                self.activation = 'toss in a %s' % TreasureType(level)
            elif activroll == 5:
                self.activation = 'toss in a weapon'
            else:
                self.activation = 'drink from it'
