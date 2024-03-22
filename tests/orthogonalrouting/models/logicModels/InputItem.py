
from logging import Logger
from logging import getLogger

from orthogonalrouting.Common import HEIGHT_SENTINEL
from orthogonalrouting.Common import NOT_SET_SENTINEL
from orthogonalrouting.Common import WIDTH_SENTINEL
from orthogonalrouting.Common import X_SENTINEL
from orthogonalrouting.Common import Y_SENTINEL

from orthogonalrouting.models.IInput import IInput


class InputItem(IInput):
    """
    Test Object
    """
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._x: int = X_SENTINEL
        self._y: int = Y_SENTINEL

        self._width:  int = WIDTH_SENTINEL
        self._height: int = HEIGHT_SENTINEL

        self._right:  int = NOT_SET_SENTINEL
        self._bottom: int = NOT_SET_SENTINEL

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
        return self._right

    @right.setter
    def right(self, value: int):
        self._right = value

    @property
    def bottom(self) -> int:
        return self._bottom

    @bottom.setter
    def bottom(self, value: int):
        self._bottom = value

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
