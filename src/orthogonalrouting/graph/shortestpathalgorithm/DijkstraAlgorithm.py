
from typing import cast
from typing import Dict
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger

from sys import float_info
from sys import maxsize

from orthogonalrouting.graph.GraphEdge import GraphEdge
from orthogonalrouting.graph.GraphVertex import GraphVertex

from orthogonalrouting.graph.Nodes import Nodes
from orthogonalrouting.graph.Nodes import nodesFactory

from orthogonalrouting.graph.bst.IPriorityBST import IPriorityBST

from orthogonalrouting.graph.interfaces.IEdge import Edges
from orthogonalrouting.graph.interfaces.INode import INode

from orthogonalrouting.graph.priorityqueue.IPriorityQueue import IPriorityQueue
from orthogonalrouting.graph.priorityqueue.SimplePriorityQueue import SimplePriorityQueue

from orthogonalrouting.graph.shortestpathalgorithm.ISearchAlgorithm import ISearchAlgorithm


CostDictionary = NewType('CostDictionary', Dict[GraphVertex, float])
PreviousNodes  = NewType('PreviousNodes',  Dict[GraphVertex, GraphVertex])
VisitedNodes   = NewType('VisitedNodes',   List[GraphVertex])
Paths          = NewType('Paths',          Dict[GraphVertex, GraphEdge])

DOUBLE_MAX: float = float_info.max
INT_MAX:    int   = maxsize


class DijkstraAlgorithm(ISearchAlgorithm):

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._minPriorityQueue: IPriorityQueue = SimplePriorityQueue()
        #             var totalCosts = new Dictionary<Graph<N, E, K>.GraphVertex, double>();
        #             var prevNodes = new Dictionary<Graph<N, E, K>.GraphVertex, Graph<N, E, K>.GraphVertex>();
        self._totalCosts:    CostDictionary = CostDictionary({})
        self._previousNodes: PreviousNodes  = PreviousNodes({})
        self._visited:       VisitedNodes   = VisitedNodes([])
        self._paths:         Paths          = Paths({})

    def shortestPath(self, tree: IPriorityBST, startNode: INode, finishNode: INode) -> Tuple[Nodes, Edges]:

        treeStartNode = tree.find(startNode.x, startNode.y)
        self._totalCosts[cast(GraphVertex, treeStartNode)] = 0

        self._minPriorityQueue.enqueue(data=treeStartNode, priority=0)

        for n in tree.nodes:
            node: INode = cast(INode, n)
            if node.key != startNode.key:
                self._totalCosts[cast(GraphVertex, node)] = DOUBLE_MAX
                self._minPriorityQueue.enqueue(data=node, priority=INT_MAX)
        #
        #   TODO !!!
        #
        while self._minPriorityQueue.count > 0:
            newSmallest: GraphVertex = self._minPriorityQueue.dequeue()
            self._visited.append(newSmallest)
            for edge in newSmallest.edges:
                # possiblyUnvisitedNode = edge.source == edge.destination : edge.source
                pass

        edges:        Edges = Edges([])
        shortestPath: Nodes = nodesFactory()

        return shortestPath, edges
