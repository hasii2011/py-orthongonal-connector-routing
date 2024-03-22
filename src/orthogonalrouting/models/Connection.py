from typing import List
from typing import NewType

from orthogonalrouting.models.Point import Point
from orthogonalrouting.models.Point import Points


class Connection:
    def __init__(self, start: Point, end: Point):

        self._points: Points = Points([start, end])

    @property
    def points(self) -> Points:
        return self._points

    @points.setter
    def points(self, value: Points):
        self._points = value

    @property
    def start(self) -> Point:
        return self._points[0]

    @property
    def end(self) -> Point:
        return self._points[1]


Connections = NewType('Connections', List[Connection])


def connectionsFactory() -> Connections:
    return Connections([])
