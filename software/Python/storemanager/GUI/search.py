import math

from PyQt4 import QtGui, QtCore

from elvenfire.artifacts.special import *
from elvenfire.artifacts.combat import *
from elvenfire.artifacts.greater import *
from elvenfire.artifacts.lesser import *
from elvenfire.artifacts.written import *
from elvenfire.artifacts.potion import *
from elvenfire.abilities.charabilities import *
from storemanager.search.criterion import *
from storemanager.search.criteriaset import *
from storemanager.GUI.treeitems import *
from storemanager.GUI import GUIError


class MultiAbilityWidget(QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setWindowTitle('Select Multiple Abilities')
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

    def _addability(self, name, layout):
        box = QtGui.QHBoxLayout()
        layout.addLayout(box)

        # Ability Selection
        check = QtGui.QCheckBox(self)
        box.addWidget(check)
        label = QtGui.QLabel(name, self)
        box.addWidget(label)
        box.addStretch(1)

        # IIQ Selection
        min = QtGui.QSpinBox(self)
        min.setValue(1)
        min.setRange(1, 5)
        min.setEnabled(False)
        box.addWidget(min)
        box.addWidget(QtGui.QLabel(' to ', self))
        max = QtGui.QSpinBox(self)
        max.setValue(5)
        max.setRange(1, 5)
        max.setEnabled(False)
        box.addWidget(max)

        # Enable IIQ selection when ability changes
        self.connect(check, QtCore.SIGNAL('stateChanged(int)'),
                     self.enable_IIQ)

        # Save references
        self.widgets[name] = (check, min, max)       

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)
        mbox.addWidget(QtGui.QLabel('Multiple Abilities:', self))

        # Build Ability List
        num = parent.ability.count()
        list = [parent.ability.itemText(i) for i in range(num)]
        if 'Any' in list: list.remove('Any')
        if 'Custom' in list: list.remove('Custom')

        # Determine number of columns
        screen = QtGui.QDesktopWidget().screenGeometry()
        height = min(800, screen.width())
        percolumn = int(height / (100/3))
        self.columns = math.ceil(len(list) / percolumn)
        self.percolumn = math.ceil(len(list) / self.columns)

        # Create and place widgets
        if self.columns == 1:
            cbox = mbox
        else:
            hbox = QtGui.QHBoxLayout()
            mbox.addLayout(hbox)
            cbox = QtGui.QVBoxLayout()
            hbox.addLayout(cbox)
        self.widgets = {}
        count = 0
        for name in list:
            self._addability(name, cbox)
            count += 1
            if count < len(list) and (count % self.percolumn == 0):
                cbox = QtGui.QVBoxLayout()
                hbox.addLayout(cbox)

        # Buttons
        bbox = QtGui.QHBoxLayout()
        mbox.addLayout(bbox)
        and_btn = QtGui.QPushButton('Require ALL of these', self)
        bbox.addWidget(and_btn)
        self.connect(and_btn, QtCore.SIGNAL('clicked()'), self.go_and)
        or_btn = QtGui.QPushButton('Require ANY of these', self)
        bbox.addWidget(or_btn)
        self.connect(or_btn, QtCore.SIGNAL('clicked()'), self.go_or)

        cancel = QtGui.QPushButton('Cancel', self)
        mbox.addWidget(cancel)

        self.show()

        self.connect(cancel, QtCore.SIGNAL('clicked()'), self.window_.close)

    def enable_IIQ(self):
        """Update the enabled/disabled state of each ability."""
        for (checkbox, min, max) in self.widgets.values():
            min.setEnabled(checkbox.isChecked())
            max.setEnabled(checkbox.isChecked())

    def _critlist(self):
        """Return a list of criteria corresponding to the selected abilities."""
        critlist = []
        for name, (checkbox, min, max) in self.widgets.items():
            if checkbox.isChecked():
                critlist.append(CharacterAbilityCriterion(name, min.value(), 
                                                                max.value()))
        return critlist

    def go_and(self):
        critlist = self._critlist()
        if not critlist:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning, 
                              'Nothing Selected',
                              'No abilities selected!',
                              QtGui.QMessageBox.Ok).exec_()
            return
        self.parent.abilitycrit = ANDCriteriaSet(critlist)
        self.emit(QtCore.SIGNAL('ability_selection_done'))
        self.window_.close()

    def go_or(self):
        critlist = self._critlist()
        if not critlist:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning, 
                              'Nothing Selected',
                              'No abilities selected!',
                              QtGui.QMessageBox.Ok).exec_()
            return
        self.parent.abilitycrit = ORCriteriaSet(critlist)
        self.emit(QtCore.SIGNAL('ability_selection_done'))
        self.window_.close()



class MultiAttributeWidget(QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setWindowTitle('Select Multiple Attributes')
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

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)
        mbox.addWidget(QtGui.QLabel('Multiple Attributes:', self))

        # Build Attribute List
        num = parent.attribute.count()
        list = [parent.attribute.itemText(i) for i in range(num)]
        if 'Any' in list: list.remove('Any')
        if 'Custom' in list: list.remove('Custom')
        self.widgets = {}
        for name in list:
            box = QtGui.QHBoxLayout()
            mbox.addLayout(box)

            # Attribute Selection
            check = QtGui.QCheckBox(self)
            box.addWidget(check)
            label = QtGui.QLabel(name, self)
            box.addWidget(label)

            # Bonus Size Selection
            min = QtGui.QSpinBox(self)
            min.setValue(1)
            min.setRange(1, 5)
            min.setEnabled(False)
            box.addWidget(min)
            box.addWidget(QtGui.QLabel(' to ', self))
            max = QtGui.QSpinBox(self)
            max.setValue(5)
            max.setRange(1, 5)
            max.setEnabled(False)
            box.addWidget(max)

            # Enable Size selection when attribute changes
            self.connect(check, QtCore.SIGNAL('stateChanged(int)'),
                         self.enable_size)

            # Save references
            self.widgets[name] = (check, min, max)

        # Buttons
        bbox = QtGui.QHBoxLayout()
        mbox.addLayout(bbox)
        and_btn = QtGui.QPushButton('Require ALL of these', self)
        bbox.addWidget(and_btn)
        self.connect(and_btn, QtCore.SIGNAL('clicked()'), self.go_and)
        or_btn = QtGui.QPushButton('Require ANY of these', self)
        bbox.addWidget(or_btn)
        self.connect(or_btn, QtCore.SIGNAL('clicked()'), self.go_or)

        cancel = QtGui.QPushButton('Cancel', self)
        mbox.addWidget(cancel)

        self.show()

        self.connect(cancel, QtCore.SIGNAL('clicked()'), self.window_.close)

    def enable_size(self):
        """Update the enabled/disabled state of each attribute."""
        for (checkbox, min, max) in self.widgets.values():
            min.setEnabled(checkbox.isChecked())
            max.setEnabled(checkbox.isChecked())

    def _critlist(self):
        """Return a list of criteria corresponding to the selected attributes."""
        critlist = []
        for name, (checkbox, min, max) in self.widgets.items():
            if checkbox.isChecked():
                critlist.append(AttributeCriterion(name, min.value(), 
                                                            max.value()))
        return critlist

    def go_and(self):
        critlist = self._critlist()
        if critlist == []:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning, 
                              'Nothing Selected',
                              'No attributes selected!',
                              QtGui.QMessageBox.Ok).exec_()
            return
        self.parent.attrcrit = ANDCriteriaSet(critlist)
        self.emit(QtCore.SIGNAL('attribute_selection_done'))
        self.window_.close()

    def go_or(self):
        critlist = self._critlist()
        if critlist == []:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning, 
                              'Nothing Selected',
                              'No attributes selected!',
                              QtGui.QMessageBox.Ok).exec_()
            return
        self.parent.attrcrit = ORCriteriaSet(critlist)
        self.emit(QtCore.SIGNAL('attribute_selection_done'))
        self.window_.close()


class SearchWidget(QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        #self.window_.setGeometry(200, 100, 800, 800)
        self.window_.setWindowTitle('Select Search Window...')
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

    def __init__(self, parent, town, simple=False):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.town = town
        self.attrcrit = self.abilitycrit = None
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)
        mbox.addWidget(QtGui.QLabel('Search Criteria:', self))

        # Text Search
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        label = QtGui.QLabel('Text: ', self)
        label.setToolTip('Search for specified text anywhere in item name.')
        box.addWidget(label)
        self.textsearch = QtGui.QLineEdit(self)
        box.addWidget(self.textsearch)

        # Item Type
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        label = QtGui.QLabel('Item Type: ', self)
        label.setToolTip('Search by item type.')
        box.addWidget(label)
        self.itemtype = QtGui.QComboBox(self)
        self.itemtype.addItems(('Any', 'Special Artifact', 'ST Battery',
                                'Weapon', 'Armor/Shield','Amulet', 'Ring',
                                'Rod', 'Book', 'Scroll',  'Gem', 'Potion'))
        box.addWidget(self.itemtype)

        # Price Range
        label = QtGui.QLabel('Price: ', self)
        box.addWidget(label)
        self.minprice = QtGui.QLineEdit(self)
        box.addWidget(self.minprice)
        box.addWidget(QtGui.QLabel(' to ', self))
        self.maxprice = QtGui.QLineEdit(self)
        box.addWidget(self.maxprice)

        # Language
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        box.addWidget(QtGui.QLabel('Language: ', self))
        self.language = QtGui.QComboBox(self)
        self.language.addItem('Any')
        self.language.addItems(languages)
        box.addWidget(self.language)
        self.language.setEnabled(False)

        # Num Charges
        label = QtGui.QLabel('# of Charges: ', self)
        box.addWidget(label)
        self.mincharges = QtGui.QSpinBox(self)
        self.mincharges.setValue(1)
        self.mincharges.setRange(1, 25)
        box.addWidget(self.mincharges)
        label = QtGui.QLabel(' to ', self)
        box.addWidget(label)
        self.maxcharges = QtGui.QSpinBox(self)
        self.maxcharges.setValue(25)
        self.maxcharges.setRange(1, 25)
        box.addWidget(self.maxcharges)
        self.mincharges.setEnabled(False)
        self.maxcharges.setEnabled(False)

        # Markup
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        label = QtGui.QLabel('Markup: ', self)
        box.addWidget(label)
        self.markup = QtGui.QComboBox(self)
        self.markup.addItems(('Any', 'Sale Items', 'Custom'))
        box.addWidget(self.markup)
        label = QtGui.QLabel('Custom: ', self)
        box.addWidget(label)
        self.minmarkup = QtGui.QSpinBox(self)
        self.minmarkup.setValue(100)
        self.minmarkup.setRange(0, 120)
        box.addWidget(self.minmarkup)
        label = QtGui.QLabel('% to ', self)
        box.addWidget(label)
        self.maxmarkup = QtGui.QSpinBox(self)
        self.maxmarkup.setValue(100)
        self.maxmarkup.setRange(0, 120)
        box.addWidget(self.maxmarkup)
        label = QtGui.QLabel('% of FMV')
        box.addWidget(label)
        self.minmarkup.setEnabled(False)
        self.maxmarkup.setEnabled(False)

        # Weapon info
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        label = QtGui.QLabel('Weapon Class: ', self)
        label.setToolTip('Style or class of weapon (e.g. Sword).')
        box.addWidget(label)
        self.weaponclass = QtGui.QComboBox(self)
        self.weaponclass.addItem('Any')
        self.weaponclass.addItems(Weapon.stylelist)
        self.weaponclass.setEnabled(False)
        box.addWidget(self.weaponclass)
        label = QtGui.QLabel('Type: ', self)
        label.setToolTip('Exact weapon (e.g. Broadsword).')
        box.addWidget(label)
        self.weapontype = QtGui.QComboBox(self)
        self.weapontype.addItem('Any')
        self.weapontype.setEnabled(False)
        box.addWidget(self.weapontype)

        # Armor info
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        label = QtGui.QLabel('Armor Type: ', self)
        label.setToolTip('Specific weapon/armor type (e.g. Small Shield).')
        box.addWidget(label)
        self.armortype = QtGui.QComboBox(self)
        self.armortype.addItem('Any')
        self.armortype.addItems(Armor.armortypes)
        self.armortype.addItems(Armor.shieldtypes)
        self.armortype.setEnabled(False)
        box.addWidget(self.armortype)
        label = QtGui.QLabel('Wearer: ', self)
        label.setToolTip('Armor can be created for a character or for a mount.')
        box.addWidget(label)
        self.armorwearer = QtGui.QComboBox(self)
        self.armorwearer.addItems(('Any', 'Character', 'Mount'))
        self.armorwearer.setEnabled(False)
        box.addWidget(self.armorwearer)

        # Attributes
        self.all_attributes = ('ST', 'DX', 'IQ', 'MA', 'Hit', 'Dmg')
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        label = QtGui.QLabel('Attribute: ', self)
        label.setToolTip('Find an item with a bonus applied to the specified' +
                         ' attribute.')
        box.addWidget(label)
        self.attribute = QtGui.QComboBox(self)
        self.attribute.addItem('Any')
        self.attribute.addItems(self.all_attributes)
        box.addWidget(self.attribute)
        label = QtGui.QLabel('min', self)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        box.addWidget(label)
        self.minattr = QtGui.QSpinBox(self)
        self.minattr.setValue(1)
        self.minattr.setRange(1, 5)
        box.addWidget(self.minattr)
        label = QtGui.QLabel('max', self)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        box.addWidget(label)
        self.maxattr = QtGui.QSpinBox(self)
        self.maxattr.setValue(5)
        self.maxattr.setRange(1, 5)
        box.addWidget(self.maxattr)
        self.attrbutton = QtGui.QPushButton('...', self)
        self.connect(self.attrbutton, QtCore.SIGNAL('clicked()'), self.attribute_select)
        box.addWidget(self.attrbutton)

        # Ability
        self.all_abilities = [k for k in PhysicalAbility.abilities.keys()]
        a = MentalAbilityWithOpposites()
        self.all_abilities.extend([k for k in a.abilities.keys()])
        self.all_abilities.sort()
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        label = QtGui.QLabel('Ability: ', self)
        label.setToolTip('Find an item that allows the character to use the' +
                         ' specified ability.')
        box.addWidget(label)
        self.ability = QtGui.QComboBox(self)
        self.ability.addItem('Any')
        self.ability.addItems(self.all_abilities)
        box.addWidget(self.ability)
        label = QtGui.QLabel('min', self)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        box.addWidget(label)
        self.minIIQ = QtGui.QSpinBox(self)
        self.minIIQ.setValue(1)
        self.minIIQ.setRange(1, 5)
        box.addWidget(self.minIIQ)
        label = QtGui.QLabel('max', self)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        box.addWidget(label)
        self.maxIIQ = QtGui.QSpinBox(self)
        self.maxIIQ.setValue(5)
        self.maxIIQ.setRange(1, 5)
        box.addWidget(self.maxIIQ)
        self.abilitybutton = QtGui.QPushButton('...', self)
        self.connect(self.abilitybutton, QtCore.SIGNAL('clicked()'), self.ability_select)
        box.addWidget(self.abilitybutton)

        # Command buttons
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        text = 'Quick Search' if not simple else 'Add Criteria'
        self.OK = QtGui.QPushButton(text, self)
        box.addWidget(self.OK)
        if not simple:
            self.advanced = QtGui.QPushButton('Advanced', self)
            box.addWidget(self.advanced)
        self.cancel = QtGui.QPushButton('Cancel', self)
        box.addWidget(self.cancel)
        #self.location = None
        #if self.town is not None and not simple:
        #    label = QtGui.QLabel('Search: ')
        #    label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #    box.addWidget(label)
        #    self.location = QtGui.QComboBox(self)
        #    self.location.addItem('All Locations')
        #    #self.location.addItem(self.town.name)
        #    for store in self.town.stores:
        #        self.location.addItem(store.name)
        #    box.addWidget(self.location)

        # Connections
        self.connect(self.itemtype, 
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_itemtype)
        self.connect(self.markup,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_markup)
        self.connect(self.weaponclass,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_weaponclass)
        self.connect(self.OK, QtCore.SIGNAL('clicked()'), self.quicksearch)
        if not simple:
            self.connect(self.advanced, QtCore.SIGNAL('clicked()'), 
                         self.advancedsearch)

        self.show()
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'), self.window_.close)

    def attribute_select(self):
        aw = MultiAttributeWidget(self)
        self.connect(aw, QtCore.SIGNAL('attribute_selection_done'),
                     self.attribute_selection_done)

    def attribute_selection_done(self):
        if self.attrcrit is None:
            raise GUIError('No attributes selected!')
        i = self.attribute.findText('Custom')
        if i == -1:
            self.attribute.insertItem(1, 'Custom')
            self.attribute.setCurrentIndex(1)
        else:
            self.attribute.setCurrentIndex(i)
        self.minattr.setEnabled(False)
        self.maxattr.setEnabled(False)
        self.connect(self.attribute,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_attribute)

    def updated_attribute(self, text):
        self.minattr.setEnabled(text != 'Custom')
        self.maxattr.setEnabled(text != 'Custom')


    def ability_select(self):
        aw = MultiAbilityWidget(self)
        self.connect(aw, QtCore.SIGNAL('ability_selection_done'),
                     self.ability_selection_done)

    def ability_selection_done(self):
        if self.abilitycrit is None:
            raise GUIError('No abilities selected!')
        i = self.ability.findText('Custom')
        if i == -1:
            self.ability.insertItem(1, 'Custom')
            self.ability.setCurrentIndex(1)
        else:
            self.ability.setCurrentIndex(i)
        self.minIIQ.setEnabled(False)
        self.maxIIQ.setEnabled(False)
        self.connect(self.ability,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_ability)

    def updated_ability(self, text):
        self.minIIQ.setEnabled(text != 'Custom')
        self.maxIIQ.setEnabled(text != 'Custom')

    def _enable_attribute(self, bool, list=None):
        self.attribute.setEnabled(bool)
        self.minattr.setEnabled(bool)
        self.maxattr.setEnabled(bool)
        if list is None:
            list = self.all_attributes
        self.attribute.clear()
        if 'Any' not in list:
            self.attribute.addItem('Any')
        self.attribute.addItems(list)

    def _enable_ability(self, bool, list=None):
        self.ability.setEnabled(bool)
        self.minIIQ.setEnabled(bool)
        self.maxIIQ.setEnabled(bool)
        if list is None:
            list = self.all_abilities
        self.ability.clear()
        if 'Any' not in list:
            self.ability.addItem('Any')
        self.ability.addItems([a for a in list])  # allow .keys(), etc

    def updated_itemtype(self, text):

        # Update item-specific fields
        type = self.itemtype.currentText()
        self.weaponclass.setEnabled(False)
        self.weapontype.setEnabled(False)
        self.armortype.setEnabled(False)
        self.armorwearer.setEnabled(False)
        self.mincharges.setEnabled(False)
        self.maxcharges.setEnabled(False)
        if type == 'Weapon':
            self.weaponclass.setEnabled(True)
            if self.weaponclass.currentText() != 'Any':
                self.weapontype.setEnabled(True)
        elif type == 'Armor/Shield':
            self.armortype.setEnabled(True)
            self.armorwearer.setEnabled(True)
        elif type == 'Rod' or type == 'ST Battery':
            self.mincharges.setEnabled(True)
            self.maxcharges.setEnabled(True)
        self.language.setEnabled(type == 'Book' or type == 'Scroll')

        # Filter ability/attribute lists
        if type == 'Special Artifact':
            self._enable_attribute(False)
            self._enable_ability(True, MentalAbility.abilities.keys())
        elif type == 'ST Battery':
            self._enable_attribute(False)
            self._enable_ability(False)
        elif type == 'Rod':
            self._enable_attribute(False)
            self._enable_ability(True, MentalAbility.EtherealBow)
        elif type == 'Gem' or type == 'Ring' or type == 'Scroll':
            self._enable_attribute(False)
            self._enable_ability(True, MentalAbility.abilities.keys())
        elif type == 'Potion' or type == 'Weapon' or type == 'Armor/Shield':
            self._enable_attribute(True)
            self._enable_ability(True, MentalAbility.abilities.keys())
        elif type == 'Amulet':
            self._enable_attribute(True)
            #self.maxattr.setValue(1)
            #self.minattr.setValue(1)
            self.minattr.setEnabled(False)
            self.maxattr.setEnabled(False)
            self._enable_ability(False)
        elif type == 'Book':
            self._enable_attribute(False)
            self._enable_ability(True)
        else:
            self._enable_attribute(True)
            self._enable_ability(True)

    def updated_markup(self, text):
        if text == 'Any':
            self.minmarkup.setEnabled(False)
            self.maxmarkup.setEnabled(False)
        elif text == 'Sale Items':
            self.minmarkup.setValue(0)
            self.minmarkup.setEnabled(False)
            self.maxmarkup.setValue(99)
            self.maxmarkup.setEnabled(False)
        elif text == 'Custom':
            self.minmarkup.setEnabled(True)
            self.maxmarkup.setEnabled(True)

    def _updatetypes(self, cls):
        self.weapontype.addItems([i[0] for i in Weapon.weaponlist
                                       if i[1] == cls])

    def updated_weaponclass(self, text):
        cls = self.weaponclass.currentText()
        self.weapontype.clear()
        self.weapontype.addItem('Any')
        self._updatetypes(cls)
        if cls == 'Missile Weapon':
            self._updatetypes('Drawn Bow')
            self._updatetypes('Cross Bow')
        elif cls == 'Thrown Weapon':
            self.weapontype.addItems([i[0] for i in Weapon.weaponlist
                                           if i[3] == True])
        self.weapontype.setEnabled(cls != 'Any')

    def _lookupitemtype(self):
        type = self.itemtype.currentText()
        if type == 'Special Artifact':
            return SpecialArtifact
        elif type == 'ST Battery':
            return STBattery
        elif type == 'Weapon':
            return Weapon
        elif type == 'Armor/Shield':
            return Armor
        elif type == 'Amulet':
            return Amulet
        elif type == 'Ring':
            return Ring
        elif type == 'Rod':
            return Rod
        elif type == 'Book':
            return Book
        elif type == 'Scroll':
            return Scroll
        elif type == 'Gem':
            return Gem
        elif type == 'Potion':
            return Potion
        else:
            raise 'Unknown item type: %s' % type

    def _buildcriteria(self):
        self.maincriteria = ANDCriteriaSet([])

        # Text Search
        if self.textsearch.text() != '':
            crit = TextCriterion(self.textsearch.text())
            self.maincriteria.addcriterion(crit)

        # Item Type
        if self.itemtype.currentText() != 'Any':
            crit = TypeCriterion(self._lookupitemtype())
            self.maincriteria.addcriterion(crit)

        # Price
        if self.minprice.text() != '' or self.maxprice.text() != '':
            min = max = None
            if self.minprice.text() != '':
                try:
                    min = int(self.minprice.text())
                except ValueError as e:
                    raise GUIError('Invalid minimum price!')
            if self.maxprice.text() != '':
                try:
                    max = int(self.maxprice.text())
                except ValueError as e:
                    raise GUIError('Invalid maximum price!')
            crit = PriceCriterion(min, max)
            self.maincriteria.addcriterion(crit)

        # Markup
        if self.markup.currentText() != 'Any':
            crit = MarkupCriterion(self.minmarkup.value(), self.maxmarkup.value())
            self.maincriteria.addcriterion(crit)

        # Weapon Details
        if self.itemtype.currentText() == 'Weapon':
            if self.weapontype.currentText() != 'Any':
                crit = WeaponTypeCriterion(self.weapontype.currentText())
                self.maincriteria.addcriterion(crit)
            elif self.weaponclass.currentText() != 'Any':
                crit = WeaponClassCriterion(self.weaponclass.currentText())
                self.maincriteria.addcriterion(crit)

        # Armor Details
        if self.itemtype.currentText() == 'Armor/Shield':
            if self.armortype.currentText() != 'Any':
                crit = ArmorTypeCriterion(self.armortype.currentText())
                self.maincriteria.addcriterion(crit)
            if self.armorwearer.currentText() != 'Any':
                crit = ArmorWearerCriterion(self.armorwearer.currentText())
                self.maincriteria.addcriterion(crit)

        # Number of charges
        if self.mincharges.isEnabled():
            if self.mincharges.value() != 1 or self.maxcharges.value() != 25:
                crit = ChargesCriterion(self.mincharges.value(),
                                           self.maxcharges.value())
                self.maincriteria.addcriterion(crit)

        # Attribute
        if self.attribute.isEnabled():
            crit = None
            if self.attribute.currentText() == 'Custom':
                crit = self.attrcrit
            elif self.attribute.currentText() != 'Any':
                crit = AttributeCriterion(self.attribute.currentText(),
                                             self.minattr.value(),
                                             self.maxattr.value())
            elif self.minattr.value() != 1 or self.maxattr.value() != 5:
                crit = AttributeCriterion(None,
                                             self.minattr.value(),
                                             self.maxattr.value())
            if crit is not None:
                self.maincriteria.addcriterion(crit)

        # Ability
        if self.ability.isEnabled():
            crit = None
            if self.ability.currentText() == 'Custom':
                crit = self.abilitycrit
            elif self.ability.currentText() != 'Any':
                crit = CharacterAbilityCriterion(self.ability.currentText(),
                                                    self.minIIQ.value(),
                                                    self.maxIIQ.value())
            elif self.minIIQ.value() != 1 or self.maxIIQ.value() != 5:
                crit = CharacterAbilityCriterion(None,
                                                    self.minIIQ.value(),
                                                    self.maxIIQ.value())
            if crit is not None:
                self.maincriteria.addcriterion(crit)

    def quicksearch(self):
        try:
            self._buildcriteria()
        except GUIError as e:
            return
        self.parent.searchcriteria = self.maincriteria
        self.emit(QtCore.SIGNAL('QuickSearch()'))
        self.window_.close()

    def advancedsearch(self):
        try:
            self._buildcriteria()
        except GUIError as e:
            return
        aw = AdvancedSearchWidget(self, self.maincriteria)
        self.connect(aw, QtCore.SIGNAL('AdvancedSearch()'), self.advanced_done)
        self.window_.hide()

    def advanced_done(self):
        self.parent.searchcriteria = self.maincriteria
        self.emit(QtCore.SIGNAL('QuickSearch()'))
        self.window_.close()
        
    def keyPressEvent(self, event):
        # Enter -> QuickSearch
        if event.key() == QtCore.Qt.Key_Return or \
           event.key() == QtCore.Qt.Key_Enter:
            self.quicksearch()
        # Escape -> Cancel
        elif event.key() == QtCore.Qt.Key_Escape:
            self.cancel()
        # Pass unrecognized
        else:
            QtGui.QWidget.keyPressEvent(self, event)


class ResultsWindow(QtGui.QMainWindow):

    def __init__(self, parent, results):
        QtGui.QMainWindow.__init__(self, parent)
        self.setGeometry(200, 100, 850, 800)
        self.setWindowTitle('Search Results')
        display = QtGui.QTreeWidget(self)
        self.setCentralWidget(display)

        display.setColumnCount(6)
        display.setSortingEnabled(True)
        for item in results:
            ItemTree(display, item, showloc=True)
        self.center()
        self.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        width = min(size.width(), int(screen.width() * .9))
        height = min(size.height(), int(screen.height() * .9))
        if width != size.width() or height != size.height():
            self.resize(width, height)
            size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class AdvancedSearchWidget(QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setGeometry(200, 200, 400, 300)
        self.window_.setWindowTitle('Advanced Search')
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

    def __init__(self, parent, maincrit):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.topcriteria = maincrit
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)

        # Header / Save / Load
        hbox = QtGui.QHBoxLayout()
        mbox.addLayout(hbox)
        hbox.addWidget(QtGui.QLabel('Search Criteria:', self))
        self.load = QtGui.QPushButton('Load Search', self)
        self.connect(self.load, QtCore.SIGNAL('clicked()'), self.load_search)
        hbox.addWidget(self.load)
        self.save = QtGui.QPushButton('Save Search', self)
        self.connect(self.save, QtCore.SIGNAL('clicked()'), self.save_search)
        hbox.addWidget(self.save)

        # Criteria Box
        self.criteriabox = QtGui.QTreeWidget(self)
        self._buildtree()
        mbox.addWidget(self.criteriabox)

        # Buttons
        bbox = QtGui.QHBoxLayout()
        mbox.addLayout(bbox)
        and_btn = QtGui.QPushButton('x AND new criteria', self)
        bbox.addWidget(and_btn)
        self.connect(and_btn, QtCore.SIGNAL('clicked()'), self.and_criteria)
        or_btn = QtGui.QPushButton('x OR new criteria', self)
        bbox.addWidget(or_btn)
        self.connect(or_btn, QtCore.SIGNAL('clicked()'), self.or_criteria)
        not_btn = QtGui.QPushButton('NOT x', self)
        bbox.addWidget(not_btn)
        self.connect(not_btn, QtCore.SIGNAL('clicked()'), self.not_criteria)
        search = QtGui.QPushButton('Search', self)
        mbox.addWidget(search)
        self.connect(search, QtCore.SIGNAL('clicked()'), self.search)

        self.show()

    def _buildtree(self):
        self.criteriabox.clear()
        self.criteriabox.setColumnCount(2)
        self.criteriabox.setHeaderLabels(('', 'Criterion'))
        if isinstance(self.topcriteria, ANDCriteriaSet):
            for crit in self.topcriteria.criteria:
                CriteriaTree(self.criteriabox, crit)
        else:
            CriteriaTree(self.criteriabox, self.topcriteria)

    def and_criteria(self):
        self.searchcriteria = None
        sw = SearchWidget(self, None, simple=True)
        self.connect(sw, QtCore.SIGNAL('QuickSearch()'), self.and_done)

    def and_done(self):
        if self.searchcriteria is not None:
            if len(self.searchcriteria.criteria) == 1:
                self.searchcriteria = self.searchcriteria.criteria[0]
            item = self.criteriabox.currentItem()
            if item is None:
                self.topcriteria.addcriterion(self.searchcriteria)
            elif isinstance(item.criterion, ANDCriteriaSet):
                item.criterion.addcriterion(self.searchcriteria)
            else:
                parent = item.parent()
                if parent is None:
                    self.topcriteria.addcriterion(self.searchcriteria)
                elif isinstance(parent.criterion, ANDCriteriaSet):
                    parent.criterion.addcriterion(self.searchcriteria)
                else:
                    parent.criterion.criteria.remove(item.criterion)
                    newand = ANDCriteriaSet([self.searchcriteria, 
                                                item.criterion])
                    parent.criterion.addcriterion(newand)
            self._buildtree()
                
        
    def or_criteria(self):
        self.searchcriteria = None
        sw = SearchWidget(self, None, simple=True)
        self.connect(sw, QtCore.SIGNAL('QuickSearch()'), self.or_done)

    def or_done(self):
        if self.searchcriteria is not None:
            if len(self.searchcriteria.criteria) == 1:
                self.searchcriteria = self.searchcriteria.criteria[0]
            item = self.criteriabox.currentItem()
            if item is None:
                self.topcriteria.addcriterion(self.searchcriteria)
            elif isinstance(item.criterion, ORCriteriaSet):
                    item.criterion.addcriterion(self.searchcriteria)
            else:
                parent = item.parent()
                if parent is None:
                    self.topcriteria.criteria.remove(item.criterion)
                    newor = ORCriteriaSet([self.searchcriteria,
                                              item.criterion])
                    self.topcriteria.addcriterion(newor)
                elif isinstance(parent.criterion, ORCriteriaSet):
                    parent.criterion.addcriterion(self.searchcriteria)
                else:
                    parent.criterion.criteria.remove(item.criterion)
                    newor = ORCriteriaSet([self.searchcriteria,
                                              item.criterion])
                    parent.criterion.addcriterion(newor)
            self._buildtree()


    def not_criteria(self):
        item = self.criteriabox.currentItem()
        if item is None: return
        parent = item.parent()
        if parent is None:
            self.topcriteria.criteria.remove(item.criterion)
            self.topcriteria.addcriterion(NOTCriteriaSet(item.criterion))
        elif isinstance(parent.criterion, NOTCriteriaSet):
            grand = parent.parent()
            grand.criterion.criteria.remove(parent.criterion)
            grand.criterion.addcriterion(parent.criterion.criteria[0])
        elif isinstance(parent.criterion, NOTCriteriaSet):
            parent.criterion.criteria.remove(item.criterion)
            parent.criterion.addcriterion(item.criterion.criteria[0])
        else:
            parent.criterion.criteria.remove(item.criterion)
            newnot = NOTCriteriaSet([item.criterion,])
            parent.criterion.addcriterion(newnot)
        self._buildtree()

    def search(self):
        self.parent.maincriteria = self.topcriteria
        self.emit(QtCore.SIGNAL('AdvancedSearch()'))
        self.window_.close()

    def save_search(self):
        searchdir = 'searches'
        if not os.path.isdir(searchdir): os.mkdir(searchdir)
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Select Search File',
                                os.path.join(searchdir, 'untitled.search'), 
                                'Saved Searches (*.search)')
        if filename != '':
            file = open(filename, 'wb')
            pickle.dump(self.topcriteria, file)
            file.close()

    def load_search(self):
        searchdir = 'searches'
        if not os.path.isdir(searchdir): os.mkdir(searchdir)
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Select Search File',
                                searchdir, 'Saved Searches (*.search)')
        if filename != '':
            file = open(filename, 'rb')
            self.topcriteria = pickle.load(file)
            file.close()
            self._buildlist()

