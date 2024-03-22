
from typing import cast

from logging import Logger
from logging import getLogger

from orthogonalrouting.graph.interfaces.IEdge import Edges
from orthogonalrouting.graph.interfaces.IEdge import IEdge
from orthogonalrouting.graph.interfaces.INode import INode

NO_NODE: INode = cast(INode, None)


class Edge(IEdge):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._key: str = ''
        self._source:      INode = NO_NODE
        self._destination: INode = NO_NODE
        self._weight:      float  = 0.0

    @property
    def key(self) -> str:
        return self._key

    @property
    def source(self) -> INode:
        return self._source

    @source.setter
    def source(self, node: INode):
        self._source = node

    @property
    def destination(self) -> INode:
        return self._destination

    @destination.setter
    def destination(self, node: INode):
        self._destination = node

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) :
        self._weight = value


def edgesFactory() -> Edges:
    return Edges([])
