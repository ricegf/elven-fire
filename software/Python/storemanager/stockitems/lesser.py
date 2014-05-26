
from elvenfire.artifacts.lesser import Amulet, Gem
from storemanager.stockitems import _StockItem, _MultiAbilityStockItem


class GemStockItem (_StockItem, Gem):
    """Gem for sale."""
    def __init__(self, ability=None, IIQ=None):
        Gem.__init__(self, ability, IIQ)
        _StockItem.__init__(self)


class AmuletStockItem (_MultiAbilityStockItem, Amulet):
    """Amulet for sale."""
    def __init__(self, abilities=None):
        Amulet.__init__(self, abilities)
        _MultiAbilityStockItem.__init__(self)
