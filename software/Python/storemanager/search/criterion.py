
import re

from elvenfire.artifacts.combat import *
from elvenfire.artifacts.potion import Potion
from elvenfire.abilities.charabilities import _CharacterAbility
from elvenfire.abilities.charabilities import *
from elvenfire.abilities.itemabilities import *
from storemanager.search import _Criterion


class TextCriterion (_Criterion):

    """Items match if the specified text appears anywhere in the item name."""

    def __init__(self, text):
        """Define text to search for."""
        self.text = text

    def match(self, item):
        """Return boolean indicating whether the text appears for this item."""
        return re.search(self.text, str(item), re.IGNORECASE) is not None

    def __str__(self):
        return 'Text contains: %s' % self.text


class TypeCriterion (_Criterion):

    """Items match if they are of the specified type (class name)."""

    def __init__(self, type):
        """Define type to search for, as a class."""
        self.type = type

    def match(self, item):
        """Return boolean indicating whether item is of the correct type."""
        return isinstance(item, self.type)

    def __str__(self):
        itemtype = str(self.type)   # <class 'Something.Weapon'>
        i1 = itemtype.rfind('.')
        i2 = itemtype.find("'", i1)
        t = itemtype[i1+1:i2]  # Weapon
        return 'Type: %s' % t


class AttributeCriterion (_Criterion):

    """Items which contain an AttributeAbility of the specified type."""

    def __init__(self, attr, minsize=None, maxsize=None):
        """Define attribute [and size] to search for ('ST', 'DX', etc)."""
        self.attr = attr
        self.minsize = minsize
        self.maxsize = maxsize

    def _attrmatch(self, ability):
        """Return boolean indicating if item.size and item.attr are correct."""
        if not (isinstance(ability, AttributeAbility) or
                isinstance(ability, AmuletAbility)):
            return False
        if 'attr' not in dir(ability) or 'size' not in dir(ability):
            return False
        if self.attr != ability.attr:
            return False
        if self.minsize is not None:
            if self.minsize > ability.size:
                return False
        if self.maxsize is not None:
            if self.maxsize < ability.size:
                return False
        return True

    def match(self, item):
        """Return boolean indicating whether item has a matching AttrAbility."""
        if 'ability' in dir(item):
            if self._attrmatch(item.ability):
                return True
        if 'abilities' in dir(item):
            for ability in item.abilities:
                if self._attrmatch(ability):
                    return True
        return False

    def __str__(self):
        if self.attr is None:
            val = 'Any Attribute +'
        else:
            val = '%s +' % self.attr
        if self.minsize is not None and self.minsize == self.maxsize:
            return '%s+%s' % (self.attr, self.minsize)
        elif self.minsize is not None and self.maxsize is not None:
            val += ' %s-%s' % (self.minsize, self.maxsize)
        elif self.minsize is not None:
            val += ' %s' % self.minsize
        elif self.maxsize is not None:
            val += ' %s' % self.maxsize
        return val


class WeaponClassCriterion (_Criterion):

    """Weapons of the class specified (e.g. 'Unusual Weapon').

    May not return Changling weapons correctly.

    """

    def __init__(self, style):
        """Define class to search for (e.g. 'Unusual Weapon')."""
        self.style = style

    def match(self, item):
        """Return boolean indicating whether item is Weapon of correct class."""
        if not isinstance(item, Weapon):
            return False
        if item.changling:
            return (self.match(item.primaryweapon) or 
                    self.match(item.secondaryweapon))
        return item.type in item.weaponlist(self.style)

    def __str__(self):
        return 'Weapon style: %s' % self.style


class WeaponTypeCriterion (_Criterion):

    """Weapons of the exact type specified (e.g. 'Great Sword')."""

    def __init__(self, type):
        """Define type to search for (e.g. 'Great Sword')."""
        self.type = type

    def match(self, item):
        """Return boolean indicating whether item is Weapon of correct type."""
        if not isinstance(item, Weapon):
            return False
        if item.changling:
            return (self.match(item.primaryweapon) or 
                    self.match(item.secondaryweapon))
        if self.type == 'Trident' or self.type == 'Net':
            return self.type in item.type
        return item.type == self.type

    def __str__(self):
        return 'Weapon type: %s' % self.type


class ArmorTypeCriterion (_Criterion):
 
    """Armor/shields of the exact type specified (e.g. 'Small Shield')."""

    def __init__(self, type):
        """Define type to search for (e.g. 'Small Shield')."""
        self.type = type

    def match(self, item):
        """Return boolean indicating if item is Armor/Shield of correct type."""
        if not isinstance(item, Armor):
            return False
        return item.type == self.type

    def __str__(self):
        return 'Armor/shield type: %s' % self.type


class ArmorWearerCriterion (_Criterion):

    """Armor/shields for 'Character' or for 'Mount'."""

    def __init__(self, wearer):
        """Define wearer: 'Character' or 'Mount'."""
        self.wearer = wearer

    def match(self, item):
        """Return boolean indicating whether item is Armor of correct wearer."""
        if not isinstance(item, Armor):
            return False
        if item.wearer is None:
            return False
        return item.wearer == self.wearer

    def __str__(self):
        return 'Armor wearer: %s' % self.wearer


class CharacterAbilityCriterion (_Criterion):

    """Character ability of the specified name and/or IIQ.

    If neither name nor IIQ are specified, ANY CharacterAbility will be
    considered a match.

    """

    def __init__(self, name=None, minIIQ=None, maxIIQ=None):
        """Define name and/or IIQ of desired ability."""
        self.name = name
        self.minIIQ = minIIQ
        self.maxIIQ = maxIIQ

    def _abilitymatch(self, ability):
        """Return boolean indicating if ability matches the criteria."""
        if isinstance(ability, WeaponAbility) and ability.type == 'Enhanced':
            for a in ability.abilities:
                if self._abilitymatch(a):
                    return True
            return False
        if not isinstance(ability, _CharacterAbility):
            return False
        if self.name is not None:
            if self.name != ability.name:
                return False
        if self.minIIQ is not None:
            if self.minIIQ > ability.IIQ:
                return False
        if self.maxIIQ is not None:
            if self.maxIIQ < ability.IIQ:
                return False
        return True

    def match(self, item):
        """Return boolean indicating whether item has specified ability."""
        if 'ability' in dir(item):
            if self._abilitymatch(item.ability):
                return True
        if 'abilities' in dir(item):
            for ability in item.abilities:
                if self._abilitymatch(ability):
                    return True
        return False

    def __str__(self):
        val = ''
        if self.name is not None:
            val += '%s ' % self.name
        else:
            val += 'Any Ability '
        if self.minIIQ is not None and self.minIIQ == self.maxIIQ:
            val += 'IIQ %s' % self.minIIQ
        elif self.minIIQ is not None and self.maxIIQ is not None:
            val += '(%s to %s IIQ)' % (self.minIIQ, self.maxIIQ)
        elif self.minIIQ is not None:
            val += '(%s or greater IIQ)' % self.minIIQ
        elif self.maxIIQ is not None:
            val += '(%s or lower IIQ)' % self.maxIIQ
        return val


class NumAbilitiesCriterion (_Criterion):

    """Item contains the specified number of abilities."""

    def __init__(self, min=None, max=None, exact=None):
        self.min = min
        self.max = max
        if exact is not None:
            self.min = exact
            self.max = exact

    def match(self, item):
        """Return boolean indicating if item has specified number of abilities."""
        if 'abilities' in dir(item):
            num = len(item.abilities)
            if self.min is not None:
                if self.min > num:
                    return False
            if self.max is not None:
                if self.max < num:
                    return False
            return True
        else:  # has 1 ability
            return (self.min is None or self.min <= 1)
            # max cannot be less than 1

    def __str__(self):
        if self.min == self.max:
            return '%s abilities' % self.min
        return '%s-%s abilities' % (self.min, self.max)


class PriceCriterion (_Criterion):

    """Item is within the specified price range."""

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def match(self, item):
        """Return boolean indicating if item is within specified price range."""
        if self.min is not None:
            if self.min > item.price():
                return False
        if self.max is not None:
            if self.max < item.price():
                return False
        return True

    def __str__(self):
        if self.min == self.max:
            return '$%s' % self.min
        return '$%s-$%s' % (self.min, self.max)


class MarkupCriterion (_Criterion):

    """Item is within the specified price range."""

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def match(self, item):
        """Return boolean indicating if markup is within specified range."""
        if self.min is not None:
            if self.min > item.markup:
                return False
        if self.max is not None:
            if self.max < item.markup:
                return False
        return True

    def __str__(self):
        if self.min == self.max:
            return '%s%% markup' % self.min
        return '%s-%s%% markup' % (self.min, self.max)


class ChargesCriterion (_Criterion):

    """Item has the specified number of charges."""

    def __init__(self, min=None, max=None):
        self.min = min
        self.max = max

    def match(self, item):
        """Return boolean indicating if charges are within specified range."""
        if 'charges' not in dir(item):
            return False
        if self.min is not None:
            if self.min > item.charges:
                return False
        if self.max is not None:
            if self.max < item.charges:
                return False
        return True

    def __str__(self):
        if self.min == self.max:
            return '%s charges' % self.min
        return '%s-%s charges' % (self.min, self.max)


class LanguageCriterion (_Criterion):

    """Language on book/scroll."""

    def __init__(self, language):
        """Define language."""
        self.language = language

    def match(self, item):
        """Return boolean indicating whether item is of correct language."""
        if 'language' not in dir(item):
            return False
        return item.language == self.language

    def __str__(self):
        return 'Language: %s' % self.language
