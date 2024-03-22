
from typing import TYPE_CHECKING
from typing import Any

from abc import ABC
from abc import abstractmethod

from orthogonalrouting.graph.Nodes import Nodes

if TYPE_CHECKING:
    from orthogonalrouting.graph.bst.PriorityBST import PriorityBSTNode

from orthogonalrouting.graph.interfaces.INode import INode


class IPriorityBST(ABC):


    @property
    @abstractmethod
    def rootBSTNode(self) -> 'PriorityBSTNode':
        pass

    @property
    @abstractmethod
    def root(self) -> INode:
        pass

    @property
    @abstractmethod
    def count(self) -> int:
        pass

    @property
    @abstractmethod
    def isEmpty(self) -> bool:
        pass

    @property
    @abstractmethod
    def nodes(self) -> Nodes:
        pass

    @nodes.setter
    @abstractmethod
    def nodes(self, nodes: Nodes):
        pass

    # IEnumerator<N> GetEnumerator();
    @abstractmethod
    def find(self, x: int = -1, y: int = -1, key: Any = None, node: INode = None) -> INode:
        """
        Find the node at location, Node or by an associated key
        Args:
            x:
            y:
            key:
            node:
        """
        pass

    @abstractmethod
    def intervalFind(self, x1: int, y1: int, x2: int, y2: int) -> Nodes:
        pass

    @abstractmethod
    def contains(self, node: INode) -> bool:
        pass

    @abstractmethod
    def insert(self, node: INode):
        pass

    @abstractmethod
    def remove(self, node: INode):
        pass

    @abstractmethod
    def buildTree(self, nodes: Nodes):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def toList(self) -> Nodes:
        pass
