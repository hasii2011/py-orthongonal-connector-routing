
from typing import cast
from typing import Any
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from dataclasses import field
from dataclasses import dataclass

from orthogonalrouting.graph.Edge import edgesFactory
if TYPE_CHECKING:
    from orthogonalrouting.graph.interfaces.IEdge import Edges


@dataclass
class GraphEdge:

    data:   Any = None
    key:    Any = data.key

    source:      'GraphVertex' = cast('GraphVertex', None)
    destination: 'GraphVertex' = cast('GraphVertex', None)

    weight: float = 0.0

    def __str__(self) -> str:
        return self.data.__str__()


@dataclass
class GraphVertex:

    key:  Any = None
    x:    int = 0
    y:    int = 0
    data: Any = None

    edges: 'Edges' = field(default_factory=edgesFactory)


class Graph:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)
    weight: float = 0.0
