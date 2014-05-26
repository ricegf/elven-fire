
from elvenfire.artifacts.written import Scroll, Book
from storemanager.stockitems import _MultiAbilityStockItem


class ScrollStockItem (_MultiAbilityStockItem, Scroll):
    """Scroll for sale."""
    def __init__(self, abilities=None, language=None):
        Scroll.__init__(self, abilities, language)
        _MultiAbilityStockItem.__init__(self)
        self.itemtype += ' (%s)' % self.language


class BookStockItem (_MultiAbilityStockItem, Book):
    """Book for sale."""
    abilityname = 'pages'
    def __init__(self, abilities=None, language=None):
        Book.__init__(self, abilities, language)
        _MultiAbilityStockItem.__init__(self)
        self.itemtype += ' (%s)' % self.language


