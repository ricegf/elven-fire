
from elvenfire.storemanager.stockitems import _MultiAbilityStockItem
from elvenfire.artifacts.combat import Weapon, Armor


class WeaponStockItem (_MultiAbilityStockItem, Weapon):
    """Enhanced Weapon for sale."""
    def __init__(self, style=None, type=None, abilities=None,
                       secondary=False, secondaryweapon=None):
        _MultiAbilityStockItem.__init__(self)
        Weapon.__init__(self, style=style, type=type, abilities=abilities,
                              secondary=secondary, 
                              secondaryweapon=secondaryweapon)

    def short(self):
        val = _MultiAbilityStockItem.short(self)
        if self.specials > 0:
            val += ' (Special)'
        return val


class ArmorStockItem (_MultiAbilityStockItem, Armor):
    """Enhanced armor or shield for sale."""
    def __init__(self, type=None, wearer=None, abilities=None):
        Armor.__init__(self, type, wearer, abilities)
        _MultiAbilityStockItem.__init__(self)