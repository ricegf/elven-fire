
from elvenfire.artifacts.greater import Ring, Rod
from storemanager.stockitems import _StockItem, _MultiAbilityStockItem


class RodStockItem (_StockItem, Rod):
    """Rod for sale."""
    def __init__(self, charges=None, ability=None, IIQ=None):
        Rod.__init__(self, charges, ability, IIQ)
        _StockItem.__init__(self)


class RingStockItem (_MultiAbilityStockItem, Ring):
    """Ring for sale."""
    def __init__(self, abilities=None):
        Ring.__init__(self, abilities)
        _MultiAbilityStockItem.__init__(self)


