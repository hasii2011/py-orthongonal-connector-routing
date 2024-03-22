
from abc import ABC
from abc import abstractmethod
from typing import Any

from orthogonalrouting.graph.Nodes import Nodes
from orthogonalrouting.graph.interfaces.IEdge import IEdge
from orthogonalrouting.graph.interfaces.INode import INode


class IGraph(ABC):

    @abstractmethod
    def addNode(self, node: INode):
        pass

    @abstractmethod
    def addNodes(self, nodes: Nodes):
        pass

    @abstractmethod
    def AddEdge(self, firstNode: INode, secondNode: INode, edge: IEdge):
        pass

    @abstractmethod
    def removeNode(self, node: INode):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def removeEdge(self, firstNode: INode, secondNode: INode, edge: IEdge = None):
        """
        This is my version of method overloading for this method.   I have to some
        work to do in the implementation

        Remove edge between the two nodes or remove it by explicitly providing it
        Args:
            firstNode:
            secondNode:
            edge:
        """
        pass

    @abstractmethod
    def find(self, x: int = -1, y: int = -1, key: Any = None) -> INode:
        """
        Find the node at location or by an associated key
        Args:
            x:
            y:
            key:
        """
        pass

    @abstractmethod
    def intervalFind(self, x1: int, y1: int, x2: int, y2: int) -> Nodes:
        pass
