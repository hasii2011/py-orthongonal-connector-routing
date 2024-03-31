
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger

from orthogonalrouting.Common import NOT_SET_INT

from orthogonalrouting.models.IInput import IInput
from orthogonalrouting.models.IInput import InputList


class DemoItem(IInput):

    def __init__(self, x: int = NOT_SET_INT, y: int = NOT_SET_INT, width: int = NOT_SET_INT, height: int = NOT_SET_INT):
        self.logger: Logger = getLogger(__name__)

        self._x:      int = x
        self._y:      int = y
        self._width:  int = width
        self._height: int = height

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def right(self) -> int:
        return self._x + self._width

    @property
    def bottom(self) -> int:
        return self._y + self._height

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value


DemoItems = InputList


def demoItemsFactory() -> DemoItems:
    return DemoItems([])
