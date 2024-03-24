
from typing import Any

from abc import ABC
from abc import abstractmethod
from typing import List
from typing import NewType

from orthogonalrouting.graph.interfaces.INode import INode


class IEdge(ABC):

    @property
    @abstractmethod
    def key(self) -> Any:
        pass

    @property
    @abstractmethod
    def source(self) -> INode:
        pass

    @source.setter
    @abstractmethod
    def source(self, value: INode):
        pass

    @property
    @abstractmethod
    def destination(self) -> INode:
        pass

    @destination.setter
    @abstractmethod
    def destination(self, value: INode):
        pass

    @property
    @abstractmethod
    def weight(self) -> float:
        pass

    @weight.setter
    @abstractmethod
    def weight(self, value: float):
        pass


Edges = NewType('Edges', List[IEdge])

