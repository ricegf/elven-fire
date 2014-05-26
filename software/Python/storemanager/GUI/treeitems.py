import os
from operator import attrgetter
from PyQt4 import QtGui, QtCore

from elvenfire.abilities.itemabilities import WeaponAbility
from elvenfire.artifacts.potion import *
from storemanager.locations import store
from storemanager.locations.university import Class
from storemanager.stockitems import _StockItem
from storemanager.stockitems.special import SpecialArtifactStockItem, STBatteryStockItem, TrainableAnimalStockItem
from storemanager.stockitems.combat import WeaponStockItem, ArmorStockItem
from storemanager.stockitems.greater import RodStockItem, RingStockItem
from storemanager.stockitems.lesser import GemStockItem, AmuletStockItem
from storemanager.stockitems.written import ScrollStockItem, BookStockItem
from storemanager.stockitems.potion import *

class AbilityTree (QtGui.QTreeWidgetItem):

    # Columns:
    col_icon = 0  # not used
    col_name = 1
    col_FMV = 2
    col_price = 3  # not used

    def __init__(self, parent, ability):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.ability = ability
        if 'item' in dir(parent):
            self.item = parent.item
        if 'store' in dir(parent):
            self.store = parent.store
        if 'town' in dir(parent):
            self.town = parent.town

        self.setText(self.col_name, str(ability))
        self.setToolTip(self.col_name, str(ability.description()))
        self.setText(self.col_FMV, str(ability.AC))
        self.setToolTip(self.col_FMV, 'Base AC for this ability')

        # Special: Enhanced has sub-abilities
        if isinstance(ability, WeaponAbility) and self.type == 'Enhanced':
            if len(ability.abilities) > 1:
                try:
                    ability.abilities.sort(key=attrgetter('IIQ'), reverse=True)
                except AttributeError: pass
                for a in ability.abilities:
                    AbilityTree(self, a)


class ItemTree (QtGui.QTreeWidgetItem):

    iconlookup = {RodStockItem : 'rod.png',
                  TrainableAnimalStockItem : 'animal.png',
                  RingStockItem : 'ring.png',
                  ArmorStockItem : 'shield.png',
                  WeaponStockItem : 'weapon.png',
                  GemStockItem : 'gem.png',
                  BookStockItem : 'book.png',
                  ScrollStockItem : 'scroll.png',
                  SpecialArtifactStockItem : 'magic.png',
                  PotionStockItem : 'potion.png',
                  AmuletStockItem : 'amulet.png',
                  STBatteryStockItem : 'STBattery.png',

                  'Sword' : 'sword.png',
                  'Ax/Mace/Hammer' : 'ax.png',
                  'Pole Weapon' : 'poleweapons.png',
                  #'Unusual Weapon',
                  'Drawn Bow' : 'bow.png',
                  'Cross Bow' : 'crossbow.png',

                  HealingPotion : 'potionblue.png',
                  WeaponPoison : 'potionteal.png',
                  Grenade : 'potionred.png',
                  AttributePotion : 'potionyellow.png',
                  AbilityPotion : 'potionpurple.png',
                  SpecialPotion : 'potiongrey.png',
                 }

    # Columns:
    col_icon = 0
    col_name = 1
    col_FMV = 2
    col_price = 3

    def __init__(self, parent, item, showloc=False):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.item = item
        if 'store' in dir(parent):
            self.store = parent.store
        if 'town' in dir(parent):
            self.town = parent.town

        # Columns:
        if showloc:
            self.col_store = 2
            self.col_town = 3
            self.col_FMV = 4
            self.col_price = 5

        self.stockitem = isinstance(item, _StockItem)  # catch Changling subs

        # Display Icon
        cls = type(item)
        if cls in self.iconlookup:
            filename = self.iconlookup[cls]
            if cls == ArmorStockItem and item.type in item.armortypes:
                filename = 'helmet.png'
            elif cls == PotionStockItem and item.cls in self.iconlookup:
                filename = self.iconlookup[item.cls]
            filename = 'icons/' + filename
            if 'style' in dir(item) and item.style in self.iconlookup:  # Weapon
                filename = 'icons/' + self.iconlookup[item.style]
            if os.path.isfile(filename):
                self.setIcon(self.col_icon, QtGui.QIcon(filename))

            if 'itemtype' in dir(item):
                self.setToolTip(self.col_icon, item.itemtype)
            if cls == ArmorStockItem and item.type in item.shieldtypes:
                self.setToolTip(self.col_icon, 'Shield')
            if cls == PotionStockItem:
                tooltip = str(item.cls)      # "<'something.HealingPotion'>"
                i1 = tooltip.rfind('.')
                i2 = tooltip.find("'", i1)
                tooltip = tooltip[i1+1:i2]   # e.g. 'HealingPotion'
                self.setToolTip(self.col_icon, tooltip)
            if cls == WeaponStockItem:
                self.setToolTip(self.col_icon, item.style)

        # Name & FMV
        name = item.short() if self.stockitem else str(item)
        self.setText(self.col_name, name)
        self.setToolTip(self.col_name, item.description())
        self.setText(self.col_FMV, str(item.value))
        self.setToolTip(self.col_FMV, 'Fair Market Value')
        self.setTextAlignment(self.col_FMV, QtCore.Qt.AlignRight)

        # Price w/Markup
        if self.stockitem:
            self.setText(self.col_price, str(item.price()))
            self.setTextAlignment(self.col_price, QtCore.Qt.AlignRight)
            if item.markup >= 100:
                self.setToolTip(self.col_price, 'Markup: %s%%' % 
                                                (item.markup - 100))
                if item.markup > 115:  # red text
                    self.setTextColor(self.col_price, QtGui.QColor(150, 0, 0))
            else:  # green text
                self.setToolTip(self.col_price, 'Markdown: %s%%' % 
                                                (100 - item.markup))
                self.setTextColor(self.col_price, QtGui.QColor(0, 150, 0))

        # Store & Town
        if showloc:
            if 'store' in dir(item):
                self.setText(self.col_store, str(item.store))
                self.setToolTip(self.col_store, str(item.store.description))
            if 'town' in dir(item):
                self.setText(self.col_town, str(item.town))
                if 'description' in dir(item.town):
                    self.setToolTip(self.col_town, str(item.town.description))

        # Column Widths & Headers
        self.treeWidget().setColumnWidth(self.col_icon, 75)
        if showloc:
            self.treeWidget().setHeaderLabels(('', 'Name', 'Store', 'Town', 
                                               'FMV', 'Price'))
            self.treeWidget().setColumnWidth(self.col_name, 250)
            self.treeWidget().setColumnWidth(self.col_store, 175)
            self.treeWidget().setColumnWidth(self.col_town, 125)
        else:
            self.treeWidget().setHeaderLabels(('', 'Name', 'FMV', 'Price'))
            self.treeWidget().setColumnWidth(self.col_name, 500)

        # Special logic: Changling weapons
        if isinstance(item, WeaponStockItem) and item.changling:
            p = ItemTree(self, item.primaryweapon)  # will be stockitem==False
            s = ItemTree(self, item.secondaryweapon)
            return

        # Show abilities
        if 'abilities' in dir(item) and len(item.abilities) > 1:
            try:
                item.abilities.sort(key=attrgetter('IIQ'), reverse=True)
            except AttributeError: pass
            for ability in item.abilities:
                a = AbilityTree(self, ability)


class HealingPotionTree (ItemTree):

    def __init__(self, parent, store):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.store = store

        # Set icon
        if HealingPotion in self.iconlookup:  # inherited from above
            filename = 'icons/' + self.iconlookup[HealingPotion]
            self.setIcon(self.col_icon, QtGui.QIcon(filename))
            self.setToolTip(self.col_icon, 'HealingPotion')

        # Set name/price
        self.setText(self.col_name, 
                     "Healing Potion (%s doses available)" % 
                     store.healingpotion)
        if 'desc' in dir(HealingPotion):
            self.setToolTip(self.col_name, HealingPotion.desc)
        self.setText(self.col_FMV, '50')
        self.setToolTip(self.col_FMV, 'Fair Market Value, per dose')
        self.setTextAlignment(self.col_FMV, QtCore.Qt.AlignRight)

        # Price w/Markup
        self.setText(self.col_price, str(store.healingprice()))
        self.setTextAlignment(self.col_price, QtCore.Qt.AlignRight)
        if store.healingmarkup >= 100:
            self.setToolTip(self.col_price, 'Per Dose Markup: %s%%' % 
                                            (store.healingmarkup - 100))
            if store.healingmarkup > 115:  # red text
                self.setTextColor(self.col_price, QtGui.QColor(150, 0, 0))
        else:
            self.setToolTip(self.col_price, 'Per Dose Markdown: %s%%' % 
                                            (100 - store.healingmarkup))
            self.setTextColor(self.col_price, QtGui.QColor(0, 150, 0))  # green


class StoreTree (QtGui.QTreeWidgetItem):

    iconlookup = {store.GeneralStore : 'general.png',
                  store.AnimalStore : 'animal.png',
                  store.BookStore : 'book.png',
                  store.PotionStore : 'potion.png',
                  store.PhysicalWeaponStore : 'weapon.png',
                  store.WeaponStore : 'rod.png',
                  store.ArmorStore : 'armorstore.png',
                  store.MagicStore : 'magic.png',
                  store.GemStore : 'gem.png',
                 }

    # Columns:
    col_icon = 0
    col_name = 1
    col_FMV = 2
    col_price = 3

    def __init__(self, parent, store, showitems=True):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.store = store
        if 'town' in dir(parent):
            self.town = parent.town

        cls = type(store)
        if cls in self.iconlookup:
            filename = 'icons/' + self.iconlookup[cls]
            if os.path.isfile(filename):
                self.setIcon(self.col_icon, QtGui.QIcon(filename))
            self.setToolTip(self.col_icon, cls.__doc__)

        self.setText(self.col_name, str(store))
        self.setToolTip(self.col_name, str(store.description))

        if showitems:
            if store.healingpotion > 0:
                HealingPotionTree(self, store)
            for item in store.getitems():
                i = ItemTree(self, item)

    def rename(self, name):
        self.setText(self.col_name, name)


class TownTree (QtGui.QTreeWidgetItem):

    # Columns:
    col_icon = 0
    col_name = 1
    col_size = 2
    col_stores = 3

    def __init__(self, parent, town):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.town = town

        self.setText(self.col_name, str(town.name))
        if 'description' in dir(town):
            self.setToolTip(self.col_name, town.description)
        self.setText(self.col_size, str(town.size))
        self.setText(self.col_stores, str(len(town.stores)))
        for store in town.stores:
            s = StoreTree(self, store, showitems=False)
            s.town = town

        # Column Headers & Widths
        self.treeWidget().setHeaderLabels(('', 'Name', 'Size', '# Stores'))
        self.treeWidget().setColumnWidth(self.col_icon, 70)
        self.treeWidget().setColumnWidth(self.col_name, 300)
        self.treeWidget().setColumnWidth(self.col_size, 50)
        self.treeWidget().setColumnWidth(self.col_stores, 50)
        self.setTextAlignment(self.col_size, QtCore.Qt.AlignCenter)
        self.setTextAlignment(self.col_stores, QtCore.Qt.AlignCenter)

    def rename(self, name):
        self.setText(self.col_name, name)



class CriteriaTree (QtGui.QTreeWidgetItem):

    def __init__(self, parent, criterion):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.criterion = criterion

        # Columns:
        col_icon = 0  # not used
        col_name = 1

        self.setText(col_name, str(criterion))

        if 'criteria' in dir(criterion):
            for crit in criterion.criteria:
                CriteriaTree(self, crit)


class UniversityTree (QtGui.QTreeWidgetItem):

    def __init__(self, parent, university):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.store = university

        # Columns:
        col_icon = 0  # not used
        col_name = 1
        col_FMV = 2
        col_price = 3

        self.setText(col_name, university.name)

        for day in range(5):
            dayname = Class.Days[day]
            UniversityDayTree(self, dayname, university.getitems(day))


class UniversityDayTree (QtGui.QTreeWidgetItem):

    def __init__(self, parent, dayname, courses):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.university = parent.store

        # Columns:
        col_icon = 0  # not used
        col_name = 1
        col_FMV = 2
        col_price = 3

        self.setText(col_name, dayname)

        for course in courses:
            i = QtGui.QTreeWidgetItem(self)
            i.item = course
            i.setText(col_name, str(course.name))
            i.setText(col_price, str(course.value))


