
from dataclasses import dataclass
from dataclasses import field

from orthogonalrouting.models.Connection import Connections
from orthogonalrouting.models.Connection import connectionsFactory

from orthogonalrouting.models.Point import Points
from orthogonalrouting.models.Point import pointsFactory

from orthogonalrouting.models.ShortestGraphPath import ShortestGraphPath
from orthogonalrouting.models.ShortestGraphPath import shortestGraphPathFactory


@dataclass
class AlgorithmResults:

    connections:   Connections       = field(default_factory=connectionsFactory)
    intersections: Points            = field(default_factory=pointsFactory)
    shortestPath:  ShortestGraphPath = field(default_factory=shortestGraphPathFactory)
