
from dataclasses import dataclass
from dataclasses import field

from orthogonalrouting.graph.Edge import edgesFactory
from orthogonalrouting.graph.Nodes import Nodes
from orthogonalrouting.graph.Nodes import nodesFactory

from orthogonalrouting.graph.interfaces.IEdge import Edges


@dataclass
class ShortestPath:

    pathNodes: Nodes = field(default_factory=nodesFactory)
    pathEdges: Edges = field(default_factory=edgesFactory)
