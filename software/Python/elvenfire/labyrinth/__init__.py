########## English Niceties ##########

def s(num, name):
    """Return the correct 's' pluralization of name, with a quantity of num.

    s(8, 'bar') = '8 bars'
    s(1, 'bar') = '1 bar'

    """
    if num == 1:
        return "%s %s" % (num, name)
    return "%s %ss" % (num, name)


def es(num, name):
    """Return the correct 'es' pluralization of name, with a quantity of num.

    es(8, 'hex') = '8 hexes'
    es(1, 'hex') = '1 hex'

    """
    if num == 1:
        return "%s %s" % (num, name)
    return "%s %ses" % (num, name)


def an(num, capitalize=False):
    """Return the correct article to match the given number.

    an(8) = 'an 8'
    an(3) = 'a 3'

    """
    if capitalize:
       val = "A"
    else:
       val = "a"
    if num == 8 or num == 11 or num == 18 or (num >= 80 and num <= 89):
        val += "n"
    return "%s %s" % (val, num)


def ea(num):
    """Return 'each' only if num is greater than 1.

    ea(8) = ' each'
    ea(1) = ''

    """
    if num == 1:
        return ""
    return " each"