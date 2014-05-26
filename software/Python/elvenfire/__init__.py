import random

class ELFError (Exception):
    pass


languages = ['Common', 'Elvish', 'Dwarvish', 'Hob/Goblin', 'Orcish', 'Giant',
             'Dragon', 'Troll', 'Troglodyte', 'Gargoyle', 'Fog Runes', 
             'Sasquatch']
rarelanguages = languages[6:]

def randomlanguage():
    roll = random.randint(1, 20)
    if roll <= 12:
        return 'Common'
    elif roll <= 14:
        return 'Elvish'
    elif roll <= 16:
        return 'Dwarvish'
    elif roll == 17:
        return 'Hob/Goblin'
    elif roll == 18:
        return 'Orcish'
    elif roll == 19:
        return 'Giant'
    else:
        return random.choice(rarelanguages)


def bonus5(level=1):
    """Return the result of rolling the Bonus5 table (integer 1..5).

    The result will be weighted toward 1, with a lower level being more strongly
    weighted than a higher level.

    """
    roll = random.randint(1, 20)
    if roll <= level:
        return 5
    elif roll < (2 * level + 1):
        return 4
    elif roll < (3 * level + 3 - max(0, level - 2)):
        return 3
    elif roll < (3 * level + 8):
        return 2
    else:
        return 1


def bonus25(level=1):
    """Return the result of rolling the Bonus25 table (integer 1..25).

    The result will be weighted toward 1, with a lower level being more strongly
    weighted than a higher level.

    """
    roll = random.randint(1, 10)
    if roll == 1 and level > 1:
        return 25
    elif roll <= level:
        return 12 + random.randint(1, 12)
    elif roll <= 1 + level + max(0, level-2):
        return sum(random.randint(1, 12) for i in range(2))
    elif roll <= 3 + level + max(0, level-2):
        return 4 + random.randint(1, 12)
    elif roll <= 5 + level:
        return sum(random.randint(1, 8) for i in range(2))
    elif roll <= min(9, 7 + level):
        return random.randint(1, 12)
    else:
        return random.randint(1, 8)

