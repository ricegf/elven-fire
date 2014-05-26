
from elvenfire.artifacts.potion import *
from storemanager.stockitems import _StockItem, _MultiAbilityStockItem


class PotionStockItem (_StockItem, Potion):
    """Potion for sale."""
    def __init__(self):
        Potion.__init__(self)
        _StockItem.__init__(self)


class HealingPotionStockItem(PotionStockItem, HealingPotion):
    """Not generally used, as healing potion is treated separately."""
    def __init__(self, doses=None):
        HealingPotion.__init__(self, doses)
        _StockItem.__init__(self)


class WeaponPoisonStockItem(PotionStockItem, WeaponPoison):
    """Weapon poison for sale."""
    def __init__(self, dmg=None, type=None, doses=None):
        WeaponPoison.__init__(self, dmg, type, doses)
        _StockItem.__init__(self)


class GrenadeStockItem(PotionStockItem, Grenade):
    """Grenade for sale."""
    def __init__(self, dmg=None, type=None):
        Grenade.__init__(self, dmg, type)
        _StockItem.__init__(self)


class AttributePotionStockItem(PotionStockItem, AttributePotion):
    """Attribute potion for sale."""
    def __init__(self, ability=None, attr=None, size=None):
        AttributePotion.__init__(self, ability, attr, size)
        _StockItem.__init__(self)


class AbilityPotionStockItem(PotionStockItem, AbilityPotion):
    """Ability potion for sale."""
    def __init__(self, ability=None, IIQ=None):
        AbilityPotion.__init__(self, ability, IIQ)
        _StockItem.__init__(self)


class SpecialPotionStockItem(PotionStockItem, SpecialPotion):
    """Special potion for sale."""
    def __init__(self, name=None):
        SpecialPotion.__init__(self, name)
        _StockItem.__init__(self)

