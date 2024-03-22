
from typing import List
from typing import NewType

from dataclasses import dataclass


@dataclass
class Point:

    x: int = 0
    y: int = 0


Points = NewType('Points', List[Point])


def pointsFactory() -> Points:
    return Points([])
