import random
import pickle
import glob

from PyQt4 import QtGui, QtCore

from storemanager.locations.town import Town
from storemanager.GUI.town import TownWidget
from storemanager.GUI.search import SearchWidget, ResultsWindow
from storemanager.GUI.treeitems import *


class NewTownWidget(QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setWindowTitle('Create New Town...')
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

        # Town Name
        nbox = QtGui.QHBoxLayout()
        mbox.addLayout(nbox)
        nbox.addWidget(QtGui.QLabel('Name: ', self))
        self.namebox = QtGui.QLineEdit('', self)
        randomname = Town('Test').randomname_nodupes()
        self.namebox.setText(randomname)
        nbox.addWidget(self.namebox)

        # Town Size
        sbox = QtGui.QHBoxLayout()
        mbox.addLayout(sbox)
        sbox.addWidget(QtGui.QLabel('Size: ', self))
        self.sizebox = QtGui.QSpinBox(self)
        self.sizebox.setValue(random.randint(1, 5))
        self.sizebox.setRange(1, 10)
        sbox.addWidget(self.sizebox)

        # OK
        self.OK = QtGui.QPushButton('OK', self)
        self.connect(self.OK, QtCore.SIGNAL('clicked()'), self.create)
        mbox.addWidget(self.OK)

        self.show()

    def create(self):
        name = self.namebox.text()
        if name == '':
            QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                              'Create New Town',
                              'You must enter a name for the town!', 
                              QtGui.QMessageBox.Ok).exec_()
            return
        try:
            size = int(self.sizebox.value())
        except ValueError as e:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                              'Create New Town',
                              'Invalid integer size!', 
                              QtGui.QMessageBox.Ok).exec_()
            return
        if size > 5:
            res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                    'Create New Town',
                                    'Most towns will not be above size 5;' +
                                    ' are you SURE you wish to create a' +
                                    ' size %s town?' % size,
                                    QtGui.QMessageBox.Yes |
                                    QtGui.QMessageBox.No).exec_()
            if res != QtGui.QMessageBox.Yes:
                self.sizebox.setValue(5)
                return
        t = Town(name, size)
        try:
            t.save()
        except IOError:
            QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                              'Create New Town',
                              'Invalid town name; please try again!', 
                              QtGui.QMessageBox.Ok).exec_()
            return
        self.emit(QtCore.SIGNAL('town_created'))
        TownWidget(self.parent, t)
        self.window_.close()


class PrePopulateWidget (QtGui.QWidget):

    def show(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setWindowTitle('Pre-Populate Continent...')
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

        # Number of Towns
        nbox = QtGui.QHBoxLayout()
        mbox.addLayout(nbox)
        nbox.addWidget(QtGui.QLabel('# of Towns: ', self))
        self.numbox = QtGui.QSpinBox(self)
        self.numbox.setValue(10)
        self.numbox.setRange(1, 100)
        nbox.addWidget(self.numbox)

        # Town Size Range
        sbox = QtGui.QHBoxLayout()
        mbox.addLayout(sbox)
        sbox.addWidget(QtGui.QLabel('Size Range: ', self))
        self.min = QtGui.QSpinBox(self)
        self.min.setValue(1)
        self.min.setRange(1, 10)
        sbox.addWidget(self.min)
        sbox.addWidget(QtGui.QLabel(' to ', self))
        self.max = QtGui.QSpinBox(self)
        self.max.setValue(5)
        self.max.setRange(1, 10)
        sbox.addWidget(self.max)

        # Buttons
        bbox = QtGui.QHBoxLayout()
        mbox.addLayout(bbox)
        self.OK = QtGui.QPushButton('Create Towns', self)
        bbox.addWidget(self.OK)
        self.connect(self.OK, QtCore.SIGNAL('clicked()'), self.create)
        self.cancel = QtGui.QPushButton('Cancel', self)
        bbox.addWidget(self.cancel)

        self.show()
        self.connect(self.cancel, QtCore.SIGNAL('clicked()'), self.canceled)

    def create(self):
        for i in range(self.numbox.value()):
            size = random.randint(self.min.value(), self.max.value())
            t = Town(None, size)
            t.save()
        self.emit(QtCore.SIGNAL('population_done'))
        self.window_.close()

    def canceled(self):
        self.emit(QtCore.SIGNAL('population_done'))
        self.window_.close()


class ContinentWidget(QtGui.QWidget):

    def _prepare(self):
        self.window_ = QtGui.QMainWindow()
        self.window_.setGeometry(200, 200, 600, 300)
        self.window_.setWindowTitle('ELF Store Manager')
        self.window_.setCentralWidget(self)
        self.center()

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

    def show(self):
        self.window_.show()

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self._prepare()
        self._gathertowns()

        # Offer to pre-populate a blank continent
        if self.townlist == []:
            res = QtGui.QMessageBox(QtGui.QMessageBox.Information,
                                    'Pre-Populate Continent?',
                                    'There are currently no towns available' +
                                    ' on this continent. Would you like to' +
                                    ' pre-populate your continent with a' +
                                    ' selection of automatically generated' +
                                    ' towns at this time?',
                                    QtGui.QMessageBox.Yes | 
                                    QtGui.QMessageBox.No).exec_()
            if res == QtGui.QMessageBox.Yes:
                pw = PrePopulateWidget(self)
                self.connect(pw, QtCore.SIGNAL('population_done'), 
                             self._populated)
                return  ## wait for completion

        self._continue()

    def _populated(self):
        self._gathertowns()
        self._continue()

    def _continue(self):

        # Header
        mbox = QtGui.QVBoxLayout()
        self.setLayout(mbox)
        mbox.addWidget(QtGui.QLabel('Welcome to Peurondia!', self))
        mbox.addWidget(QtGui.QLabel('Please select a town...', self))

        # Primary left-right box
        hbox = QtGui.QHBoxLayout()
        mbox.addLayout(hbox)

        # Town selection
        self.townselect = QtGui.QTreeWidget(self)
        self.townselect.setSortingEnabled(True)
        hbox.addWidget(self.townselect)
        self._buildlist()
        self.connect(self.townselect, 
                     QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem *, int)'), 
                     self.open_town)

        # Buttons: Cross-Continent
        vbox = QtGui.QVBoxLayout()
        hbox.addLayout(vbox)
        self.search = QtGui.QPushButton('Search All', self)
        self.connect(self.search, QtCore.SIGNAL('clicked()'), self.search_all)
        vbox.addWidget(self.search)
        self.update = QtGui.QPushButton('Update All', self)
        self.connect(self.update, QtCore.SIGNAL('clicked()'), self.update_all)
        vbox.addWidget(self.update)
        sep = QtGui.QFrame(self)
        sep.setFrameShape(QtGui.QFrame.HLine)
        vbox.addWidget(sep)

        # Buttons: Modify Stores
        self.new = QtGui.QPushButton('New...', self)
        self.connect(self.new, QtCore.SIGNAL('clicked()'), self.new_town)
        vbox.addWidget(self.new)
        self.rename_ = QtGui.QPushButton('Rename', self)
        self.connect(self.rename_, QtCore.SIGNAL('clicked()'), self.rename)
        vbox.addWidget(self.rename_)
        self.delete = QtGui.QPushButton('Delete', self)
        self.connect(self.delete, QtCore.SIGNAL('clicked()'), self.delete_town)
        vbox.addWidget(self.delete)
        sep = QtGui.QFrame(self)
        sep.setFrameShape(QtGui.QFrame.HLine)
        vbox.addWidget(sep)

        # Buttons: Enter Town
        self.OK = QtGui.QPushButton('Enter Town', self)
        self.connect(self.OK, QtCore.SIGNAL('clicked()'), self.open_town)
        vbox.addWidget(self.OK)

        self.show()

    def search_all(self):
        sw = SearchWidget(self, None)
        self.connect(sw, QtCore.SIGNAL('QuickSearch()'), self.search_done)

    def search_done(self):
        results = []
        for town in self.townlist:
            for store in town.stores:
                list = self.searchcriteria.search(store)
                for item in list:
                    item.store = store
                    item.town = town
                results += list
        if results == []:
            QtGui.QMessageBox(QtGui.QMessageBox.Information, 'No Results',
                              'There are no items available matching your' + \
                              ' specified criteria.', QtGui.QMessageBox.Ok).exec_()
            return
        ResultsWindow(self, results)

    def update_all(self):
        res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'Confirm Update',
                                'Are you SURE you wish to update ALL towns'
                                + ' at this time? Prices will be updated, and'
                                + ' items may be sold or added when you update.',
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_()
        if (res == QtGui.QMessageBox.Yes):
            removedlist = []
            for town in self.townlist:
                removedlist += town.update()
                town.save()
            self._buildlist()
            CommissionWindow(self, removedlist)

    def _selected(self):
        i = self.townselect.currentItem()
        if 'town' in dir(i):
            return i.town
        return None

    def _gathertowns(self):
        townfiles = glob.glob('towns/*.town')
        self.townlist = []
        for file in townfiles:
            myfile = open(file, 'rb')
            town = pickle.load(myfile)
            myfile.close()
            self.townlist.append(town)

    def _buildlist(self, recheck=False):
        if recheck:
            self._gathertowns()
        self.townselect.clear()
        self.townselect.setColumnCount(4)
        self.townselect.setHeaderLabels(('', 'Name', 'Size', '# Stores'))
        for town in self.townlist:
            TownTree(self.townselect, town)

    def new_town(self):
        """Create a new town."""
        tw = NewTownWidget(self)
        self.connect(tw.ntw, QtCore.SIGNAL('town_created'), 
                     self.new_town_done)

    def new_town_done(self):
        self._buildlist(recheck=True)

    def rename(self):
        """Rename the selected town/store."""
        i = self.townselect.currentItem()
        if 'store' in dir(i):
            loc = i.store
        else:
            loc = i.town
            loc.delete()
        name, ok = QtGui.QInputDialog.getText(None, "Rename %s" % loc.name,
                                        "Enter a new name for %s:" % loc.name,
                                        QtGui.QLineEdit.Normal, str(loc.name))
        if ok:
            loc.name = name
            i.rename(str(loc))
        i.town.save()  # always save, to replace town removal on a cancel

    def delete_town(self):
        """Delete the selected town."""
        town = self._selected()
        if town is None:
            QtGui.QMessageBox(QtGui.QMessageBox.Information,
                              'Delete Town', 'No town selected!', 
                              QtGui.QMessageBox.Ok).exec_()
            return
        res = QtGui.QMessageBox(QtGui.QMessageBox.Warning,
                                'Delete Town?!',
                                'Are you SURE you want to permanently' +
                                ' delete %s?' % town,
                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No).exec_()
        if (res == QtGui.QMessageBox.Yes):
            town.delete()
            self.townselect.removeItemWidget(self.townselect.currentItem(), 0)
            self.townlist.remove(town)

    def open_town(self):
        town = self._selected()
        if town is None:
            QtGui.QMessageBox(QtGui.QMessageBox.Information,
                              'Open Town', 'No town selected!', 
                              QtGui.QMessageBox.Ok).exec_()
            return
        TownWidget(self, town)

    def keyPressEvent(self, event):
        # Enter -> Enter Town
        if event.key() == QtCore.Qt.Key_Return or \
           event.key() == QtCore.Qt.Key_Enter:
            self.entertown()
        # Ctrl+F -> Find
        elif event.key() == QtCore.Qt.Key_F and \
             event.modifiers() == QtCore.Qt.ControlModifier:
            self.search()
        # Ctrl+U -> Update
        elif event.key() == QtCore.Qt.Key_U and \
             event.modifiers() == QtCore.Qt.ControlModifier:
            self.update()
        # Pass unrecognized
        else:
            QWidget.keyPressEvent(self, event)
