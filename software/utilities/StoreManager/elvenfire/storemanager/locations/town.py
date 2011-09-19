import random
import pickle
import os

from elvenfire import bonus5
from elvenfire.storemanager.locations import TownError, _Store
from elvenfire.storemanager.locations.store import GeneralStore


class Town:

    """A town containing one or more stores.

    Attributes:
      name   -- name of town
      size   -- size of town (integer 1..5)
      stores -- list of available Stores in town

    """

    def __init__(self, name=None, size=None):
        """Initialize all attributes and generate stores."""
        if name is None:
            name = self.randomname_nodupes()
        self.name = name
        self.stores = []
        if size is None:
            size = self.randomsize()
        self.size = size
        self.pickstores()

    def __random_town_name(self, count=1):
        """Return a random name, getting more creative with a higher count.

        The intention is that each duplicate name returned results in another
        call, with a higher count. An original name will ALWAYS be returned...
        eventually...

        """
        numlist = ['Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh',
                   'Eighth', 'Ninth', 'Tenth', 'Eleventh', 'Twelfth']
        if count <= 50:     # 50 attempts at pure random town names
            return self.randomname()
        elif count <= 100:  # +50 attempts at including a number
            return "%s the %s" % (self.randomname(), random.choice(numlist))
        else:               # oh well, just make something up!
            newname = ''
            length = random.randint(3, int(count/10))
            for i in range(length):
                newname += random.choice('abcdefghijklmnopqrstuvwxyz   ')
            words = newname.split()
            if not words:   # got all spaces!
                return self.__random_store_name(store, count+1)
            return ' '.join([w.capitalize() for w in words])

    def randomname_nodupes(self):
        count = 1
        name = self.randomname()
        while os.path.isfile(self.__filename(name)):
            name = self.__random_town_name(count)
            count += 1
        return name

    def randomname(self):
        """Return a random name for the town."""
        return random.choice(('Sassafras', 'Holliva', 'Europa', 'Nivelle',
                              'Hogwarts', 'Corrat', 'Selena', 'Brobbingdod',
                              'Tarisha', 'Abacad', 'Porringshire', 'Dallas',
                              'Baconegs', 'Hungary', "Wheaten's Mill",
                              "Lake Purity", "Gallahad", "Shawton",
                              'New Curidat', 'Ruins of Curidat', 'Jamesson',
                              'Goblick', 'Quentyn', 'Rattid', 'Layonge',
                              'Connaloy', 'Dober', 'Fellour', 'Nikkit',
                              'Inglewood', 'Logan', 'Drexel', 'Trentston',
                              'Katte', 'Jurish', 'Hillensdale', 'Moorins',
                              'Pixxville', 'Opulenne', 'Fort George',
                              'Treeor', 'Umbridge', 'Valore', 'Wynxin',
                              'York', 'Zulami', 'Xalle'))

    def randomsize(self):
        return bonus5()

    def pickstores(self):
        """Populate self.stores with all available stores."""
        numspecialty = random.randint(self.size-1, self.size**2-self.size)
        self.stores.append(GeneralStore(None, self.size))  # always 1
        stores = _Store.__subclasses__()
        for i in range(numspecialty):
            this = random.choice(stores)
            self.stores.append(this(None, self.size))
        self.__rename_duplicates()

    def addstore(self, store):
        self.stores.append(store)

    def __random_store_name(self, store, count=1):
        """Return a random name, getting more creative with a higher count.

        The intention is that each duplicate name returned results in another
        call, with a higher count. An original name will ALWAYS be returned...
        eventually... But we do try to keep it logical!

        """
        numlist = ['Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh',
                   'Eighth', 'Ninth', 'Tenth', 'Eleventh', 'Twelfth']
        if count <= 25:     # 25 attempts at pure random store names
            return store.randomname()
        elif count <= 75:   # +50 attempts at including a town name
            return "%s of %s" % (store.randomname(), self.randomname())
        elif count <= 150:  # +75 attempts at including a number
            return "%s the %s" % (store.randomname(), random.choice(numlist))
        elif count <= 250:  # +100 attempts at including town & number
            return "%s the %s of %s" % (store.randomname(),
                                        random.choice(numlist),
                                        self.randomname())
        else:               # oh well, just make something up!
            newname = ''
            length = random.randint(3, int(count/10))
            for i in range(length):
                newname += random.choice('abcdefghijklmnopqrstuvwxyz   ')
            words = newname.split()
            if not words:   # got all spaces!
                return self.__random_store_name(store, count+1)
            return ' '.join([w.capitalize() for w in words])

    def __rename_store(self, store, storelist):
        """Randomly rename store such that it has no duplicate in storelist."""
        namelist = [s.name for s in storelist]
        count = 1
        newname = store.randomname()
        while newname in namelist:
            newname = self.__random_store_name(store, count)
            count += 1
        store.name = newname

    def __rename_duplicates(self):
        """Rename stores as necessary to remove any duplicate store names."""
        for i in range(len(self.stores)):
            this_store = self.stores[i]
            others = self.stores[i+1:]
            for other_store in others:
                if this_store.name == other_store.name:
                    self.__rename_store(other_store, self.stores[:i+1])
        # So the list is always duplicate-free up to and including index i

    def update(self):
        """Update all stores in town, refreshing inventory and pricing."""
        removedlist = []
        for store in self.stores:
            removedlist += store.update()
        return removedlist

    def getitems(self):
        """Return a list of all items available for sale within the town."""
        items = []
        for store in self.stores:
            items.extend(store.getitems())
        return items

    def __str__(self):
        s = 's' if len(self.stores) > 1 else ''
        return "%s (size %s): %s store%s" % (self.name, self.size, 
                                            len(self.stores), s)

    def readable(self):
        val = "\n\nTown: %s\n\n" % self.name
        for store in self.stores:
            val += store.readable() + "\n"
        return val


    def __filename(self, name=None):
        if not os.path.isdir('towns'): os.mkdir('towns')
        if name is None:
            name = self.name
        return os.path.join('towns', '%s.town' % name)

    def save(self):
        filename = self.__filename()
        file = open(filename, 'wb')
        pickle.dump(self, file)
        file.close()

    def load(filename):
        file = open(str(filename), 'rb')
        t = pickle.load(file)
        file.close()
        return t

    def delete(self):
        filename = self.__filename()
        os.remove(filename)

    def purchase(self, item):
        for store in self.stores:
            if item in store.inventory:
                return store.purchase(item)
        raise TownError('Item "%s" cannot be found in any store of %s!' %
                        (item, self.name))

    def print(self, filename):
        file = open(filename, 'w')
        file.write(self.readable())
        file.close()