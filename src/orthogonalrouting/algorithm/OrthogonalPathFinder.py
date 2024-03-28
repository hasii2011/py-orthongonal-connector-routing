from typing import Dict
from typing import List
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from orthogonalrouting.Common import FLOAT_MAX
from orthogonalrouting.Common import NOT_SET_INT

from orthogonalrouting.algorithm.CollisionDetection import CollisionDetection
from orthogonalrouting.algorithm.CollisionDetection import DetectedCollision
from orthogonalrouting.algorithm.CollisionDetection import DetectedCollisions
from orthogonalrouting.algorithm.CollisionDetection import detectedCollisionsFactory

from orthogonalrouting.algorithm.IOrthogonalPathFinder import IOrthogonalPathFinder

from orthogonalrouting.enumerations.ConnectorOrientation import ConnectorOrientation
from orthogonalrouting.enumerations.SearchAlgorithm import SearchAlgorithm
from orthogonalrouting.graph.Edge import Edge
from orthogonalrouting.graph.Graph import Graph
from orthogonalrouting.graph.Node import Node
from orthogonalrouting.graph.Nodes import Nodes
from orthogonalrouting.graph.interfaces.IEdge import Edges

from orthogonalrouting.graph.interfaces.INode import INode
from orthogonalrouting.models.AlgorithmResults import AlgorithmResults

from orthogonalrouting.models.Connection import Connection
from orthogonalrouting.models.Connection import Connections
from orthogonalrouting.models.Connection import connectionsFactory

from orthogonalrouting.models.IInput import IInput
from orthogonalrouting.models.Point import Point
from orthogonalrouting.models.Point import Points
from orthogonalrouting.models.Point import pointsFactory
from orthogonalrouting.models.ShortestGraphPath import ShortestGraphPath
from orthogonalrouting.models.internalModels.CollisionData import CollisionData
from orthogonalrouting.models.logicModels.Connector import Connector


@dataclass(slots=True)
class YBottomValue:
    y:      int = NOT_SET_INT
    bottom: int = NOT_SET_INT


@dataclass(slots=True)
class XRightValue:
    x:     int = NOT_SET_INT
    right: int = NOT_SET_INT


LeftCollision           = YBottomValue
RightCollision          = YBottomValue
VerticalMiddleCollision = YBottomValue
TopCollision            = XRightValue

XAxisItems = NewType('XAxisItems', Dict[YBottomValue, XRightValue])
YAxisItems = NewType('YAxisItems', Dict[XRightValue,  YBottomValue])

LeftCollisions           = NewType('LeftCollisions',           List[LeftCollision])
RightCollisions          = NewType('RightCollisions',          List[LeftCollision])
VerticalMiddleCollisions = NewType('VerticalMiddleCollisions', List[VerticalMiddleCollision])
TopCollisions            = NewType('TopCollisions',            List[TopCollision])


class OrthogonalPathFinder(IOrthogonalPathFinder):

    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._margin: int = 0

        self._graph:              Graph              = Graph()
        self._collisionDetection: CollisionDetection = CollisionDetection()
        self._connections:        Connections        = connectionsFactory()

    @property
    def margin(self) -> int:
        return self._margin

    @margin.setter
    def margin(self, value: int):
        self._margin = value

    def constructGraph(self, intersections: List[Point]):

        self._graph.clear()

        for p in intersections:
            intersection: Point = cast(Point, p)
            edges: Connections = connectionsFactory()
            #  Find edges
            for c in self._connections:
                connection: Connection = cast(Connection, c)
                if self._isInsideLine(line=connection, x=intersection.x, y=intersection.y) is True:
                    edges.append(connection)
                # Every intersection has only two edges
                if len(edges) == 2:
                    break

            # Find possible neighbors
            possibleNeighbors: Points = pointsFactory()
            for c in edges:
                edge: Connection = cast(Connection, c)
                for pp in intersections:
                    point: Point = cast(Point, pp)
                    if self._isInsideLine(line=edge, x=point.x, y=point.y) and intersection != point:
                        possibleNeighbors.append(point)

            #  Find nearest neighbors
            left:   Point = cast(Point, None)
            right:  Point = cast(Point, None)
            top:    Point = cast(Point, None)
            bottom: Point = cast(Point, None)
            for n in possibleNeighbors:
                neighbor: Point = cast(Point, n)
                if neighbor.x < intersection.x and neighbor.y == intersection.y and (left is None or left.x < neighbor.x):
                    left = neighbor
                elif neighbor.x > intersection.x and neighbor.y == intersection.y and (right is None or right.x > neighbor.x):
                    right = neighbor
                elif neighbor.y < intersection.y and neighbor.x == intersection.x and (top is None or top.y < neighbor.y):
                    top = neighbor
                elif neighbor.y > intersection.y and neighbor.x == intersection.x and (bottom is None or bottom.y > neighbor.y):
                    bottom = neighbor

            # Add vertices and edges to the graph
            self._addNode(intersection)
            vertices: Points = Points([left, right, top, bottom])
            for v in vertices:
                vertex: Point = cast(Point, v)
                if vertex is None:
                    pass
                else:
                    self._addNode(vertex)
                    self._addEdge(intersection, vertex)

    # noinspection PyChainedComparisons
    def createLeadLines(self, items: List[IInput], maxWidth: int, maxHeight: int) -> Connections:

        maxWidth  = maxWidth - self._margin     # TODO: Don't modify input parameters
        maxHeight = maxHeight - self._margin    # TODO: Don't modify input parameters
        xAxisItems: XAxisItems = XAxisItems({})
        yAxisItems: YAxisItems = YAxisItems({})
        # Create Horizontal & Vertical dictionaries
        for i in items:
            item: IInput = cast(IInput, i)
            yRange: YBottomValue = YBottomValue(y=item.y - self._margin, bottom=item.bottom + self._margin)
            xRange: XRightValue  = XRightValue(x=item.x - self._margin,  right=item.right + self._margin)

            if yRange not in xAxisItems.keys():
                xAxisItems[yRange] = xRange

            if xRange not in yAxisItems.keys():
                yAxisItems[xRange] = yRange

        self._connections = connectionsFactory()

        # Create lead lines
        for i in items:
            item = cast(IInput, i)
            # Vertical Lines

            leftCollisions:           LeftCollisions           = LeftCollisions([])
            rightCollisions:          RightCollisions          = RightCollisions([])
            verticalMiddleCollisions: VerticalMiddleCollisions = VerticalMiddleCollisions([])
            median = self._calculateMedian(a=item.x, b=item.right)

            for r in yAxisItems.keys():
                rangeValue: XRightValue = cast(XRightValue, r)
                if (item.x - self._margin) == rangeValue.x and (item.right + self._margin) == rangeValue.right:
                    continue

                # noinspection PyChainedComparisons
                if (item.x - self._margin) >= rangeValue.x and (item.x - self._margin) <= rangeValue.right:
                    leftCollisions.append(yAxisItems[rangeValue])

                # noinspection PyChainedComparisons
                if (item.right + self._margin) >= rangeValue.x and (item.right + self._margin) <= rangeValue.right:
                    rightCollisions.append(yAxisItems[rangeValue])

                # noinspection PyChainedComparisons
                if median >= rangeValue.x and median <= rangeValue.right:
                    verticalMiddleCollisions.append(yAxisItems[rangeValue])

            cData: CollisionData = CollisionData()          # C# name was data, ugh

            cData.startPoint   = item.y - self._margin
            cData.startX       = item.x - self._margin
            cData.endX         = self._calculateMedian(a=item.x, b=item.right)
            cData.endY         = item.y - self._margin
            cData.oppositeSide = item.bottom + self._margin
            cData.maximum      = maxHeight
            cData.isVertical   = True

            detectedCollisions:     DetectedCollisions = self._fromLeftCollisionsToDetectedCollisions(leftCollisions=leftCollisions)
            detectedLeftCollisions: Connections        = self._collisionDetection.detectCollision(detectedCollisions, cData)

            self._connections = cast(Connections, self._connections + detectedLeftCollisions)
            # end of Vertical lines

            # Horizontal lines
            topCollisions:              TopCollisions = TopCollisions([])
            bottomCollisions:           TopCollisions = TopCollisions([])
            horizontalMiddleCollisions: TopCollisions = TopCollisions([])

            median = self._calculateMedian(item.y, item.bottom)
            for rKey in xAxisItems.keys():
                yBottomValue: YBottomValue = cast(YBottomValue, rKey)

                if (item.y - self._margin) == yBottomValue.y and (item.bottom + self._margin) == yBottomValue.bottom:
                    continue

                if (item.y - self._margin) >= yBottomValue.y and (item.y - self._margin) <= yBottomValue.bottom:
                    topCollisions.append(xAxisItems[yBottomValue])

                if (item.bottom + self._margin) >= yBottomValue.y and (item.bottom + self._margin) <= yBottomValue.bottom:
                    bottomCollisions.append(xAxisItems[yBottomValue])

                if median >= yBottomValue.y and median <= yBottomValue.bottom:
                    horizontalMiddleCollisions.append(xAxisItems[yBottomValue])

            dData: CollisionData = CollisionData()          # C# code reused data name, ugh

            dData.startPoint = item.x - self._margin
            dData.startX     = self._margin                 # Zero position
            dData.startY     = item.y - self._margin
            dData.endX       = maxWidth
            dData.endY       = item.y - self._margin
            dData.maximum    = maxWidth
            dData.isVertical = False

            detectedCollisions                 = self._fromTopCollisionsToDetectedCollisions(topCollisions)
            detectedTopCollisions: Connections = self._collisionDetection.detectCollision(detectedCollisions, dData)
            self._connections = cast(Connections, self._connections + detectedTopCollisions)

            dData.startY = dData.endY = item.bottom + self._margin

            detectedCollisions                 = self._fromTopCollisionsToDetectedCollisions(bottomCollisions)
            detectedBottomCollisions: Connections = self._collisionDetection.detectCollision(detectedCollisions, dData)
            self._connections = cast(Connections, self._connections + detectedBottomCollisions)

            eData: CollisionData = CollisionData()      # C# code reused data name, ugh

            eData.startPoint   = item.x - self._margin
            eData.startX       = self._margin                # Zero position
            eData.startY       = self._calculateMedian(item.y, item.bottom)
            eData.endX         = item.x - self._margin
            eData.endY         = self._calculateMedian(item.y, item.bottom)
            eData.oppositeSide = item.right + self._margin
            eData.maximum      = maxWidth
            eData.isVertical   = False

            # end of Horizontal lines

            detectedCollisions                        = self._fromTopCollisionsToDetectedCollisions(horizontalMiddleCollisions)
            detectedHorizontalCollisions: Connections = self._collisionDetection.connectorPointsCollisionDetection(detectedCollisions, eData)
            self._connections = cast(Connections, self._connections + detectedHorizontalCollisions)

        return self._connections

    def OrthogonalPath(self, items: List[IInput], maxWidth: int, maxHeight: int, searchAlgorithm: SearchAlgorithm, targetConnector: Connector) -> AlgorithmResults:

        connections:   Connections = self.createLeadLines(items, maxWidth, maxHeight)
        intersections: Points      = pointsFactory()

        for c in connections:
            conn: Connection = cast(Connection, c)
            for c2 in connections:
                conn2: Connection = cast(Connection, c2)
                if conn == conn2:
                    continue
                else:
                    intersection: Point = self.findIntersection(lineA=conn, lineB=conn2)
                    if intersection is not None:
                        intersections.append(intersection)
        # this.ConstructGraph(intersections.OrderBy(x => x.X).ThenBy(y => y.Y));
        intersections.sort(key=lambda point: (point.x, point.y))
        self.constructGraph(intersections)
        shortestPath: ShortestGraphPath = self.calculatePathForConnector(targetConnector, searchAlgorithm)

        return AlgorithmResults(
            connections=connections,
            intersections=intersections,
            shortestPath=shortestPath
        )

    def findIntersection(self, lineA: Connection, lineB: Connection) -> Point:

        A1: int = lineA.end.y - lineA.start.y
        B1: int = lineA.start.x - lineA.end.x
        C1: int = A1 * lineA.start.x + B1 * lineA.start.y

        A2: int = lineB.end.y - lineB.start.y
        B2: int = lineB.start.x - lineB.end.x
        C2: int = A2 * lineB.start.x + B2 * lineB.start.y

        determinant: int = A1 * B2 - A2 * B1
        if determinant == 0:
            return cast(Point, None)

        x: int = (B2 * C1 - B1 * C2) // determinant
        y: int = (A1 * C2 - A2 * C1) // determinant

        # x,y can intersect outside the line since line is infinitely long;
        # so finally check if x, y is within both the line segments
        if self._isInsideLine(lineA, x, y) and self._isInsideLine(lineB, x, y):

            return Point(x, y)

        return cast(Point, None)

    def shortestPath(self, startNode: INode, finishNode: INode, searchAlgorithm: SearchAlgorithm) -> ShortestGraphPath:
        """
        """
        assert searchAlgorithm == SearchAlgorithm.Dijkstra, 'Only support Dijkstra'

        nodeEdges: Tuple[Nodes, Edges] = self._graph.shortestPath(algorithm=searchAlgorithm, startNode=startNode, finishNode=finishNode)

        return ShortestGraphPath(pathNodes=nodeEdges[0], pathEdges=nodeEdges[1])

    # noinspection PyUnusedLocal
    def getShortestGraphPathInternal(self, startNode: INode, finishNode: INode, searchAlgorithm: SearchAlgorithm) -> ShortestGraphPath:
        return ShortestGraphPath()  # TODO  When we support the Astra algorithm

    def calculatePathForConnector(self, targetConnector: Connector, searchAlgorithm: SearchAlgorithm) -> ShortestGraphPath:
        """
        Ugh targetConnector updated !!!!

        Args:
            targetConnector:
            searchAlgorithm:

        Returns:

        """

        shortestPath: ShortestGraphPath = self.shortestPath(targetConnector.sourceNode(), targetConnector.destinationNode(), searchAlgorithm)
        for pEdge in shortestPath.pathEdges:
            pathEdge: Edge = cast(Edge, pEdge)
            connection: Connection = Connection(pathEdge.source.position, pathEdge.destination.position)
            targetConnector.connectorPath.append(connection)

        return ShortestGraphPath()

    def calculateOrientation(self, item: IInput, relativeCoordinates: Point) -> ConnectorOrientation:

        def indexOf(pointToCheck: Point) -> int:

            returnIndex: int = 0
            for x in range(len(coordinates)):
                if pointToCheck == coordinates[x]:
                    returnIndex = x
                    break
            return returnIndex

        coordinates: Points = Points([
            Point(0,               item.height // 2),   # LEFT
            Point(item.width // 2, 0),                  # TOP
            Point(item.width,      item.height // 2),   # RIGHT
            Point(item.width // 2, item.height)         # BOTTOM
        ]
        )

        closestPoint:           Point = Point()
        closestDistanceSquared: float = FLOAT_MAX
        for p in coordinates:
            point: Point = cast(Point, p)
            distanceSquared: float = pow(point.x - relativeCoordinates.x, 2) + pow(point.y - relativeCoordinates.y, 2)
            if distanceSquared < closestDistanceSquared:
                closestDistanceSquared = distanceSquared
                closestPoint = point

        # return (ConnectorOrientation)Enum.Parse(typeof(ConnectorOrientation), orientation.ToString());
        indexOfPoint: int = indexOf(closestPoint)

        orientation: ConnectorOrientation = ConnectorOrientation(indexOfPoint)

        return orientation

    def _addNode(self, data: Point):
        """

        Args:
            data:
        """
        node: INode = Node(data.x, data.y)
        if self._graph.find(x=data.x, y=data.y) is None:
            self._graph.addNode(node)

    def _addEdge(self, sourcePoint: Point, destinationPoint: Point):

        source:      Node = self._graph.find(x=sourcePoint.x,      y=sourcePoint.y)
        destination: Node = self._graph.find(x=destinationPoint.x, y=destinationPoint.y)

        edge: Edge = Edge()
        edge.source      = source
        edge.destination = destination
        edge.weight      = self._distance(source=Point(x=sourcePoint.x, y=sourcePoint.y),
                                          target=Point(x=destinationPoint.x, y=destinationPoint.y)
                                          )
        self._graph.addEdge(firstNode=source, secondNode=destination, edge=edge)

    def _isInsideLine(self, line: Connection, x: int, y: int) -> bool:
        """
            return (x >= line.Start.X && x <= line.End.X || x >= line.End.X && x <= line.Start.X) &&
                   (y >= line.Start.Y && y <= line.End.Y || y >= line.End.Y && y <= line.Start.Y);

        Args:
            line:
            x:
            y:

        Returns:
        """
        return (line.start.x <= x <= line.end.x or line.end.x <= x <= line.start.x) and (line.start.y <= y <= line.end.y or line.end.y <= y <= line.start.y)

    def _distance(self, source: Point, target: Point) -> float:
        return pow(target.x - source.x, 2) + pow(target.y - source.y, 2)

    def _calculateMedian(self, a: int, b: int) -> int:

        return (a + b) // 2

    def _fromLeftCollisionsToDetectedCollisions(self, leftCollisions: LeftCollisions) -> DetectedCollisions:

        detectedCollisions: DetectedCollisions = detectedCollisionsFactory()

        for left in leftCollisions:
            leftCollision: LeftCollision = cast(LeftCollision, left)
            detectedCollision: DetectedCollision = DetectedCollision(a=leftCollision.y, b=leftCollision.bottom)
            detectedCollisions.append(detectedCollision)

        return detectedCollisions

    def _fromTopCollisionsToDetectedCollisions(self, topCollisions: TopCollisions) -> DetectedCollisions:

        detectedCollisions: DetectedCollisions = detectedCollisionsFactory()
        for top in topCollisions:
            topCollision: TopCollision = cast(TopCollision, top)
            detectedCollision: DetectedCollision = DetectedCollision(a=topCollision.x, b=topCollision.right)
            detectedCollisions.append(detectedCollision)

        return detectedCollisions
