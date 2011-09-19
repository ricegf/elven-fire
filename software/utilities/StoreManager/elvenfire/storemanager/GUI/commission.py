from PyQt4 import QtGui, QtCore

from elvenfire.storemanager.GUI.treeitems import ItemTree

class CommissionWindow(QtGui.QMainWindow):

    def __init__(self, parent, removedlist):
        QtGui.QMainWindow.__init__(self, parent)
        self.setGeometry(200, 100, 600, 300)
        self.setWindowTitle('Commissions Due')
        display = QtGui.QTreeWidget(self)
        self.setCentralWidget(display)

        display.setColumnCount(5)
        display.setSortingEnabled(True)
        count = 0
        for item in removedlist:
            if item.commission:
                CommissionTree(display, item)
                count += 1
        if count > 0:
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


class CommissionTree (ItemTree):

    col_icon = 0
    col_name = 1
    col_player = 2
    col_character = 3
    col_commission = 4

    def __init__(self, parent, item):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.item = item

        self.setText(self.col_name, item.short())
        self.setToolTip(self.col_name, item.description())
        (player, character, commission) = item.get_commission()
        self.setText(self.col_player, player)
        self.setText(self.col_character, character)
        self.setText(self.col_commission, str(commission))
        self.setTextAlignment(self.col_commission, QtCore.Qt.AlignRight)
        self.setToolTip(self.col_commission, 'FMV: $%s\n' % item.value +
                                             'Sale price: $%s' % item.price())

        self.treeWidget().setHeaderLabels(('', 'Name', 'Player', 'Character',
                                           'Commission ($)'))
        self.treeWidget().setColumnWidth(self.col_icon, 50)
        self.treeWidget().setColumnWidth(self.col_name, 270)
        self.treeWidget().setColumnWidth(self.col_player, 80)
        self.treeWidget().setColumnWidth(self.col_character, 100)
        self.treeWidget().setColumnWidth(self.col_commission, 50)


