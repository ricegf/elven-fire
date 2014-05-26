
from elvenfire.creatures.trainable import TrainableAnimal
from elvenfire.artifacts.special import SpecialArtifact, STBattery
from storemanager.stockitems import _StockItem

class TrainableAnimalStockItem (_StockItem):

    """TrainableAnimal for sale.

    New attributes:
      self.animal -- TrainableAnimal type

    """

    def __init__(self, name=None, subtype=None):
        self.animal = TrainableAnimal(name, subtype)
        self.name = self.animal.name
        if self.animal.subtype is not None:
            self.name = "%s: %s" % (self.animal.subtype, self.animal.name)
        self.desc = str(self.animal)
        self.value = self.animal.value()
        _StockItem.__init__(self)


class SpecialArtifactStockItem (_StockItem, SpecialArtifact):
    """Special Artifact for sale."""
    def __init__(self, type=None, ability=None, IIQ=None, IQ=None, size=None):
        SpecialArtifact.__init__(self, type, ability, IIQ, IQ, size)
        _StockItem.__init__(self)


class STBatteryStockItem (_StockItem, STBattery):
    """Strength Battery for sale."""
    def __init__(self, charges=None):
        STBattery.__init__(self, charges)
        _StockItem.__init__(self)


