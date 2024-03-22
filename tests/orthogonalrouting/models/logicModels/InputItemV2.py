
from dataclasses import dataclass

from orthogonalrouting.Common import HEIGHT_SENTINEL
from orthogonalrouting.Common import NOT_SET_SENTINEL
from orthogonalrouting.Common import WIDTH_SENTINEL
from orthogonalrouting.Common import X_SENTINEL
from orthogonalrouting.Common import Y_SENTINEL
from orthogonalrouting.models.IInput import IInput


@dataclass
class InputItemV2(IInput):

    x: int = X_SENTINEL
    y: int = Y_SENTINEL

    width:  int = WIDTH_SENTINEL
    height: int = HEIGHT_SENTINEL

    right: int  = NOT_SET_SENTINEL
    bottom: int = NOT_SET_SENTINEL
