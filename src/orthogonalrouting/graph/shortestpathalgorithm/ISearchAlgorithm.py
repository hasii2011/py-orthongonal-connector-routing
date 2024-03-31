
from typing import Tuple

from abc import ABC
from abc import abstractmethod

from orthogonalrouting.graph.Node import Node
from orthogonalrouting.graph.Nodes import Nodes

from orthogonalrouting.graph.bst.IPriorityBST import IPriorityBST

from orthogonalrouting.graph.interfaces.IEdge import Edges


class ISearchAlgorithm(ABC):

    @abstractmethod
    def shortestPath(self, tree: IPriorityBST, startNode: Node, finishNode: Node) -> Tuple[Nodes, Edges]:
        pass
