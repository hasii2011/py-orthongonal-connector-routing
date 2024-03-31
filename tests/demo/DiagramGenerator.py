
from logging import Logger
from logging import getLogger

from tests.demo.DemoItem import DemoItem
from tests.demo.DemoItem import DemoItems
from tests.demo.DemoItem import demoItemsFactory


class DiagramGenerator:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._demoItems: DemoItems = demoItemsFactory()

    @property
    def demoItems(self) -> DemoItems:
        return self._demoItems

    def generateDefaultItems(self):

        self._demoItems.append(DemoItem(x=50,  y=150, height=50,  width=130))
        self._demoItems.append(DemoItem(x=400, y=130, height=50,  width=130))
        self._demoItems.append(DemoItem(x=440, y=50,  height=50,  width=150))
        self._demoItems.append(DemoItem(x=420, y=270, height=50,  width=130))
        self._demoItems.append(DemoItem(x=270, y=110, height=150, width=50))
