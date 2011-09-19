
from PyQt4 import QtGui, QtCore

from elvenfire.storemanager.locations.store import *
from elvenfire.artifacts.special import *
from elvenfire.artifacts.combat import *
from elvenfire.artifacts.greater import *
from elvenfire.artifacts.lesser import *
from elvenfire.artifacts.written import *
from elvenfire.artifacts.potion import *
from elvenfire.storemanager.GUI.search import SearchWidget
from elvenfire.storemanager.GUI.treeitems import *
from elvenfire.storemanager.GUI.additem import AddItemWidget
from elvenfire.storemanager.GUI.commission import CommissionWindow


class NewStoreWidget(QtGui.QWidget):

    storelist = [('General Store', GeneralStore, 'All types of artifact'),
                 ('Animal Store', AnimalStore, 'Trainable animals'),
                 ('Book Store', BookStore, 'Books and scrolls'),
                 ('Potion Store', PotionStore, 'Potions, poisons, and grenades'),
                 ('Weapon Store', PhysicalWeaponStore, 'Physical weapons of all types'),
                 ('Weapons & Rods', WeaponStore, 'Both physical and mental weapons'),
                 ('Armor Store', ArmorStore, 'Armor and shields'),
                 ('Magic Store', MagicStore, 'Small store containing rings, rods, amulets, gems, and special artifacts.'),
                 ('Gem Store', GemStore, 'Carries gems and the occasional strength battery'),
                ]

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setGeometry(300, 200, 500, 150)
        self.window_.setWindowTitle('Create New Store...')
        self.window_.setCentralWidget(self)
        self.center()
        self.window_.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.window_.geometry()
        width = min(size.width(), int(screen.width() * .9))
        height = min(size.height(), int(screen.height() * .9))
        if width != size.width() or height != size.height():
            self.window_.resize(width, height)
            size = self.window_.geometry()
        self.window_.move((screen.width() - size.width()) / 2,
                          (screen.height() - size.height()) / 2)

    def __init__(self, parent, town):
        QtGui.QWidget.__init__(self, parent)
        self.town = town

        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)

        # Store Type
        sbox = QtGui.QHBoxLayout()
        mbox.addLayout(sbox)
        sbox.addWidget(QtGui.QLabel('Type: ', self))
        self.typebox = QtGui.QComboBox(self)
        self.typebox.addItems([s[0] for s in self.storelist])
        self.typebox.setCurrentIndex(random.randint(0, len(self.storelist)-1))
        self.connect(self.typebox, 
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self._randomname)
        sbox.addWidget(self.typebox)

        # Store Size
        sbox.addWidget(QtGui.QLabel('Size: ', self))
        self.sizebox = QtGui.QComboBox(self)
        self.sizebox.addItems(('By Town Size', 'Custom'))
        self.connect(self.sizebox, 
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self._updatesizebox)
        sbox.addWidget(self.sizebox)
        self.sizedice = QtGui.QLineEdit('', self)
        sbox.addWidget(self.sizedice)
        self.sizedice.setEnabled(False)

        # Store Name
        nbox = QtGui.QHBoxLayout()
        mbox.addLayout(nbox)
        nbox.addWidget(QtGui.QLabel('Name: ', self))
        self.namebox = QtGui.QLineEdit('', self)
        nbox.addWidget(self.namebox)

        # Store Description
        nbox = QtGui.QHBoxLayout()
        mbox.addLayout(nbox)
        nbox.addWidget(QtGui.QLabel('Description: ', self))
        self.descbox = QtGui.QLineEdit('', self)
        nbox.addWidget(self.descbox)        

        # Choose random store name
        self.randomname = self.randomdesc = None
        self._randomname()

        # OK
        self.OK = QtGui.QPushButton('Create', self)
        self.connect(self.OK, QtCore.SIGNAL('clicked()'), self.create)
        mbox.addWidget(self.OK)

        self.show()

    def _randomname(self):
        (name, cls, desc) = self.storelist[self.typebox.currentIndex()]
        if self.randomname is None or self.namebox.text() == self.randomname:
            namelist = [s.name for s in self.town.stores]
            for i in range(50):
                newname = cls.randomname(None)
                if newname not in namelist:
                    break
            else:
                newname = ''
            self.randomname = newname
            self.namebox.setText(newname)
        if self.randomdesc is None or self.descbox.text() == self.randomdesc:
            self.randomdesc = cls.defaultdesc(None)
            self.descbox.setText(self.randomdesc)


    def _updatesizebox(self, text):
        if text == 'By Town Size':
            self.sizedice.setEnabled(False)
        else:
            self.sizedice.setEnabled(True)
            if self.sizedice.text() == '':
                self.sizedice.setText("%sd6" % self.town.size)
        

    def create(self):
        name = self.namebox.text()
        desc = self.descbox.text()
        cls = self.storelist[self.typebox.currentIndex()][1]
        if name == '':
            QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                              'Create New Store',
                              'You must enter a store name!', 
                              QtGui.QMessageBox.Ok).exec_()
            return
        elif name in [s.name for s in self.town.stores]:
            res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                   'Rename Store',
                                   '%s already exists in this town!' % name +
                                   ' Are you sure you wish to continue?',
                                   QtGui.QMessageBox.Yes |
                                   QtGui.QMessageBox.No).exec_()
            if res != QtGui.QMessageBox.Yes:
                return
        if self.sizebox.currentText() == 'By Town Size':
            size = self.town.size
        else:
            size = self.sizedice.text()
        store = cls(name, size, desc)
        self.town.addstore(store)
        self.town.save()
        self.emit(QtCore.SIGNAL('store_created'))
        self.window_.close()


class TownWidget(QtGui.QWidget):

    iconlookup = {Rod : 'rod.png',
                  TrainableAnimal : 'animal.png',
                  Ring : 'ring.jpg',
                  Armor : 'shield.png',
                  Weapon : 'weapon.png',
                  Gem : 'gem.jpg',
                  Book : 'book.png',
                  Scroll : 'scroll.jpg',
                  SpecialArtifact : 'magic.png',
                  Potion : 'potion.png',

                  GeneralStore : 'general.png',
                  AnimalStore : 'animal.png',
                  BookStore : 'book.png',
                  PotionStore : 'potion.png',
                  PhysicalWeaponStore : 'weapon.png',
                  WeaponStore : 'rod.png',
                  ArmorStore : 'shield.png',
                  MagicStore : 'magic.png',
                  GemStore : 'gems.jpg',
                 }

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setGeometry(200, 100, 850, 750)
        self.window_.setWindowTitle(self.town.name)
        self.window_.setCentralWidget(self)
        self.center()
        self.window_.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.window_.geometry()
        width = min(size.width(), int(screen.width() * .9))
        height = min(size.height(), int(screen.height() * .9))
        if width != size.width() or height != size.height():
            self.window_.resize(width, height)
            size = self.window_.geometry()
        self.window_.move((screen.width() - size.width()) / 2,
                          (screen.height() - size.height()) / 2)

    def _seticon(self, action, name):
        filename = 'icons/' + str(name)
        if os.path.isfile(filename):
            action.setIcon(QtGui.QIcon(filename))

    def __init__(self, parent, town):
        self.town = town
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent

        # Actions: Update All Stores
        update = QtGui.QAction('&Update All Stores', self)
        update.setShortcut('Ctrl+U')
        self._seticon(update, 'refresh.png')
        update.setToolTip('Update all stores in this town, selling old' +
                          ' and adding new stock as appropriate.')
        update.setStatusTip('Update all stores in this town.')
        update.setWhatsThis('Steps to update each store:\n' +
                            ' (1) Reduce the markup of each item by d6\n' +
                            ' (2) Remove (store dice) / 8 items (round up)\n' +
                            ' (3) Add items as needed to return total' +
                            ' inventory size to (store dice)')

        # Actions: Clear Search Results
        clear = QtGui.QAction('&Clear Search Results', self)
        self._seticon(clear, 'nosearch.png')
        clear.setToolTip('Clear all Search Results from display')
        clear.setStatusTip('Clear all Search Results from display')
        clear.setWhatsThis('Simply removes old search results from the' +
                           ' town display.')

        # Actions: Search Town
        search = QtGui.QAction('&Search Town', self)
        search.setShortcut('Ctrl+F')
        self._seticon(search, 'search.png')
        search.setToolTip('Search all stores for specific item criteria')
        search.setStatusTip('Search all stores in town')
        search.setWhatsThis('Allows you to specify an item you are looking' +
                            ' for, as specifically or generally as you' +
                            ' like, and then searches each store in town' +
                            ' for items that meet your criteria.')

        # Actions: Purchase Item
        purchase = QtGui.QAction('&Purchase Item', self)
        purchase.setShortcut('Ctrl+P')
        purchase.setToolTip('Purchase the selected item')
        purchase.setStatusTip('Purchase the selected item')
        purchase.setWhatsThis('Purchase the selected item, removing it' +
                              ' from the store premanently.')

        # Actions: Sell/Add Item
        additem = QtGui.QAction('Sell/&Add Item', self)
        additem.setShortcut('Ctrl+N')
        additem.setToolTip('Sell an item back to the store')
        additem.setStatusTip("Add a new item to store's inventory")
        additem.setWhatsThis("Sell a character's item to the store on" +
                             ' commission. The item will be added to the' +
                             " store's inventory, and the character will" +
                             ' receive a 60% commission when the item sells.')

        # Actions: New Store
        newstore = QtGui.QAction('&New Store', self)
        self._seticon(newstore, 'newstore.png')
        newstore.setToolTip('Create a new store within this town')
        newstore.setStatusTip('Open a new store within this town')
        newstore.setWhatsThis('Create a new store within this town. A' +
                              ' name and description may be chosen, as' +
                              ' well as a custom size, if desired.')

        # Actions: Rename Store
        renamestore = QtGui.QAction('&Rename Store', self)
        self._seticon(renamestore, 'renamestore.png')
        renamestore.setToolTip('Rename this store')
        renamestore.setStatusTip('Rename this store')
        renamestore.setWhatsThis('Change the name of the selected store.')

        # Actions: Delete Store
        deletestore = QtGui.QAction('&Delete Store', self)
        self._seticon(deletestore, 'deletestore.png')
        deletestore.setToolTip('Delete selected store')
        deletestore.setStatusTip('Permanently delete selected store')
        deletestore.setWhatsThis('Permanently close selected store, removing' +
                                 ' it and all of its contents from the town.')

        # Actions: Leave Town
        leavetown = QtGui.QAction('&Leave Town', self)
        self._seticon(leavetown, 'back.png')
        leavetown.setToolTip('Return to the Continent window')
        leavetown.setStatusTip('Leave this town, saving all changes.')
        leavetown.setWhatsThis('Close this window and return to the town' +
                               ' selection screen.')

        # Actions: Print Town
        printtown = QtGui.QAction('&Print Town', self)
        printtown.setShortcut('Ctrl+P')
        printtown.setToolTip('Print this town to a file')
        printtown.setStatusTip('Print this town and its contents to a file')
        printtown.setWhatsThis('Print this town and its contents to a file')

        # Connect Actions
        self.connect(update, QtCore.SIGNAL('triggered()'), self.update)
        self.connect(clear, QtCore.SIGNAL('triggered()'), self._buildtree)
        self.connect(search, QtCore.SIGNAL('triggered()'), self.search)
        self.connect(purchase, QtCore.SIGNAL('triggered()'), self.purchase)
        self.connect(additem, QtCore.SIGNAL('triggered()'), self.additem)
        self.connect(newstore, QtCore.SIGNAL('triggered()'), self.newstore)
        self.connect(renamestore, QtCore.SIGNAL('triggered()'), self.renamestore)
        self.connect(deletestore, QtCore.SIGNAL('triggered()'), self.deletestore)
        #self.connect(leavetown, QtCore.SIGNAL('triggered()'), self.window_.close)
        self.connect(printtown, QtCore.SIGNAL('triggered()'), self.print)


        # Header
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)
        mbox.addWidget(QtGui.QLabel(str(self.town), self))
        hbox = QtGui.QHBoxLayout()
        mbox.addLayout(hbox)
        hbox.addWidget(QtGui.QLabel('Stores:', self), 3)

        # Clear Search Results
        self.clear_btn = QtGui.QPushButton('Clear', self)
        self.clear_btn.setToolTip('Clear all Search Results from window')
        self.connect(self.clear_btn, QtCore.SIGNAL('clicked()'), clear.trigger)
        hbox.addWidget(self.clear_btn, 1)

        # Update stores
        self.update_btn = QtGui.QPushButton('UPDATE', self)
        self.update_btn.setToolTip('Update inventory for all stores in this town')
        self.connect(self.update_btn, QtCore.SIGNAL('clicked()'), update.trigger)
        hbox.addWidget(self.update_btn, 2)

        # Store listing
        self.storeselect = QtGui.QTreeWidget(self)
        self.storeselect.setSortingEnabled(True)
        self._buildtree()
        mbox.addWidget(self.storeselect)

        # Buttons: Search
        bbox = QtGui.QHBoxLayout()
        mbox.addLayout(bbox)
        self.search_btn = QtGui.QPushButton('Search...', self)
        self.connect(self.search_btn, QtCore.SIGNAL('clicked()'), search.trigger)
        bbox.addWidget(self.search_btn)

        # Buttons: Buy/Sell
        bbox = QtGui.QHBoxLayout()
        mbox.addLayout(bbox)
        self.purchase_btn = QtGui.QPushButton('Purchase', self)
        self.connect(self.purchase_btn, QtCore.SIGNAL('clicked()'), purchase.trigger)
        bbox.addWidget(self.purchase_btn)
        self.sell_btn = QtGui.QPushButton('Sell Item...', self)
        self.connect(self.sell_btn, QtCore.SIGNAL('clicked()'), additem.trigger)
        bbox.addWidget(self.sell_btn)

        # Buttons: Store manipulation
        bbox = QtGui.QHBoxLayout()
        mbox.addLayout(bbox)
        self.newstore_btn = QtGui.QPushButton('New Store...', self)
        self.connect(self.newstore_btn, QtCore.SIGNAL('clicked()'), 
                     newstore.trigger)
        bbox.addWidget(self.newstore_btn)
        self.rename_btn = QtGui.QPushButton('Rename Store', self)
        self.connect(self.rename_btn, QtCore.SIGNAL('clicked()'), 
                     renamestore.trigger)
        bbox.addWidget(self.rename_btn)
        self.delete_btn = QtGui.QPushButton('Delete Store', self)
        self.connect(self.delete_btn, QtCore.SIGNAL('clicked()'),
                     deletestore.trigger)
        bbox.addWidget(self.delete_btn)

        self.show()
        self.connect(leavetown, QtCore.SIGNAL('triggered()'), self.window_.close)

        # Menu Bar
        menubar = self.window_.menuBar()
        townmenu = menubar.addMenu('Town')
        townmenu.addAction(search)
        townmenu.addAction(clear)
        townmenu.addSeparator()
        townmenu.addAction(printtown)
        townmenu.addSeparator()
        townmenu.addAction(leavetown)
        storemenu = menubar.addMenu('Store')
        storemenu.addAction(newstore)
        storemenu.addAction(renamestore)
        storemenu.addAction(deletestore)
        storemenu.addSeparator()
        storemenu.addAction(update)
        itemmenu = menubar.addMenu('Item')
        itemmenu.addAction(search)
        itemmenu.addSeparator()
        itemmenu.addAction(purchase)
        itemmenu.addAction(additem)
        

    def _selectedstore(self):
        i = self.storeselect.currentItem()
        if 'store' in dir(i):
            return self.storeselect.currentItem().store
        return None

    def _selecteditem(self):
        i = self.storeselect.currentItem()
        if 'item' in dir(i):
            return i.item
        return None

    def _buildtree(self, expand=None):
        self.storeselect.clear()
        self.storeselect.setColumnCount(4)
        for store in self.town.stores:
            s = StoreTree(self.storeselect, store)
            if expand is not None and expand == store:
                s.setExpanded(True)
        self.parent._buildlist()


    ## Town-Wide Actions ##

    def update(self):
        res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'Confirm Update',
                                'Are you SURE you wish to update %s' % self.town
                                + ' at this time? Prices will be updated, and'
                                + ' items may be sold or added when you update.',
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_()
        if (res == QtGui.QMessageBox.Yes):
            removedlist = self.town.update()
            self._buildtree()
            self.town.save()
            CommissionWindow(self, removedlist)

    def search(self):
        sw = SearchWidget(self, self.town)
        self.connect(sw, QtCore.SIGNAL('QuickSearch()'), self.search_done)

    def search_done(self):
        itemlist = self.searchcriteria.search(self.town)
        s = QtGui.QTreeWidgetItem(self.storeselect)
        s.store = self.town
        searchicon = 'icons/search.png'
        if os.path.isfile(searchicon):
            s.setIcon(0, QtGui.QIcon(searchicon))
        s.setText(1, 'Search Results')
        for item in itemlist:
            ItemTree(s, item)
        s.setExpanded(True)
        self.storeselect.scrollToItem(s)

    def print(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Print Town to File',
                                                     '%s.txt' % self.town.name,
                                                     'Text files (*.txt)')
        if filename:
            self.town.print(filename)


    ## Add/Remove Items ##

    def additem(self):
        store = self._selectedstore()
        if store is None:
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning, 
                                     'No Store Selected',
                                     'Please select a store and try again.',
                                     QtGui.QMessageBox.Ok).exec_()
        AddItemWidget(self, store)

    def purchase(self):
        item = self._selecteditem()
        store = self._selectedstore()
        if isinstance(self.storeselect.currentItem(), HealingPotionTree):
            return self.purchase_healingpotion(store)
        if item is None:
            if store is not None:
                msg = "%s is not for sale!" % store.name
            else:
                msg = "Please select an item to puchase"
            QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                              'Purchase Item', msg,
                              QtGui.QMessageBox.Ok).exec_()
            return
        elif isinstance(item, HealingPotion):
            return self.purchase_healingpotion(store)
        res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'Confirm Purchase',
                                'Are you SURE you wish to purchase %s' % 
                                item.short() +
                                ' for $%s?' % item.price(),
                                QtGui.QMessageBox.Yes | 
                                QtGui.QMessageBox.No).exec_()
        if (res == QtGui.QMessageBox.Yes):
            store.purchase(item)
            self.town.save()
            self._buildtree(expand=store)
            if item.commission:
                CommissionWindow(self, [item])

    def purchase_healingpotion(self, store):
        doses, ok = QtGui.QInputDialog.getInt(self, 'Number of Doses',
                                              'How many doses would you' +
                                              ' like to purchase?', 1,
                                              1, store.healingpotion)
        if ok:
            store.healingpotion -= doses
            self.town.save()
            self._buildtree(expand=store)


    ## Store Actions ##

    def newstore(self):
        """Create a new store."""
        sw = NewStoreWidget(self, self.town)
        self.connect(sw, QtCore.SIGNAL('store_created'), 
                     self.new_store_done)

    def new_store_done(self):
        self._buildtree()

    def renamestore(self):
        """Rename the selected store."""
        store = self._selectedstore()
        if store is None:
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning, 
                                     'No Store Selected',
                                     'Please select a store and try again.',
                                     QtGui.QMessageBox.Ok).exec_()
        name, ok = QtGui.QInputDialog.getText(None, "Rename %s" % store.name,
                                     "Enter a new name for %s:" % store.name,
                                     QtGui.QLineEdit.Normal, str(store.name))
        if ok:
            if name in [s.name for s in self.town.stores]:
                res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                       'Rename Store',
                                       '%s already exists in this town!' % name +
                                       ' Are you sure you wish to continue?',
                                       QtGui.QMessageBox.Yes |
                                       QtGui.QMessageBox.No).exec_()
                if res != QtGui.QMessageBox.Yes:
                    return
            store.name = name
            i.rename(str(store))
            self.town.save()
            self.parent._buildlist()

    def deletestore(self):
        """Delete selected store."""
        store = self._selectedstore()
        if store is None:
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning, 
                                     'No Store Selected',
                                     'Please select a store and try again.',
                                     QtGui.QMessageBox.Ok).exec_()
        res = QtGui.QMessageBox(QtGui.QMessageBox.Question,
                                'Confirm %s Deletion' % i.store.name,
                                'Are you SURE you wish to delete %s' % store,
                                QtGui.QMessageBox.Yes | 
                                QtGui.QMessageBox.No).exec_()
        if (res == QtGui.QMessageBox.Yes):
            self.town.stores.remove(store)
            self.town.save()
            self._buildtree()

