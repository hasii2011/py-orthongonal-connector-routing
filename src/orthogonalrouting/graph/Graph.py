
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from orthogonalrouting.Common import NOT_SET_INT

from orthogonalrouting.enumerations.SearchAlgorithm import SearchAlgorithm

from orthogonalrouting.graph.interfaces.IEdge import Edges
from orthogonalrouting.graph.interfaces.IEdge import IEdge
from orthogonalrouting.graph.interfaces.INode import INode
from orthogonalrouting.graph.interfaces.INode import NO_INODE

from orthogonalrouting.graph.Node import Node
from orthogonalrouting.graph.Nodes import Nodes
from orthogonalrouting.graph.Nodes import nodesFactory
from orthogonalrouting.graph.Edge import edgesFactory
from orthogonalrouting.graph.GraphEdge import GraphEdge
from orthogonalrouting.graph.GraphEdge import GraphEdges
from orthogonalrouting.graph.GraphVertex import GraphVertex
from orthogonalrouting.graph.GraphVertex import GraphVertices

from orthogonalrouting.graph.shortestpathalgorithm.DijkstraAlgorithm import DijkstraAlgorithm
from orthogonalrouting.graph.shortestpathalgorithm.ISearchAlgorithm import ISearchAlgorithm

from orthogonalrouting.graph.bst.PriorityBST import PriorityBST


class Graph:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)
        # this.tree = new PriorityBST<GraphVertex, K>();
        self._tree: PriorityBST = PriorityBST()

    @property
    def nodesCount(self):
        return self._tree.count

    def addEdge(self, firstNode: INode, secondNode: INode, edge: IEdge):
        """

        Args:
            firstNode:
            secondNode:
            edge:
        """

        genericEdge: GraphEdge = GraphEdge()

        # Up cast !!
        genericEdge.source      = cast(GraphVertex, self._tree.find(x=edge.source.x,      y=edge.source.y))
        genericEdge.destination = cast(GraphVertex, self._tree.find(x=edge.destination.x, y=edge.destination.y))
        genericEdge.weight      = edge.weight
        genericEdge.data        = edge

        first: GraphVertex = cast(GraphVertex, self._tree.find(x=firstNode.x, y=firstNode.y))
        first.edges.append(genericEdge)

        second: GraphVertex = cast(GraphVertex, self._tree.find(x=secondNode.x, y=secondNode.y))
        second.edges.append(genericEdge)

    def addNode(self, node: Node):
        """

        Args:
            node:
        """
        graphVertex: GraphVertex = GraphVertex()
        graphVertex.key  = node.key
        graphVertex.x    = node.x
        graphVertex.y    = node.y
        graphVertex.data = node

        self._tree.insert(graphVertex)

    def addNodes(self, nodes: Nodes):

        for n in nodes:
            node: Node = cast(Node, n)
            self.addNode(node=node)

    def clear(self):
        self._tree.clear()

    def find(self, x: int = NOT_SET_INT, y: int = NOT_SET_INT, key: str = None) -> Node:
        """
        Poor man's method overload

        Args:
            x:
            y:
            key:

        Returns:  The data associated with the GraphVertex.
        May return None if no data
        """
        if x == NOT_SET_INT:
            return self.findByKey(key=key)  # type: ignore
        else:
            return self.findByCoordinates(x=x, y=y)

    def findByKey(self, key: str):
        result: INode = cast(GraphVertex, self._tree.find(key=key))

        if result == NO_INODE:
            return result
        else:
            graphVertex: GraphVertex = cast(GraphVertex, result)
            return graphVertex.data

    def findByCoordinates(self, x: int, y: int):
        result: INode = cast(GraphVertex, self._tree.find(x=x, y=y))
        if result == NO_INODE:
            return result
        else:
            graphVertex: GraphVertex = cast(GraphVertex, result)
            return graphVertex.data

    def findEdges(self, node: INode) -> Edges:
        """

        Args:
            node:

        Returns:  The edges that the input node participates in
        """
        edgesToReturn: Edges = edgesFactory()

        treeNode = self._tree.find(x=node.x, y=node.y)
        if treeNode == NO_INODE:
            pass
        else:
            nodes: GraphVertices = cast(GraphVertices, self._tree.nodes)
            for n in nodes:
                graphVertex: GraphVertex = cast(GraphVertex, n)
                nodeEdges: GraphEdges = graphVertex.edges
                for e in nodeEdges:
                    graphEdge: GraphEdge = cast(GraphEdge, e)
                    if graphEdge.source.key == node.key or graphEdge.destination.key == node.key:
                        edgesToReturn.append(graphEdge.data)

        return edgesToReturn

    def intervalFind(self, x1: int, y1: int, x2: int, y2: int) -> Nodes:
        """

        Args:
            x1:
            y1:
            x2:
            y2:

        Returns:
        """

        interval: Nodes = nodesFactory()

        results: GraphVertices = cast(GraphVertices, self._tree.intervalFind(x1=x1, y1=y1, x2=x2, y2=y2))

        for item in results:
            graphVertex: GraphVertex = cast(GraphVertex, item)
            interval.append(graphVertex.data)

        return interval

    def removeEdge(self, edge: IEdge):
        self._removeEdgeBetweenNodes(firstNode=edge.source, secondNode=edge.destination)

    def removeNode(self, node: INode):
        foundNode: INode = self._tree.find(x=node.x, y=node.y)

        self._tree.remove(foundNode)

    def shortestPath(self, algorithm: SearchAlgorithm, startNode: Node, finishNode: Node) -> Tuple[Nodes, Edges]:

        searchAlgorithm: ISearchAlgorithm
        if algorithm == SearchAlgorithm.Dijkstra:
            searchAlgorithm = DijkstraAlgorithm()
        else:
            assert False, 'Alternate search algorithm not yet implemented'

        results: Tuple[Nodes, Edges] = searchAlgorithm.shortestPath(tree=self._tree, startNode=startNode, finishNode=finishNode)

        return results

    def _removeEdgeBetweenNodes(self, firstNode: INode, secondNode: INode):

        first:  GraphVertex = cast(GraphVertex, self._tree.find(x=firstNode.x,  y=firstNode.y))
        second: GraphVertex = cast(GraphVertex, self._tree.find(x=secondNode.x, y=secondNode.y))
        if first == NO_INODE or second == NO_INODE:
            return
        else:
            # var edge = first.Edges.Except(second.Edges).FirstOrDefault();
            difference:  GraphEdges = self._difference(first=first.edges, second=second.edges)
            edgeToRemove: GraphEdge = self._firstOrNone(edges=difference)

            if edgeToRemove is not None:
                first.edges.remove(edgeToRemove)
                second.edges.remove(edgeToRemove)

    def _difference(self, first: GraphEdges, second: GraphEdges) -> GraphEdges:

        if len(first) >= len(second):
            return self._realDifference(longerList=first, shorterList=second)
        else:
            return self._realDifference(longerList=second, shorterList=first)

    def _realDifference(self, longerList: GraphEdges, shorterList: GraphEdges) -> GraphEdges:

        differenceList: GraphEdges = GraphEdges([])

        for element in longerList:
            if element not in shorterList:
                differenceList.append(element)

        return differenceList

    def _firstOrNone(self, edges: GraphEdges):
        if len(edges) == 0:
            return None
        else:
            return edges[0]
