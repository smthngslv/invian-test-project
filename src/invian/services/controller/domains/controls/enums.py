from enum import Enum

__all__ = ("ControlStatus",)


class ControlStatus(str, Enum):
    UP = "up"
    DOWN = "down"
