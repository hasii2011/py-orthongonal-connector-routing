
from typing import Any
from typing import List
from typing import NewType
from typing import TYPE_CHECKING
from typing import cast

from orthogonalrouting.Common import NO_STRING
from orthogonalrouting.graph.interfaces.IEdge import IEdge

if TYPE_CHECKING:
    from orthogonalrouting.graph.GraphVertex import GraphVertex


class GraphEdge(IEdge):

    def __init__(self):

        self._key:         str = NO_STRING
        self._weight:      float = 0.0

        self._data:        Any         = None
        self._source:      'GraphVertex' = cast('GraphVertex', None)
        self._destination: 'GraphVertex' = cast('GraphVertex', None)

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    @property
    def source(self) -> 'GraphVertex':
        return self._source

    @source.setter
    def source(self, value: 'GraphVertex'):
        self._source = value

    @property
    def destination(self) -> 'GraphVertex':
        return self._destination

    @destination.setter
    def destination(self, value: 'GraphVertex'):
        self._destination = value

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float):
        self._weight = value

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, value: Any):
        self._data = value


GraphEdges = NewType('GraphEdges', List[GraphEdge])


def graphEdgesFactory() -> GraphEdges:
    return GraphEdges([])
