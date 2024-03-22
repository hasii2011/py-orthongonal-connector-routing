from typing import cast

X_SENTINEL: int = -666
Y_SENTINEL: int = -666

WIDTH_SENTINEL:  int = -777
HEIGHT_SENTINEL: int = -777

NOT_SET_SENTINEL: int = 0xDEADBEEF

NOT_SET_BOOLEAN: bool = cast(bool, None)
NOT_SET_INT:     int  = cast(int, None)
