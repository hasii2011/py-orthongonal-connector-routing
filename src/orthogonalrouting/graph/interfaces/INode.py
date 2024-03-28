
from typing import Any
from typing import cast

from abc import ABC
from abc import abstractmethod


class INode(ABC):

    @property
    @abstractmethod
    def x(self) -> int:
        pass

    @x.setter
    @abstractmethod
    def x(self, value: int):
        pass

    @property
    @abstractmethod
    def y(self) -> int:
        pass

    @y.setter
    @abstractmethod
    def y(self, value: int):
        pass

    @property
    @abstractmethod
    def key(self) -> Any:
        pass


NO_INODE: INode = cast(INode, None)
