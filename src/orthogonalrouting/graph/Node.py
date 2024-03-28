
from logging import Logger
from logging import getLogger
from typing import cast

from orthogonalrouting.Common import X_SENTINEL
from orthogonalrouting.Common import Y_SENTINEL
from orthogonalrouting.graph.interfaces.INode import INode
from orthogonalrouting.models.Point import Point


class Node(INode):
    """
    Simulate C# 'default' node by setting x and y sentinel value
    """

    def __init__(self, x: int = X_SENTINEL, y: int = Y_SENTINEL):

        self.logger: Logger = getLogger(__name__)

        self._x: int = x
        self._y: int = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int):
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int):
        self._y = y

    @property
    def position(self) -> Point:
        return Point(x=self._x, y=self._y)

    @property
    def key(self) -> str:
        return f'[{self.x},{self.y}]'

    def __eq__(self, other) -> bool:

        ans: bool = False
        if isinstance(other, INode) is True:
            if self.x == other.x and self.y == other.y:
                ans = True

        return ans

    def __hash__(self):
        return hash(str(self))

    def __str__(self) -> str:
        return self.key

    def __repr__(self) -> str:
        return self.__str__()


NO_NODE: Node = cast(Node, None)
