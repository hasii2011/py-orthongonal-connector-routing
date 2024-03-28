
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from orthogonalrouting.Common import NOT_SET_INT

from orthogonalrouting.models.Connection import Connection
from orthogonalrouting.models.Connection import Connections
from orthogonalrouting.models.Connection import connectionsFactory
from orthogonalrouting.models.Point import Point

from orthogonalrouting.models.internalModels.CollisionData import CollisionData


@dataclass(kw_only=True, slots=True)
class DetectedCollision:
    a: int
    b: int


@dataclass(kw_only=True, slots=True)
class MinMax:
    minimum: int = NOT_SET_INT
    maximum: int = NOT_SET_INT


DetectedCollisions = NewType('DetectedCollisions', List[DetectedCollision])


def detectedCollisionsFactory() -> DetectedCollisions:
    return DetectedCollisions([])


class CollisionDetection:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def detectCollision(self, detectedCollisions: DetectedCollisions, data: CollisionData) -> Connections:

        if len(detectedCollisions) == 1:
            return self._singleCollision(detectedCollisions=detectedCollisions, data=data)
        elif len(detectedCollisions) > 1:
            return self._multipleCollisions(detectedCollisions, data)
        else:
            # no collision
            selfie: Connections = connectionsFactory()
            self._createConnection(data.startX, data.startY, data.endX, data.endY, selfie)
            return selfie

    def connectorPointsCollisionDetection(self, detectedCollisions: DetectedCollisions, data: CollisionData) -> Connections:

        collisionConnections: Connections = Connections([])

        if len(detectedCollisions) == 0:
            self._createConnection(data.startX, data.oppositeSide, data.endX, data.maximum, collisionConnections)   # Ugh will update collisionConnections
            if data.isVertical is True:
                self._createConnection(data.startX, data.oppositeSide, data.endX, data.maximum, collisionConnections)
            else:
                self._createConnection(data.oppositeSide, data.startY, data.maximum, data.endY, collisionConnections)
        else:
            minMax: MinMax = self._findMinMax(detectedCollisions, data)
            if data.isVertical is True:
                self._createConnection(data.startX, minMax.minimum,    data.endX, data.endY,      collisionConnections)
                self._createConnection(data.startX, data.oppositeSide, data.endX, minMax.maximum, collisionConnections)
            else:
                self._createConnection(minMax.minimum,    data.startY, data.endX,      data.endY, collisionConnections)
                self._createConnection(data.oppositeSide, data.startY, minMax.maximum, data.endY, collisionConnections)

        return collisionConnections

    def _singleCollision(self, detectedCollisions: DetectedCollisions, data: CollisionData) -> Connections:

        collisionConnections: Connections = connectionsFactory()
        # left collision
        if detectedCollisions[0].b < data.startPoint:
            if data.isVertical is True:
                self._createConnection(data.startX, detectedCollisions[0].b, data.endX, data.endY, collisionConnections)
            else:
                self._createConnection(detectedCollisions[0].b, data.startY, data.endX, data.endY, collisionConnections)
        else:
            # right collision
            if data.isVertical is True:
                self._createConnection(data.startX, data.startY, data.endX, detectedCollisions[0].a, collisionConnections)
            else:
                self._createConnection(data.startX, data.startY, detectedCollisions[0].a, data.endY, collisionConnections)
        return collisionConnections

    def _multipleCollisions(self, detectedCollisions: DetectedCollisions, data: CollisionData) -> Connections:

        collisionConnections: Connections = connectionsFactory()
        minMax: MinMax = self._findMinMax(detectedCollisions, data)
        if data.isVertical is True:
            self._createConnection(data.startX, minMax.minimum, data.endX, minMax.maximum, collisionConnections)
        else:
            self._createConnection(minMax.minimum, data.startY, minMax.maximum, data.endY, collisionConnections)

        return collisionConnections

    def _createConnection(self, startX: int, startY: int, endX: int, endY: int, connections: Connections) -> Connection:
        """
        Has the side affect that the connections list is modified
        TODO:  Do not like the side affect

        Args:
            startX:
            startY:
            endX:
            endY:
            connections:

        Returns:  The created connection
        """
        if connections is None:
            connections = connectionsFactory()  # TODO:  I don't like this

        collisionConnection: Connection = Connection(start=Point(x=startX, y=startY), end=Point(x=endX, y=endY))
        connections.append(collisionConnection)

        return collisionConnection

    # noinspection PyChainedComparisons
    def _findMinMax(self, detectedCollisions: DetectedCollisions, data: CollisionData) -> MinMax:

        minimum: int = 0
        maximum: int = data.maximum

        for c in detectedCollisions:
            collision: DetectedCollision = cast(DetectedCollision, c)

            if collision.b < data.startPoint and collision.b > minimum:
                minimum = collision.b
            elif collision.a > data.startPoint and collision.a < maximum:
                maximum = collision.a

        minMax: MinMax = MinMax(minimum=minimum, maximum=maximum)

        return minMax
