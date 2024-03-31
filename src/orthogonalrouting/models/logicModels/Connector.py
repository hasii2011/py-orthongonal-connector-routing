
from typing import cast
from typing import List
from typing import NewType

from dataclasses import dataclass
from dataclasses import field

from orthogonalrouting.enumerations.ConnectorOrientation import ConnectorOrientation

from orthogonalrouting.graph.Node import Node

from orthogonalrouting.models.Connection import Connection
from orthogonalrouting.models.IInput import IInput

ConnectorPath = NewType('ConnectorPath', List[Connection])


def connectorPathFactory() -> ConnectorPath:
    return ConnectorPath([])


@dataclass
class Connector:
    source:                 IInput               = cast(IInput, None)
    destination:            IInput               = cast(IInput, None)
    connectorPath:          ConnectorPath        = field(default_factory=connectorPathFactory)
    sourceOrientation:      ConnectorOrientation = ConnectorOrientation.NOT_SET
    destinationOrientation: ConnectorOrientation = ConnectorOrientation.NOT_SET

    def sourceNode(self) -> Node:
        return self._calculateOrientationNode(orientation=self.sourceOrientation, item=self.source)

    def destinationNode(self) -> Node:
        return self._calculateOrientationNode(orientation=self.destinationOrientation, item=self.destination)

    def _calculateOrientationNode(self, orientation: ConnectorOrientation, item: IInput) -> Node:

        match orientation:
            case ConnectorOrientation.LEFT:
                return Node(x=item.x, y=item.y + item.height // 2)

            case ConnectorOrientation.RIGHT:
                return Node(x=item.right, y=item.y + item.height // 2)

            case ConnectorOrientation.TOP:
                return Node(x=item.x + item.width // 2, y=item.y)

            case ConnectorOrientation.BOTTOM:
                return Node(x=item.x + item.width // 2, y=item.bottom)
            case _:
                return cast(Node, None)
