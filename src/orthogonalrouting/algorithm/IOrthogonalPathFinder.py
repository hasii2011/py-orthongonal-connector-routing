
from typing import List

from abc import ABC
from abc import abstractmethod

from orthogonalrouting.enumerations.SearchAlgorithm import SearchAlgorithm
from orthogonalrouting.enumerations.ConnectorOrientation import ConnectorOrientation

from orthogonalrouting.graph.interfaces.INode import INode
from orthogonalrouting.models.Connection import Connections

from orthogonalrouting.models.IInput import IInput
from orthogonalrouting.models.Point import Point
from orthogonalrouting.models.Connection import Connection
from orthogonalrouting.models.ShortestGraphPath import ShortestGraphPath

from orthogonalrouting.models.logicModels.Connector import Connector


class IOrthogonalPathFinder(ABC):

    @property
    @abstractmethod
    def margin(self) -> int:
        pass

    @margin.setter
    @abstractmethod
    def margin(self, value: int):
        pass

    # Algorithm steps

    @abstractmethod
    def createLeadLines(self, items: List[IInput], maxWidth: int, maxHeight: int) -> Connections:
        pass

    @abstractmethod
    def findIntersection(self, lineA: Connection, lineB: Connection) -> Point:
        pass

    @abstractmethod
    def constructGraph(self, intersections: List[Point]):
        pass

    @abstractmethod
    def shortestPath(self, startNode: INode, finishNode: INode, searchAlgorithm: SearchAlgorithm) -> ShortestGraphPath:
        pass

    @abstractmethod
    def calculatePathForConnector(self, targetConnector: Connector, searchAlgorithm: SearchAlgorithm) -> ShortestGraphPath:
        pass

    # end off steps

    @abstractmethod
    def calculateOrientation(self, item: IInput, relativeCoordinates: Point) -> ConnectorOrientation:
        pass
