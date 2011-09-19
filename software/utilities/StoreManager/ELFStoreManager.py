import sys

from PyQt4 import QtGui, QtCore

from elvenfire import ELFError
from elvenfire.storemanager.GUI.continent import ContinentWidget


VERSION = '0.1.2'


def main():
    app = QtGui.QApplication(sys.argv)
    
    try:
        mw = ContinentWidget(None)
        mw.window_.setWindowTitle('ELF Store Manager v%s' % VERSION)
        sys.exit(app.exec_())
    except ELFError as e:
        QtGui.QMessageBox(QtGui.QMessageBox.Critical, "Error", 
                          "Unexpected error encountered:\n\n" + str(e),
                          QtGui.QMessageBox.Ok).exec_()
        raise e ## DEBUG


if __name__ == '__main__':
    main()