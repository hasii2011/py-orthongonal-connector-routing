
from logging import Logger
from logging import getLogger

from orthogonalrouting.algorithm.OrthogonalPathFinder import OrthogonalPathFinder
from orthogonalrouting.enumerations.ConnectorOrientation import ConnectorOrientation
from orthogonalrouting.enumerations.SearchAlgorithm import SearchAlgorithm
from orthogonalrouting.models.AlgorithmResults import AlgorithmResults
from orthogonalrouting.models.logicModels.Connector import Connector
from tests.demo.DemoItem import DemoItems
from tests.demo.DiagramGenerator import DiagramGenerator


class OrthogonalPathFinderAdapter:
    def __init__(self, diagramGenerator: DiagramGenerator):

        self.logger: Logger = getLogger(__name__)

        self._diagramGenerator:     DiagramGenerator     = diagramGenerator
        self._orthogonalPathFinder: OrthogonalPathFinder = OrthogonalPathFinder()

    def runDefaultDemo(self):

        self._diagramGenerator.generateDefaultItems()

        demoItems: DemoItems = self._diagramGenerator.demoItems

        connector: Connector = Connector()
        connector.source                 = demoItems[0]
        connector.sourceOrientation      = ConnectorOrientation.LEFT
        connector.destination            = demoItems[3]
        connector.destinationOrientation = ConnectorOrientation.RIGHT

        results: AlgorithmResults = self._orthogonalPathFinder.orthogonalPath(items=demoItems,
                                                                              maxWidth=800, maxHeight=450,
                                                                              searchAlgorithm=SearchAlgorithm.Dijkstra, targetConnector=connector)

        self.logger.info(f'{results.connections=}')
        self.logger.info(f'{results.intersections=}')

        self._drawPath(connector)

    def _drawPath(self, connector):
        pass
