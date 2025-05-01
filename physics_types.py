from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Circle:
    p_x: float
    p_y: float
    r: float

    @property
    def top(self):
        return self.p_y - self.r

    @property
    def bottom(self):
        return self.p_y + self.r

    @property
    def left(self):
        return self.p_x - self.r

    @property
    def right(self):
        return self.p_x + self.r

@dataclass
class Ball(Circle):
    v_x: float
    v_y: float
    a_x: float
    a_y: float


class Surface(Enum):
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()