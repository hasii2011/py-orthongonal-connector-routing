
from typing import cast

from logging import Logger
from logging import getLogger


from orthogonalrouting.graph.interfaces.IEdge import Edges
from orthogonalrouting.graph.interfaces.IEdge import IEdge
from orthogonalrouting.graph.interfaces.INode import INode
from orthogonalrouting.graph.interfaces.INode import NO_NODE

from orthogonalrouting.graph.Edge import edgesFactory
from orthogonalrouting.graph.GraphEdge import GraphEdge
from orthogonalrouting.graph.GraphEdge import GraphEdges

from orthogonalrouting.graph.GraphVertex import GraphVertex
from orthogonalrouting.graph.GraphVertex import GraphVertices

from orthogonalrouting.graph.Nodes import Nodes
from orthogonalrouting.graph.Nodes import nodesFactory

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

    def addNode(self, node: INode):
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
            node: INode = cast(INode, n)
            self.addNode(node=node)

    def clear(self):
        self._tree.clear()

    def find(self, key: str) -> INode:
        """

        Args:
            key:

        Returns:  The data associated with the GraphVertex.
        May return None if no data

        """
        result: INode = cast(GraphVertex, self._tree.find(key=key))
        if result == NO_NODE:
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
        if treeNode == NO_NODE:
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

    def _removeEdgeBetweenNodes(self, firstNode: INode, secondNode: INode):

        first:  GraphVertex = cast(GraphVertex, self._tree.find(x=firstNode.x,  y=firstNode.y))
        second: GraphVertex = cast(GraphVertex, self._tree.find(x=secondNode.x, y=secondNode.y))
        if first == NO_NODE or second == NO_NODE:
            return
        else:
            # var edge = first.Edges.Except(second.Edges).FirstOrDefault();
            pass
