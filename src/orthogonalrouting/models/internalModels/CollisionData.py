
from sys import maxsize

from dataclasses import dataclass

from orthogonalrouting.Common import NOT_SET_BOOLEAN
from orthogonalrouting.Common import NOT_SET_SENTINEL
from orthogonalrouting.Common import X_SENTINEL
from orthogonalrouting.Common import Y_SENTINEL


@dataclass
class CollisionData:

    startPoint:   int  = NOT_SET_SENTINEL
    startX:       int  = X_SENTINEL
    startY:       int  = Y_SENTINEL
    endX:         int  = X_SENTINEL
    endY:         int  = Y_SENTINEL
    maximum:      int  = maxsize // 2
    oppositeSide: int  = NOT_SET_SENTINEL
    isVertical:   bool = NOT_SET_BOOLEAN
