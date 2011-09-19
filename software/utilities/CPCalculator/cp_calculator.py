import sys
import math

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL

__version__ = '1.0'


def __dependencies_for_freezing():
    import sip


def calc_cp(melee, missile, strength, hits):
    ocp = (3.0 * melee + missile) / 4.0
    dcp = strength / 4.0 + hits
    return math.sqrt(ocp ** 2 + dcp ** 2)

def calc_dcl(primary, poison=0, num=1):
    return num * (primary + poison / 2.0)


class CPCalculator (QtGui.QWidget):

    def __init__(self):
        super(CPCalculator, self).__init__()
        self._initGUI()
        self._center()

    def _center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def _calculate(self):
        melee = calc_dcl(self.melee_dcl.value(),
                         self.melee_poison.value(),
                         self.melee_num.value())
        missile = calc_dcl(self.missile_dcl.value(),
                           self.missile_poison.value(),
                           self.missile_num.value())
        result = calc_cp(melee, missile, 
                         self.strength.value(), self.hits.value())
        self.cp.setText(str(result))

    def _initGUI(self):
        self.resize(100, 150)
        self.setWindowTitle("ELF Combat Power (CP) Calculator")

        # Melee Offensive Details
        melee_dcl = QtGui.QLabel("Primary Melee DCL:")
        self.melee_dcl = QtGui.QDoubleSpinBox()
        self.melee_dcl.setToolTip("The Damage Class (DCL) of the character's primary melee attack.")
        self.melee_dcl.setMinimum(0.0)
        self.melee_dcl.setSingleStep(0.5)
        melee_poison = QtGui.QLabel("Melee Poison:")
        self.melee_poison = QtGui.QDoubleSpinBox()
        self.melee_poison.setToolTip("The Damage Class (DCL) of poison used with the character's primary melee attack.  Enter 0.0 for no poison.")
        self.melee_poison.setMinimum(0.0)
        self.melee_poison.setSingleStep(0.5)
        melee_num = QtGui.QLabel("# of Attacks:")
        self.melee_num = QtGui.QSpinBox()
        self.melee_num.setToolTip("The number of times the character can use this melee attack in a single turn.")
        self.melee_num.setMinimum(0)

        # Ranged Offensive Details
        missile_dcl = QtGui.QLabel("Primary Missile DCL:")
        self.missile_dcl = QtGui.QDoubleSpinBox()
        self.missile_dcl.setToolTip("The Damage Class (DCL) of the character's primary ranged attack.  Enter 0.0 if the character has no ranged attack.")
        self.missile_dcl.setMinimum(0.0)
        self.missile_dcl.setSingleStep(0.5)
        missile_poison = QtGui.QLabel("Missile Poison:")
        self.missile_poison = QtGui.QDoubleSpinBox()
        self.missile_poison.setToolTip("The Damage Class (DCL) of poison used with the character's primary ranged attack.  Enter 0.0 for no poison.")
        self.missile_poison.setMinimum(0.0)
        self.missile_poison.setSingleStep(0.5)
        missile_num = QtGui.QLabel("# of Attacks:")
        self.missile_num = QtGui.QSpinBox()
        self.missile_num.setToolTip("The number of times the character can use this ranged attack in a single turn.")
        self.missile_num.setMinimum(0)

        # Defensive Details
        strength = QtGui.QLabel("Character Strength:")
        self.strength = QtGui.QSpinBox()
        self.strength.setToolTip("The number of hits the character can withstand (not counting armor) before passing out.")
        self.strength.setMinimum(1)
        self.strength.setMaximum(99999)
        hits = QtGui.QLabel("Hits Absorbed:")
        self.hits = QtGui.QSpinBox()
        self.hits.setToolTip("The number of hits the character can withstand before taking damage (e.g. from armor, shield, or Physical Fitness).")
        self.hits.setMinimum(0)

        # Calculator
        cp = QtGui.QLabel("Combat Power:")
        self.cp = QtGui.QLabel("")
        self.melee_dcl.valueChanged.connect(self._calculate)
        self.melee_poison.valueChanged.connect(self._calculate)
        self.melee_num.valueChanged.connect(self._calculate)
        self.missile_dcl.valueChanged.connect(self._calculate)
        self.missile_poison.valueChanged.connect(self._calculate)
        self.missile_num.valueChanged.connect(self._calculate)
        self.strength.valueChanged.connect(self._calculate)
        self.hits.valueChanged.connect(self._calculate)

        # Default Values
        self.melee_dcl.setValue(7.0)
        self.melee_num.setValue(1)
        self.missile_dcl.setValue(7.0)
        self.missile_num.setValue(1)
        self.strength.setValue(12)
        self._calculate()

        # Notes...  TODO: put in help?
        extra_help = ("Characters than can attack with both melee and missile in a single turn (e.g. dragons): enter the sum of the attacks' DCLs as a single melee attack.",
                      "Mental abilities that are commonly used should be considered here (e.g. Stone Flesh, Ethereal Bow).")

        # Layout
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(melee_dcl, 1, 0, 1, 2)
        grid.addWidget(self.melee_dcl, 1, 2)
        grid.addWidget(melee_poison, 2, 1)
        grid.addWidget(self.melee_poison, 2, 2)
        grid.addWidget(melee_num, 3, 1)
        grid.addWidget(self.melee_num, 3, 2)
        grid.addWidget(missile_dcl, 4, 0, 1, 2)
        grid.addWidget(self.missile_dcl, 4, 2)
        grid.addWidget(missile_poison, 5, 1)
        grid.addWidget(self.missile_poison, 5, 2)
        grid.addWidget(missile_num, 6, 1)
        grid.addWidget(self.missile_num, 6, 2)
        grid.addWidget(strength, 7, 0, 1, 2)
        grid.addWidget(self.strength, 7, 2)
        grid.addWidget(hits, 8, 0, 1, 2)
        grid.addWidget(self.hits, 8, 2)
        grid.addWidget(cp, 9, 0, 1, 2)
        grid.addWidget(self.cp, 9, 2)
        self.setLayout(grid)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cp = CPCalculator()
    cp.show()
    sys.exit(app.exec_())