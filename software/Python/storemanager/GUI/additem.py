
from PyQt4 import QtGui, QtCore

from elvenfire.artifacts import written
from elvenfire.artifacts.lesser import Amulet
from elvenfire.artifacts.combat import *
from elvenfire.abilities.charabilities import *
from elvenfire.abilities.itemabilities import *
from storemanager.stockitems.special import *
from storemanager.stockitems.combat import *
from storemanager.stockitems.greater import *
from storemanager.stockitems.lesser import *
from storemanager.stockitems.written import *


class AddItemWidget (QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        #self.window_.setGeometry(300, 200, 500, 150)
        self.window_.setWindowTitle('Add Item to Store...')
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

    def __init__(self, parent, store):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.store = store
        self.abilities = []
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)
        mbox.addWidget(QtGui.QLabel('Add new item to %s' % self.store.name))

        # Item Type
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        box.addWidget(QtGui.QLabel('Item Type: ', self))
        self.itemtype = QtGui.QComboBox(self)
        self.itemtype.addItems(('Choose One', 'Special Artifact', 'ST Battery',
                                'Weapon', 'Armor', 'Shield', 'Amulet', 'Ring',
                                'Rod', 'Book', 'Scroll', 'Gem', 'Potion'))
        self.connect(self.itemtype, 
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_itemtype)
        box.addWidget(self.itemtype)

        # Subtype (weapon class / specific artifact / Potion type)
        self.subtype_label = QtGui.QLabel('Subtype: ', self)
        box.addWidget(self.subtype_label)
        self.subtype = QtGui.QComboBox(self)
        self.subtype.addItem('Choose Item Type')
        self.connect(self.subtype, 
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_subtype)
        self.subtype.setEnabled(False)
        box.addWidget(self.subtype)

        # Specific type (weapon type, armor type, specific potion)
        self.spectype_label = QtGui.QLabel('Specific: ', self)
        box.addWidget(self.spectype_label)
        self.spectype = QtGui.QComboBox(self)
        self.spectype.addItem('Choose Item Type')
        self.spectype.setEnabled(False)
        box.addWidget(self.spectype)

        # Language
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        self.language_label = QtGui.QLabel('Language: ', self)
        box.addWidget(self.language_label)
        self.language = QtGui.QComboBox(self)
        self.language.addItems(written.languages)
        self.language.setEnabled(False)
        box.addWidget(self.language)

        # Number of charges
        self.charges_label = QtGui.QLabel('# of charges: ', self)
        box.addWidget(self.charges_label)
        self.charges = QtGui.QSpinBox(self)
        self.charges.setRange(1, 25)
        self.charges.setEnabled(False)
        box.addWidget(self.charges)

        # Ability Storage/Display
        self.abilities = []
        self.abilitiesbox = QtGui.QLabel('Current Abilities:\n', self)
        mbox.addWidget(self.abilitiesbox)

        # Abilities: Type
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        box.addWidget(QtGui.QLabel('New Ability: ', self))
        self.abilitytype = QtGui.QComboBox(self)
        self.abilitytype.addItem('Choose Item Type')
        self.connect(self.abilitytype,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_abilitytype)
        self.abilitytype.setEnabled(False)
        box.addWidget(self.abilitytype)

        # Abilities: Ability
        self.ability_label = QtGui.QLabel('Subtype: ', self)
        box.addWidget(self.ability_label)
        self.ability = QtGui.QComboBox(self)
        self.ability.addItem('Choose Item Type')
        self.connect(self.ability,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_ability)
        self.ability.setEnabled(False)
        box.addWidget(self.ability)

        # Abilities: IIQ/Bonus
        self.abilitysize_label = QtGui.QLabel('IIQ: ', self)
        box.addWidget(self.abilitysize_label)
        self.abilitysize = QtGui.QSpinBox(self)
        self.abilitysize.setRange(1, 5)
        self.abilitysize.setEnabled(False)
        box.addWidget(self.abilitysize)

        # Abilities: Add
        self.ability_btn = QtGui.QPushButton('Add', self)
        self.connect(self.ability_btn, QtCore.SIGNAL('clicked()'), 
                     self.add_ability)
        self.ability_btn.setEnabled(False)
        box.addWidget(self.ability_btn)

        # Gather list of abilities (and sort) for later use
        list = MentalAbilityWithOpposites.getabilities()
        self.all_mental_abilities = [i for i in list.keys()]
        self.all_mental_abilities.sort()
        list = PhysicalAbility.abilities
        self.physical_abilities = [i for i in list.keys()]
        self.physical_abilities.sort()
        list = MentalAbility.abilities
        self.mental_abilities = [i for i in list.keys()]
        self.mental_abilities.sort()

        # Commission: Player, Character
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        box.addWidget(QtGui.QLabel('Commission: Player: ', self))
        self.player = QtGui.QLineEdit(self)
        box.addWidget(self.player)
        box.addWidget(QtGui.QLabel('Character: ', self))
        self.character = QtGui.QLineEdit(self)
        box.addWidget(self.character)

        # Buttons
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        self.OK = QtGui.QPushButton('Add Item', self)
        self.connect(self.OK, QtCore.SIGNAL('clicked()'), self.create)
        box.addWidget(self.OK)
        self.cancel = QtGui.QPushButton('Cancel', self)
        box.addWidget(self.cancel)

        self.show()
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'), 
                     self.window_.close)


    def updated_itemtype(self, type):

        # Disable everything below this branch
        self.subtype.setEnabled(False)
        self.spectype.setEnabled(False)
        self.language.setEnabled(False)
        self.charges.setEnabled(False)
        self.abilitytype.setEnabled(False)
        self.ability.setEnabled(False)
        self.abilitysize.setEnabled(False)
        self.ability_btn.setEnabled(False)

        self.abilities = []
        self._update_abilitiesbox()

        if type == 'Special Artifact':
            self.cls = SpecialArtifactStockItem
            self.subtype_label.setText('Artifact Type: ')
            self.subtype.clear()
            self.subtype.addItem('Choose artifact type')
            self.subtype.addItems(('Wish Ring', 'Self-Powered Ring',
                                   'Gem of Summoning', 'Belt of Fetching',
                                   'Gem of Maintain Illusion', 'Flying Carpet',
                                   'Shapeshifter', 'Cloak of Vision',
                                   'Gem of True Seeing', 'Lens of Translation',
                                   'Charm', 'Unicorn Horn'))
            self.subtype.setEnabled(True)

        elif type == 'ST Battery':
            self.cls = STBatteryStockItem
            self.charges_label.setText('# of Charges: ')
            self.charges.setRange(1, 25)
            self.charges.setEnabled(True)

        elif type == 'Weapon':
            self.cls = WeaponStockItem
            self.subtype_label.setText('Weapon Class: ')
            self.subtype.clear()
            self.subtype.addItem('Choose weapon class')
            self.subtype.addItems(Weapon.stylelist)
            self.subtype.setEnabled(True)

            self.abilitytype.clear()
            self.abilitytype.addItem('Choose ability type')
            self.abilitytype.addItems(('Special', 'Enhanced', 'Attribute'))
            self.abilitytype.setEnabled(True)

        elif type == 'Armor':
            self.cls = ArmorStockItem
            self.subtype_label.setText('Armor Wearer: ')
            self.subtype.clear()
            self.subtype.addItems(('Character', 'Mount'))
            self.subtype.setEnabled(True)

            self.spectype_label.setText('Armor Type: ')
            self.spectype.clear()
            self.spectype.addItem('Choose armor type')
            self.spectype.addItems(Armor.armortypes)
            self.spectype.setEnabled(True)

            self.abilitytype.clear()
            self.abilitytype.addItem('Attribute')

            self.ability.clear()
            self.ability.addItem('Choose an attribute')
            self.ability.addItems(('DX', 'Hit', 'MA'))
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('Bonus: +')
            self.abilitysize.setRange(1, 10)
            self.abilitysize.setEnabled(True)

            self.ability_btn.setEnabled(True)

        elif type == 'Shield':
            self.cls = ArmorStockItem
            self.spectype_label.setText('Shield Type: ')
            self.spectype.clear()
            self.spectype.addItem('Choose shield type')
            self.spectype.addItems(Armor.shieldtypes)
            self.spectype.setEnabled(True)

            self.abilitytype.clear()
            self.abilitytype.addItem('Attribute')

            self.ability.clear()
            self.ability.addItem('Choose an attribute')
            self.ability.addItems(('DX', 'Hit', 'MA'))
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('Bonus: +')
            self.abilitysize.setRange(1, 10)
            self.abilitysize.setEnabled(True)

            self.ability_btn.setEnabled(True)

        elif type == 'Amulet':
            self.cls = AmuletStockItem
            self.subtype_label.setText('Amulet Type: ')
            self.subtype.clear()
            self.subtype.addItem('Choose amulet type')
            self.subtype.addItems(('Control', 'Proof', 'Attribute', 
                                   'Skepticism'))
            self.subtype.setEnabled(True)

        elif type == 'Rod':
            self.cls = RodStockItem
            self.charges_label.setText('# of Charges: ')
            self.charges.setRange(1, 25)
            self.charges.setEnabled(True)

            self.abilitytype.clear()
            self.abilitytype.addItem('Ethereal Bow')

            self.ability.clear()
            self.ability.addItem('Choose an element')
            self.ability.addItems(MentalAbility.EtherealBow)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Ring' or type == 'Gem':
            if type == 'Ring':
                self.cls = RingStockItem
            else:
                self.cls = GemStockItem
            self.abilitytype.clear()
            self.abilitytype.addItem('Mental Ability')

            self.ability.clear()
            self.ability.addItem('Choose an ability')
            self.ability.addItems(self.all_mental_abilities)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Book':
            self.cls = BookStockItem
            self.language_label.setText('Language: ')
            self.language.setEnabled(True)
            self.abilitytype.clear()
            self.abilitytype.addItem('Character Ability')

            self.ability.clear()
            self.ability.addItem('Choose an ability')
            self.ability.addItems(self.physical_abilities)
            self.ability.addItems(self.all_mental_abilities)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Scroll':
            self.cls = ScrollStockItem
            self.language_label.setText('Language: ')
            self.language.setEnabled(True)
            self.abilitytype.clear()
            self.abilitytype.addItem('Mental Ability')

            self.ability.clear()
            self.ability.addItem('Choose an ability')
            self.ability.addItems(self.all_mental_abilities)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Potion':
            self.cls = PotionStockItem
            self.subtype_label.setText('Potion Class: ')
            self.subtype.clear()
            self.subtype.addItem('Choose potion class')
            self.subtype.addItems(('Healing', 'Weapon Poison', 'Grenade',
                                   'Attribute', 'Ability', 'Other'))
            self.subtype.setEnabled(True)

        else:
            raise GUIError("Oops! I don't recognize that item type!")
        
    def updated_subtype(self, type):

        # Disable everything below this branch
        self.spectype.setEnabled(False)
        self.language.setEnabled(False)
        self.charges.setEnabled(False)
        self.abilitytype.setEnabled(False)
        self.ability.setEnabled(False)
        self.abilitysize.setEnabled(False)
        self.ability_btn.setEnabled(False)

        if type == 'Self-Powered Ring':
            self.abilitytype.clear()
            self.abilitytype.addItem('Mental Ability')

            self.ability.clear()
            self.ability.addItem('Choose an ability')
            self.ability.addItems(self.all_mental_abilities)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Gem of Summoning':
            self.charges_label.setText('IQ: ')
            self.charges.setRange(9, 25)
            self.charges.setEnabled(True)

        elif type == 'Flying Carpet':
            self.charges_label.setText('Hexes: ')
            self.charges.setRange(1, 25)
            self.charges.setEnabled(True)

        elif type == 'Cloak of Vision':
            self.abilitytype.clear()
            self.abilitytype.addItem('Cloak of Vision')
            self.ability.clear()
            self.ability.addItem('Vision')
            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Charm':
            self.charges_label.setText('Charm Size: ')
            self.charges.setRange(1, 2)
            self.charges.setEnabled(True)

        elif type in Weapon.stylelist:
            self.spectype_label.setText('Weapon type: ')
            self.spectype.clear()
            self.spectype.addItem('Choose a weapon')
            self.spectype.addItems(Weapon.weaponlist(type))
            self.spectype.setEnabled(True)
            self.abilitytype.setEnabled(True)
            if not self.abilitytype.currentText().startswith('Choose'):
                self.ability.setEnabled(True)
                if not self.ability.currentText().startswith('Choose'):
                    i = self.ability.currentIndex()
                    self.ability.setCurrentIndex(0)
                    self.ability.setCurrentIndex(i)  # reset abilitysize

        elif type in Armor.wearers:
            self.ability.setEnabled(True)
            self.abilitysize.setEnabled(True)
            self.ability_btn.setEnabled(True)


        elif type == 'Control':
            self.spectype_label.setText('Controlled type: ')
            self.spectype.clear()
            self.spectype.addItem('Choose what to control')
            self.spectype.addItems(AmuletAbility.controls)
            self.spectype.setEnabled(True)

        elif type == 'Proof':
            self.spectype_label.setText('Element: ')
            self.spectype.clear()
            self.spectype.addItem('Choose element')
            self.spectype.addItems(AmuletAbility.elements)
            self.spectype.setEnabled(True)

        elif self.itemtype.currentText() == 'Amulet' and type == 'Attribute':
            self.spectype_label.setText('Attribute: ')
            self.spectype.clear()
            self.spectype.addItem('Choose attribute')
            self.spectype.addItems(['%s+1' % a for a 
                                    in AmuletAbility.attributes])
            self.spectype.setEnabled(True)

        elif type == 'Skepticism':
            self.charges_label.setText('Skepticism Bonus: ')
            self.charges.setRange(1, 5)
            self.charges.setEnabled(True)

        elif type == 'Healing':
            self.spectype_label.setText('Subtype: ')
            self.spectype.clear()
            self.spectype.addItem('Healing Potion')

            self.charges_label.setText('Doses: ')
            self.charges.setRange(1, 25)
            self.charges.setEnabled(True)

        elif type == 'Other':
            self.spectype_label.setText('Subtype: ')
            self.spectype.clear()
            self.spectype.addItems(('Universal Antidote', 'Universal Solvent',
                                    'Revival'))
            self.spectype.setEnabled(True)

        elif type == 'Weapon Poison':
            self.spectype_label.setText('Damage: ')
            self.spectype.clear()
            self.spectype.addItem('Select damage')
            self.spectype.addItems(('d100', 'd12', 'd10', '2d20', 'd20',
                                    'drain 3/r for 6 rounds', 'd6 + sleep',
                                    'd6 + freeze', 'd6 + slow', 'd6',
                                    'd20 dragons', 'd20 hydras', 'd20 reptiles',
                                    'd20 mammals', 'd20 insects', 'd20 plants'))
            self.spectype.setEnabled(True)

        elif type == 'Grenade':
            self.spectype_label.setText('Damage: ')
            self.spectype.clear()
            self.spectype.addItem('Select damage')
            self.spectype.addItems(('d20 & d12 & d6', 'd12 & d8', 'd10 & d6',
                                    'd8 & d4'))
            self.spectype.setEnabled(True)

            self.language_label.setText('Type: ')
            self.language.clear()
            self.language.addItem('Select type')
            self.language.addItems(('Gas', 'Contact', 'Water'))
            self.language.setEnabled(True)

        elif self.itemtype.currentText() == 'Potion' and type == 'Attribute':
            self.abilitytype.clear()
            self.abilitytype.addItem('Attribute')

            self.ability.clear()
            self.ability.addItem('Choose attribute')
            self.ability.addItems(('ST', 'DX', 'IQ', 'MA'))
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('Bonus: +')
            self.abilitysize.setRange(1, 10)
            self.abilitysize.setEnabled(True)

        elif type == 'Ability':
            self.abilitytype.clear()
            self.abilitytype.addItem('Ability')

            self.ability.clear()
            self.ability.addItem('Choose ability')
            self.ability.addItems(self.all_mental_abilities)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        #else: do nothing

    def updated_abilitytype(self, type):

        if type == 'Special':
            self.ability.clear()
            self.ability.addItem('Choose special ability')
            self.ability.addItems(WeaponAbility.typelist)
            self.ability.setEnabled(True)
            self.abilitysize.setEnabled(False)

        elif type == 'Enhanced':
            self.ability.clear()
            self.ability.addItem('Choose mental ability')
            self.ability.addItems(self.all_mental_abilities)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Attribute':  # always Weapon
            self.ability.clear()
            self.ability.addItem('Choose an attribute')
            self.ability.addItems(('ST', 'DX', 'Dam'))
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('Bonus: +')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        #else: do nothing

    def updated_ability(self, type):
         if self.itemtype.currentText() in ('Weapon', 'Armor', 'Shield',
                                            'Amulet', 'Ring', 'Book', 'Scroll'):
             if not self.ability.currentText().startswith('Choose'):
                 self.ability_btn.setEnabled(True)

         if type in WeaponAbility.typelist:
             self.abilitysize.setEnabled(False)

         if type == 'Animated':
             self.abilitysize_label.setText('Range (MH): ')
             self.abilitysize.setRange(1, 5)
             self.abilitysize.setEnabled(True)

         elif type == 'Defender':
             self.abilitysize_label.setText('Dx Penalty: ')
             self.abilitysize.setRange(1, 5)
             self.abilitysize.setEnabled(True)

         elif type == 'Changling':
             self.OK.setText('Next Weapon')
             self.add_ability()

         elif type == 'MA':
             self.abilitysize.setRange(1, 10)

         else:  # either attribute (size already enabled) or weapon (disabled)
             self.abilitysize.setRange(1, 5)

         if (type != 'Changling' and 
             WeaponAbility('Changling') not in self.abilities):
             self.OK.setText('Add Item')

    def _notset(self, field):
        if '__iter__' in dir(field):
            for f in field:
                if self._notset(f): return True
            return False
        if field.currentText().startswith('Choose'): return True
        if field.currentText().startswith('Select'): return True
        return False

    def _update_abilitiesbox(self):
        text = 'Current Abilities:\n'
        for ability in self.abilities:
            text += '  ' + str(ability) + '\n'
        self.abilitiesbox.setText(text)

    def add_enhanced(self, enhanced):
        ability = MentalAbilityWithOpposites(self.ability.currentText(),
                                             self.abilitysize.value())
        if ability in enhanced.abilities:
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                     'Duplicate Mental Ability',
                                     '%s is already on this item!' % ability,
                                     QtGui.QMessageBox.Ok).exec_()
        abilities = enhanced.abilities + [ability]
        i = self.abilities.index(enhanced)
        self.abilities[i] = WeaponAbility('Enhanced', 
                                          abilities = enhanced.abilities)
        self.ability.setCurrentIndex(0)
        self._update_abilitiesbox()
        

    def add_ability(self):

        """Add specified ability to abilities list."""

        # Verify ability is fully specified
        if self._notset((self.abilitytype, self.ability)):
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                     'Ability Not Selected',
                                     'Please specify an ability first!',
                                     QtGui.QMessageBox.Ok).exec_()


        # Handle Enhanced 'next'
        if self.abilitytype.currentText() == 'Enhanced':
            for abil in self.abilities:
                if isinstance(abil, WeaponAbility) and abil.type == 'Enhanced':
                    return self.add_enhanced(abil)
            else:
                ma = MentalAbilityWithOpposites(self.ability.currentText(),
                                                self.abilitysize.value())
                ability = WeaponAbility('Enhanced', abilities=[ma])

        # Character ability?
        elif 'Ability' in self.abilitytype.currentText():
            ability = PhysicalOrMentalAbility(self.ability.currentText(),
                                              self.abilitysize.value())

        # Attribute ability?
        elif 'Attribute' in self.abilitytype.currentText():
            ability = AttributeAbility(self.ability.currentText(),
                                       self.abilitysize.value())

        # Weapon ability? (other than Enhanced)
        elif self.abilitytype.currentText() == 'Special':
            if self.ability.currentText() == 'Animated':
                ability = WeaponAbility('Animated', 
                                        range=self.abilitysize.value())
            elif self.ability.currentText() == 'Defender':
                ability = WeaponAbility('Defender',
                                        size=self.abilitysize.value())
            else:
                ability = WeaponAbility(self.ability.currentText())



        # Prevent duplicates
        if ability in self.abilities:
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                     'Duplicate Ability',
                                     '%s is already on this item!' % ability,
                                     QtGui.QMessageBox.Ok).exec_()

        # Save ability
        self.abilities.append(ability)

        # Is the item 'full'?
        num = len(self.abilities)
        if num >= self.cls.maxabilities:
            self.ability_btn.setEnabled(False)

        # Reset
        self.abilitytype.setCurrentIndex(0)
        self.ability.setCurrentIndex(0)

        # Update static field
        self._update_abilitiesbox()

    def error(self, msg):
        QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Cannot create item',
                          msg, QtGui.QMessageBox.Ok).exec_()

    def handle_changling(self):

        """Prompt for second weapon before creating."""

        if self._notset(self.spectype):
            return self.error('You must specify the weapon type!')

        # Confirm
        msg = ("Defining a Changling requires two weapon definitions." +
               " If you continue, the primary weapon will be:\n\n" +
               "Type: %s" % self.spectype.currentText() + '\n' +
               "Abilities:\n")
        for a in self.abilities:
            msg += '  %s\n' % a
        msg += ("\nAre you ready to continue, and specify the secondary" +
                " weapon?")
        res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'Confirm first weapon', msg,
                                QtGui.QMessageBox.Yes |
                                QtGui.QMessageBox.No).exec_()
        if res != QtGui.QMessageBox.Yes:
            return

        # Prompt for second weapon
        sw = SecondaryWeaponWidget(self)
        self.connect(sw, QtCore.SIGNAL('secondary_done'), self.changling_done)
        # (will set self.secondaryweapon)

    def changling_done(self):
        """Finish weapon specification."""
        item = WeaponStockItem(type=self.spectype.currentText(),
                               abilities=self.abilities,
                               secondaryweapon=self.secondaryweapon)
        self.store.additem(item)
        self.parent.town.save()
        self.parent._buildtree(expand=self.store)
        self.window_.close()

    def create(self):

        """Verify and create item."""

        # Deal with Changling 'Next Weapon'
        if WeaponAbility('Changling') in self.abilities:
            return self.handle_changling()

        if self._notset(self.itemtype):
            return self.error('You must specify an item type!')

        # Special Artifacts
        if self.cls == SpecialArtifactStockItem:

            if self._notset([self.subtype]):
                return self.error('Please specify the artifact type!')

            type = self.subtype.currentText()
            if type == 'Self-Powered Ring':
                if self._notset([self.ability]):
                    return self.error('You must select an ability!')
                ability = MentalAbilityWithOpposites(self.ability.currentText(),
                                                     self.abilitysize.value())
                item = self.cls(type, ability=ability)

            elif type == 'Gem of Summoning':
                item = self.cls(type, IQ=self.charges.value())
            elif type == 'Flying Carpet':
                item = self.cls(type, size=self.charges.value())
            elif type == 'Cloak of Vision':
                item = self.cls(type, IIQ=self.abilitysize.value())
            else:
                item = self.cls(type)

        # ST Batteries
        elif self.cls == STBatteryStockItem:
            item = self.cls(self.charges.value())

        # Weapons
        elif self.cls == WeaponStockItem:
            if not self.abilities:
                return self.error('You must specify at least one ability!')
            elif self._notset(self.subtype):
                return self.error('Please choose a weapon class!')
            elif self._notset(self.spectype):
                return self.error('Please choose a weapon type!')

            item = self.cls(type=self.spectype.currentText(),
                            abilities=self.abilities)

        # Armor / Shield
        elif self.cls == ArmorStockItem:
            if not self.abilities:
                return self.error('You must specify at least one ability!')
            elif self._notset(self.spectype):
                return self.error('Please choose a specific type!')

            if self.subtype.isEnabled():
                item = self.cls(type=self.spectype.currentText(),
                                wearer=self.subtype.currentText(),
                                abilities=self.abilities)
            else:
                item = self.cls(type=self.spectype.currentText(),
                                abilities=self.abilities)

        # Amulet
        elif self.cls == AmuletStockItem:
            if self._notset(self.subtype):
                return self.error('You must specify the amulet type!')

            type = self.subtype.currentText()
            if type == 'Skepticism':
                ability = AmuletAbility(type, size=self.charges.value())

            elif type == 'Attribute':
                if self._notset(self.spectype):
                    return self.error('You must choose an attribute!')
                attr = self.spectype.currentText().split('+')[0]
                ability = AmuletAbility(type, attr=attr)

            elif type == 'Proof':
                if self._notset(self.spectype):
                    return self.error('You must choose an element!')
                ability = AmuletAbility(type, 
                                        element=self.spectype.currentText())

            elif type == 'Control':
                if self._notset(self.spectype):
                    return self.error('You must choose a creature type!')
                ability = AmuletAbility(type + ' ' + 
                                        self.spectype.currentText())

            else:
                raise GUIError('Uh-oh! Invalid amulet type?')

            item = self.cls(abilities=[ability])

        # Ring
        elif self.cls == RingStockItem:
            if not self.abilities:
                return self.error('You must specify at least one ability!')
            item = self.cls(self.abilities)

        # Rod
        elif self.cls == RodStockItem:
            if self._notset(self.ability):
                return self.error('Please choose an element!')
            ability = MentalAbility(self.ability.currentText(),
                                    self.abilitysize.value())
            item = RodStockItem(self.charges.value(), ability)

        # Book/Scroll
        elif self.cls == BookStockItem or self.cls == ScrollStockItem:
            if not self.abilities:
                return self.error('You must specify at least one ability!')
            item = self.cls(abilities=self.abilities, 
                            language=self.language.currentText())

        # Gem
        elif self.cls == GemStockItem:
            if self._notset(self.ability):
                return self.error('You must choose an ability!')
            ability = MentalAbilityWithOpposites(self.ability.currentText(),
                                                 self.abilitysize.value())
            item = self.cls(ability)

        # Potion
        elif self.cls == PotionStockItem:
            if self._notset(self.subtype):
                return self.error('You must choose a potion class!')
            type = self.subtype.currentText()

            if type == 'Healing':
                item = HealingPotionStockItem(self.charges.value())

            elif type == 'Weapon Poison':
                if self._notset(self.spectype):
                    return self.error('Please select damage size!')
                dmg = self.spectype.currentText()
                if self.language.isEnabled():
                    item = WeaponPoisonStockItem(dmg, doses=1,
                                       type=self.language.currentText())
                else:
                    item = WeaponPoisonStockItem(dmg, doses=1)

            elif type == 'Grenade':
                if self._notset([self.spectype, self.language]):
                    return self.error('You must specify both type' +
                                      ' and damage!')
                item = GrenadeStockItem(dmg=self.spectype.currentText(),
                                        type=self.language.currentText())

            elif type == 'Attribute':
                if self._notset(self.ability):
                    return self.error('Please choose an attribute!')
                ability = AttributeAbility(self.ability.currentText(),
                                           self.abilitysize.value())
                item = AttributePotionStockItem(ability)

            elif type == 'Ability':
                if self._notset(self.ability):
                    return self.error('Please choose an ability!')
                ability = MentalAbilityWithOpposites(self.ability.currentText(),
                                                     self.abilitysize.value())
                item = AbilityPotionStockItem(ability)

            else:
                item = SpecialPotionStockItem(self.spectype.currentText())

        else:
            raise GUIError('Uh-oh: Unknown item class!')

        # Item should be set now...
        player = self.player.text()
        character = self.character.text()
        if player or character:
            if not (player and character):
                return self.error('You must specify both player AND' +
                                  'character to log a commission!')
            # Won't work for HealingPotion!!
            item.set_commission(player, character)

        # Confirm
        msg = ("Adding new item to %s.\n\n" % self.store.name + 
               "Item: %s\n\n" % item.short() +
               "FMV: %s\n\n" % item.value +
               "Are you sure you wish to continue?")
        res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'Add Item', msg,
                                QtGui.QMessageBox.Yes |
                                QtGui.QMessageBox.No).exec_()
        if res != QtGui.QMessageBox.Yes:
            return

        # Add item
        self.store.additem(item)
        self.parent.town.save()
        self.parent._buildtree(expand=self.store)
        self.window_.close()





class SecondaryWeaponWidget(QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setWindowTitle('Specify secondary weapon')
        self.window_.setCentralWidget(self)
        self.window_.show()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)

        # Display primary details
        primarybox = QtGui.QLabel(self)
        primarybox.setText('Primary Weapon:\n\n' +
                           'Type: %s\n' % self.parent.spectype.currentText() +
                           'Abilities:\n' + 
                           '\n'.join(['  %s' % i 
                                      for i in self.parent.abilities]) + 
                           '\n\n\nSecondary Weapon:\n')
        mbox.addWidget(primarybox)

        # Determine available styles
        if 'Bow' in self.parent.subtype.currentText():
            stylelist = ['Sword', 'Ax/Mace/Hammer', 'Pole Weapon',
                         'Unusual Weapon']
        else:
            stylelist = ['Drawn Bow', 'Cross Bow']

        # Weapon class / type
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        box.addWidget(QtGui.QLabel('Weapon Class: ', self))
        self.weaponclass = QtGui.QComboBox(self)
        self.weaponclass.addItem('Choose weapon class')
        self.weaponclass.addItems(stylelist)
        box.addWidget(self.weaponclass)
        self.connect(self.weaponclass,  
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_class)
        box.addWidget(QtGui.QLabel('Weapon Type: ', self))
        self.weapontype = QtGui.QComboBox(self)
        self.weapontype.addItem('Choose weapon type')
        self.weapontype.setEnabled(False)
        box.addWidget(self.weapontype)

        # Ability Storage/Display
        self.abilities = [WeaponAbility('Changling')]
        self.abilitiesbox = QtGui.QLabel('Current Abilities:\n' +
                                         '  Changling\n', self)
        mbox.addWidget(self.abilitiesbox)

        # Abilities: Type
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        box.addWidget(QtGui.QLabel('New Ability: ', self))
        self.abilitytype = QtGui.QComboBox(self)
        self.abilitytype.addItem('Choose Ability Type')
        self.abilitytype.addItems(('Special', 'Enhanced', 'Attribute'))
        self.connect(self.abilitytype,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_abilitytype)
        box.addWidget(self.abilitytype)

        # Abilities: Ability
        self.ability_label = QtGui.QLabel('Subtype: ', self)
        box.addWidget(self.ability_label)
        self.ability = QtGui.QComboBox(self)
        self.ability.addItem('Choose Ability Type')
        self.connect(self.ability,
                     QtCore.SIGNAL('currentIndexChanged(QString)'),
                     self.updated_ability)
        self.ability.setEnabled(False)
        box.addWidget(self.ability)

        # Abilities: IIQ/Bonus
        self.abilitysize_label = QtGui.QLabel('IIQ: ', self)
        box.addWidget(self.abilitysize_label)
        self.abilitysize = QtGui.QSpinBox(self)
        self.abilitysize.setRange(1, 5)
        self.abilitysize.setEnabled(False)
        box.addWidget(self.abilitysize)

        # Abilities: Add
        self.ability_btn = QtGui.QPushButton('Add', self)
        self.connect(self.ability_btn, QtCore.SIGNAL('clicked()'), 
                     self.add_ability)
        box.addWidget(self.ability_btn)

        # Gather list of abilities (and sort) for later use
        list = MentalAbilityWithOpposites.getabilities()
        self.all_mental_abilities = [i for i in list.keys()]
        self.all_mental_abilities.sort()

        # Buttons
        box = QtGui.QHBoxLayout()
        mbox.addLayout(box)
        self.OK = QtGui.QPushButton('Add Item', self)
        self.connect(self.OK, QtCore.SIGNAL('clicked()'), self.create)
        box.addWidget(self.OK)
        self.cancel = QtGui.QPushButton('Cancel', self)
        box.addWidget(self.cancel)

        self.show()
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'), 
                     self.window_.close)

    def updated_class(self, type):
        self.weapontype.clear()
        self.weapontype.addItem('Choose a weapon')
        self.weapontype.addItems(Weapon.weaponlist(type))
        self.weapontype.setEnabled(True)

    def updated_abilitytype(self, type):

        if type == 'Special':
            self.ability.clear()
            self.ability.addItem('Choose special ability')
            self.ability.addItems(WeaponAbility.typelist)
            self.ability.setEnabled(True)
            self.abilitysize.setEnabled(False)

        elif type == 'Enhanced':
            self.ability.clear()
            self.ability.addItem('Choose mental ability')
            self.ability.addItems(self.all_mental_abilities)
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('IIQ: ')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        elif type == 'Attribute':  # always Weapon
            self.ability.clear()
            self.ability.addItem('Choose an attribute')
            self.ability.addItems(('ST', 'DX', 'Dam'))
            self.ability.setEnabled(True)

            self.abilitysize_label.setText('Bonus: +')
            self.abilitysize.setRange(1, 5)
            self.abilitysize.setEnabled(True)

        #else: do nothing

    def updated_ability(self, type):

         if type in WeaponAbility.typelist:
             self.abilitysize.setEnabled(False)

         if type == 'Animated':
             self.abilitysize_label.setText('Range (MH): ')
             self.abilitysize.setRange(1, 5)
             self.abilitysize.setEnabled(True)

         elif type == 'Defender':
             self.abilitysize_label.setText('Dx Penalty: ')
             self.abilitysize.setRange(1, 5)
             self.abilitysize.setEnabled(True)

    def _notset(self, field):
        if '__iter__' in dir(field):
            for f in field:
                if self._notset(f): return True
            return False
        if field.currentText().startswith('Choose'): return True
        if field.currentText().startswith('Select'): return True
        return False

    def _update_abilitiesbox(self):
        text = 'Current Abilities:\n'
        for ability in self.abilities:
            text += '  ' + str(ability) + '\n'
        self.abilitiesbox.setText(text)

    def add_enhanced(self, enhanced):
        ability = MentalAbilityWithOpposites(self.ability.currentText(),
                                             self.abilitysize.value())
        if ability in enhanced.abilities:
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                     'Duplicate Mental Ability',
                                     '%s is already on this item!' % ability,
                                     QtGui.QMessageBox.Ok).exec_()
        abilities = enhanced.abilities + [ability]
        i = self.abilities.index(enhanced)
        self.abilities[i] = WeaponAbility('Enhanced', 
                                          abilities = enhanced.abilities)
        self.ability.setCurrentIndex(0)
        self._update_abilitiesbox()

    def add_ability(self):

        """Add specified ability to abilities list."""

        # Verify ability is fully specified
        if self._notset((self.abilitytype, self.ability)):
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                     'Ability Not Selected',
                                     'Please specify an ability first!',
                                     QtGui.QMessageBox.Ok).exec_()


        # Handle Enhanced 'next'
        if self.abilitytype.currentText() == 'Enhanced':
            for abil in self.abilities:
                if isinstance(abil, WeaponAbility) and abil.type == 'Enhanced':
                    return self.add_enhanced(abil)
            else:
                ma = MentalAbilityWithOpposites(self.ability.currentText(),
                                                self.abilitysize.value())
                ability = WeaponAbility('Enhanced', abilities=[ma])

        # Character ability?
        elif 'Ability' in self.abilitytype.currentText():
            ability = PhysicalOrMentalAbility(self.ability.currentText(),
                                              self.abilitysize.value())

        # Attribute ability?
        elif 'Attribute' in self.abilitytype.currentText():
            ability = AttributeAbility(self.ability.currentText(),
                                       self.abilitysize.value())

        # Weapon ability? (other than Enhanced)
        elif self.abilitytype.currentText() == 'Special':
            if self.ability.currentText() == 'Animated':
                ability = WeaponAbility('Animated', 
                                        range=self.abilitysize.value())
            elif self.ability.currentText() == 'Defender':
                ability = WeaponAbility('Defender',
                                        size=self.abilitysize.value())
            else:
                ability = WeaponAbility(self.ability.currentText())



        # Prevent duplicates
        if ability in self.abilities:
            return QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                     'Duplicate Ability',
                                     '%s is already on this item!' % ability,
                                     QtGui.QMessageBox.Ok).exec_()

        # Save ability
        self.abilities.append(ability)

        # Is the item 'full'?
        num = len(self.abilities)
        if num >= Weapon.maxabilities:
            self.ability_btn.setEnabled(False)

        # Reset
        self.abilitytype.setCurrentIndex(0)
        self.ability.setCurrentIndex(0)

        # Update static field
        self._update_abilitiesbox()

    def error(self, msg):
        QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Cannot create item',
                          msg, QtGui.QMessageBox.Ok).exec_()

    def create(self):
        if self._notset(self.weapontype):
            return self.error('You must choose a weapon type!')
        self.parent.secondaryweapon = Weapon(type=self.weapontype.currentText(),
                                             abilities=self.abilities,
                                             secondary=True)

        msg = ("Defining a Changling requires two weapon definitions." +
               " If you continue, the secondary weapon will be:\n\n" +
               "Type: %s" % self.weapontype.currentText() + '\n' +
               "Abilities:\n")
        for a in self.abilities:
            msg += '  %s\n' % a
        msg += ("\nAre you ready to continue, and add this item to %s?" %
                self.parent.store.name)
        res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'Confirm second weapon', msg,
                                QtGui.QMessageBox.Yes |
                                QtGui.QMessageBox.No).exec_()
        if res != QtGui.QMessageBox.Yes:
            return

        self.emit(QtCore.SIGNAL('secondary_done'))
        self.window_.close()

