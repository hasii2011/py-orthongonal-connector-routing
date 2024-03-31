
from typing import List
from typing import NewType

from abc import ABC
from abc import abstractmethod


class IInput(ABC):

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
    def right(self) -> int:
        pass

    @property
    @abstractmethod
    def bottom(self) -> int:
        pass

    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @width.setter
    @abstractmethod
    def width(self, value: int):
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @height.setter
    @abstractmethod
    def height(self, value: int):
        pass


InputList = NewType('InputList', List[IInput])