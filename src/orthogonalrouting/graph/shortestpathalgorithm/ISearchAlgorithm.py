
from typing import Tuple

from abc import ABC
from abc import abstractmethod

from orthogonalrouting.graph.Nodes import Nodes

from orthogonalrouting.graph.bst.IPriorityBST import IPriorityBST

from orthogonalrouting.graph.interfaces.IEdge import Edges
from orthogonalrouting.graph.interfaces.INode import INode


class ISearchAlgorithm(ABC):

    @abstractmethod
    def shortestPath(self, tree: IPriorityBST, startNode: INode, finishNode: INode) -> Tuple[Nodes, Edges]:
        pass
