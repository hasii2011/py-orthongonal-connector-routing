
from logging import Logger
from logging import getLogger

from orthogonalrouting.graph.Node import NO_NODE
from orthogonalrouting.graph.Node import Node
from orthogonalrouting.graph.interfaces.IEdge import Edges
from orthogonalrouting.graph.interfaces.IEdge import IEdge


class Edge(IEdge):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._key: str = ''
        self._source:      Node = NO_NODE
        self._destination: Node = NO_NODE
        self._weight:      float  = 0.0

    @property
    def key(self) -> str:
        return self._key

    @property
    def source(self) -> Node:
        return self._source

    @source.setter
    def source(self, node: Node):
        self._source = node

    @property
    def destination(self) -> Node:
        return self._destination

    @destination.setter
    def destination(self, node: Node):
        self._destination = node

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) :
        self._weight = value


def edgesFactory() -> Edges:
    return Edges([])
