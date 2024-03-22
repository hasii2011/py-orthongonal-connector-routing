
from logging import Logger
from logging import getLogger

from wx import App

from codeallybasic.UnitTestBase import UnitTestBase
from wx import DEFAULT_FRAME_STYLE
from wx import FRAME_FLOAT_ON_PARENT
from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from tests.demo.DemoDiagramFrame import DemoDiagramFrame

FRAME_WIDTH:  int = 1280
FRAME_HEIGHT: int = 800


class DemoPriorityQueueApp(App):

    def __init__(self):

        UnitTestBase.setUpLogging()

        super().__init__(redirect=False)

        self.logger: Logger = getLogger(__name__)

    # noinspection PyAttributeOutsideInit
    def OnInit(self):

        self._topLevelFrame: SizedFrame = SizedFrame(parent=None, title="Demo Priority Queue",
                                                     size=(FRAME_WIDTH, FRAME_HEIGHT),
                                                     style=DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT)
        self._topLevelFrame.CreateStatusBar()  # should always do this when there's a resize border

        sizedPanel: SizedPanel = self._topLevelFrame.GetContentsPane()

        self._diagramFrame: DemoDiagramFrame = DemoDiagramFrame(parent=sizedPanel)

        # noinspection PyUnresolvedReferences
        self._diagramFrame.SetSizerProps(expand=True, proportion=1)

        self.SetTopWindow(self._topLevelFrame)

        self._topLevelFrame.SetAutoLayout(True)
        self._topLevelFrame.Show(True)

        return True


if __name__ == '__main__':
    testApp: DemoPriorityQueueApp = DemoPriorityQueueApp()
    testApp.MainLoop()
