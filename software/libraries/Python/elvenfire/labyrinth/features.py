import random

from elvenfire.labyrinth import an, es, s


def Columns():
    return "1 column per MH - blocks all movement and attacks"

def Pools():
    size = random.randint(8, 15)
    return "%s-hex pool of water" % an(size, capitalize=True) + \
           " - 4 MA to traverse, or 4vDx to avoid fall"

def RoughFloor():
    size = random.randint(8, 15)
    return "%s of rough floor (dispersed)" % es(size, 'hex') + \
           " - 3 MA to traverse, or 3vDx to avoid fall"

def Bushes():
    size = random.randint(6, 11)
    return "%s of bushes (dispersed) " % es(size, 'hex') + \
           " - block ground movement, Dx-2 to attack behind"

def Boulders():
    size = random.randint(6, 11)
    return s(size, 'boulder') + \
           " - all MA to climb, Dx-4 to attack behind or from behind"

def Pits():
    size = random.randint(12, 16)
    return "%s-hex pit" % an(size, capitalize=True) + \
           " - blocks ground movement, if forced in take 7 [2d6] damage"

def Walls():
    size = random.randint(6, 11)
    return "%s-hex wall" % an(size, capitalize=True) + \
           " - blocks ground movement, Dx-6 to attack target behind wall"

