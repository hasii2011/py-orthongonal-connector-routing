from logging import Logger
from logging import getLogger


class Nodes(list):

    def __init__(self, iterable):
        super().__init__(iterable)

        self.logger: Logger = getLogger(__name__)

    def addRange(self, nodes: 'Nodes'):
        """
        Emulate C#s method
        Args:
            nodes:
        """
        self.extend(nodes)


def nodesFactory() -> Nodes:
    return Nodes([])
