
from logging import Logger
from logging import getLogger

from wx import App
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FRAME_FLOAT_ON_PARENT
from wx import Menu
from wx import MenuBar

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from codeallybasic.UnitTestBase import UnitTestBase

from tests.demo.DemoDiagramFrame import DemoDiagramFrame
from tests.demo.DiagramGenerator import DiagramGenerator
from tests.demo.OrthogonalPathFinderAdapter import OrthogonalPathFinderAdapter

FRAME_WIDTH:  int = 1280
FRAME_HEIGHT: int = 800


class DemoOrthogonalRouting(App):

    def __init__(self):

        UnitTestBase.setUpLogging()

        super().__init__(redirect=False)

        self.logger: Logger = getLogger(__name__)

    # noinspection PyAttributeOutsideInit
    def OnInit(self):

        self._topLevelFrame: SizedFrame = SizedFrame(parent=None, title="Demo Orthogonal Routing",
                                                     size=(FRAME_WIDTH, FRAME_HEIGHT),
                                                     style=DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT)
        self._topLevelFrame.CreateStatusBar()  # should always do this when there's a resize border

        sizedPanel: SizedPanel = self._topLevelFrame.GetContentsPane()

        self._diagramFrame: DemoDiagramFrame = DemoDiagramFrame(parent=sizedPanel)

        # noinspection PyUnresolvedReferences
        self._diagramFrame.SetSizerProps(expand=True, proportion=1)

        self._defaultDemoId: int = wxNewIdRef()

        self._createApplicationMenuBar()

        self.SetTopWindow(self._topLevelFrame)

        self._topLevelFrame.SetAutoLayout(True)
        self._topLevelFrame.Show(True)

        self._diagramGenerator: DiagramGenerator = DiagramGenerator()

        self._diagramFrame.diagramGenerator = self._diagramGenerator

        return True

    def _createApplicationMenuBar(self):
        menuBar:     MenuBar = MenuBar()

        fileMenu:    Menu    = Menu()

        fileMenu.Append(id=self._defaultDemoId, item='Default Demo\tCtrl-D', helpString='Run default demo')

        menuBar.Append(fileMenu, 'File')

        self._topLevelFrame.SetMenuBar(menuBar)

        self._topLevelFrame.Bind(EVT_MENU, self._onDefaultDemo, id=self._defaultDemoId)

    # noinspection PyUnusedLocal
    def _onDefaultDemo(self, event: CommandEvent):

        adapter: OrthogonalPathFinderAdapter = OrthogonalPathFinderAdapter(self._diagramGenerator)
        adapter.runDefaultDemo()


if __name__ == '__main__':
    testApp: DemoOrthogonalRouting = DemoOrthogonalRouting()
    testApp.MainLoop()
