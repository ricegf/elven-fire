import random
import math
import re

from elvenfire import bonus25
from storemanager import StoreMgrError


class StoreError (StoreMgrError):
    pass


class TownError (StoreMgrError):
    pass


class _Store:

    """Abstract class: store.

    Attributes:
      name          -- name of store
      description   -- brief description of the store and/or its usual contents
      inventory     -- list of items in stock
      healingpotion -- points of healing potion in stock
      healingmarkup -- this week's markup on healing potion (95-120)
      numdice       -- number of dice to roll at each restock
      diesize       -- size of each die to roll at restock

    To implement, override the following:
      randomname()  -- (optional) used to generate a name when none is given
      randomitem()  -- return a random StockItem of your desired type
      defaultdesc() -- return a string describing the contents of the store
                       note that the user may override this description

    (Optional):
      randomdice()    -- determine correct die roll based on .townsize
      sortinventory() -- sort inventory in any order desired for display

    Public Methods:
      Store(name, size) -- initialize the store and generate starting inventory
      .purchase(item)   -- remove selected item from stock
      .update()         -- update available stock, including markdowns
      .getitems()       -- return list of available items

    """

    ## Private Functions

    def __init__(self, name, size, desc=None):

        """Determine initial attributes and inventory.

        name -- desired name of store, or None to generate randomly
        size -- either die rolls ('3d6') or a town size (integer)
        desc -- (optional) brief description of store

        """

        # Determine name & description
        self.name = name
        if self.name is None:
            self.name = self.randomname()
        self.description = desc
        if self.description is None:
            self.description = self.defaultdesc()

        # Determine die rolls based on size
        if 'd' in str(size):
            num, die = size.split('d')
            if num == '':
                num = 1
            self.numdice, self.diesize = int(num), int(die)
        else:
            self.townsize = int(size)
            self.randomdice()

        # Generate starting inventory
        self.inventory = []
        self.healingpotion = 0
        self._sethealingmarkup()
        inventorysize = self._storesize()
        for i in range(inventorysize):
            self._newitem()

    def _storesize(self):
        """Roll the store dice."""
        return sum(random.randint(1, self.diesize) for i in range(self.numdice))

    def _newitem(self):
        """Add a random item to stock, filtering out healing potions."""
        item = self.randomitem()
        if "Healing Potion" in str(item):
            self.healingpotion += item.doses
            return self._newitem()
        self.inventory.append(item)

    def _sethealingmarkup(self):
        self.healingmarkup = random.randint(95, 120)

    def healingprice(self):
        """Return this week's price per dose for healing potion."""
        return round(50 * self.healingmarkup / 100)
        

    ## Overridables

    def randomname(self):
        """Return a randomly generated name for the store."""
        raise NotImplementedError()

    def defaultdesc(self):
        """Return a brief description of the store and its contents."""
        return "A store, with items available for purchase."

    def randomdice(self):
        """Determine store's die rolls based on townsize."""
        self.numdice = self.townsize
        self.diesize = 6

    def randomitem(self):
        """Return an appropriate random item for inventory."""
        raise NotImplementedError()

    def sortinventory(self):
        """Sort inventory in the correct order for display."""
        random.shuffle(self.inventory)

    ## Public Functions

    def getitems(self):
        """Return list of current items for sale."""
        return self.inventory

    def purchase(self, item):
        """Remove item from the store's inventory."""
        if not item in self.inventory:
            if "Healing Potion" in str(item):
                self.healingpotion -= item.doses
            else:
                raise StoreException('Item "%s" is not in inventory of %s!' %
                                     (item, self.name))
        else:
            self.inventory.remove(item)

    def additem(self, item):
        """Add item to store's inventory."""
        if "Healing Potion" in str(item):
            self.healingpotion += item.doses
        else:
            self.inventory.append(item)

    def update(self):

        """Update store, refreshing inventory lists and reducing all markups."""

        # Reduce all markups; re-sort
        for item in self.inventory:
            item.reduce_markup()
        self.inventory.sort()

        # Remove roll/8 items (potion 20% of the time)
        removedlist = []
        removal = math.ceil(self._storesize() / 8)
        if (self.healingpotion > 0 and random.randint(1, 5) == 1):
            potion = bonus25()
            self.healingpotion -= min(self.healingpotion, potion)
            removal -= 1
        if removal > 0:
            self.inventory = self.inventory[removal:]
            removedlist = self.inventory[:removal]

        # Bring store size back up to new roll
        newsize = self._storesize()
        if newsize > len(self.inventory):
            for i in range(newsize - len(self.inventory)):
                self._newitem()

        # Sort appropriately for sale
        self.sortinventory()

        # Set new healing potion markup
        self._sethealingmarkup()

        return removedlist

    def readable(self):
        """Return store contents, in human-readable format."""
        val = "\n\n********************************************************\n"
        val += ' %s (%s items)\n' % (self.name, len(self.inventory))
        val += '********************************************************\n\n'
        if self.healingpotion > 0:
            string = 'points' if self.healingpotion > 1 else 'point'
            string = "%s %s of healing potion" % (self.healingpotion, string)
            val += "%-50s FMV: $50/point\n\n" % string
        for item in self.inventory:
            val += item.readable() + '\n'
        return val

    def __str__(self):
        """Return brief name of store, with number of available items."""
        s = 's' if len(self.inventory) > 1 else ''
        return "%s (%s item%s)" % (self.name, len(self.inventory), s)        
