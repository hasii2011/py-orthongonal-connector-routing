
from typing import Any
from typing import List
from typing import NewType

from orthogonalrouting.Common import NOT_SET_INT
from orthogonalrouting.Common import NO_STRING

from orthogonalrouting.graph.GraphEdge import GraphEdges
from orthogonalrouting.graph.GraphEdge import graphEdgesFactory

from orthogonalrouting.graph.interfaces.INode import INode


class GraphVertex(INode):

    def __init__(self):

        self._x:   int = NOT_SET_INT
        self._y:   int = NOT_SET_INT
        self._key: str = NO_STRING

        self._data:  Any         = None
        self._edges: GraphEdges  = graphEdgesFactory()

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, value: Any):
        self._data = value

    @property
    def edges(self) -> GraphEdges:
        return self._edges

    @edges.setter
    def edges(self, value: GraphEdges):
        self._edges = value

    def __str__(self):
        return self._data.__str__()


GraphVertices = NewType('GraphVertices', List[GraphVertex])
