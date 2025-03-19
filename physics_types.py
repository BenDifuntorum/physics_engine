from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Circle:
    x: float
    y: float
    radius: float

    @property
    def top(self):
        return self.y - self.radius

    @property
    def bottom(self):
        return self.y + self.radius

    @property
    def left(self):
        return self.x - self.radius

    @property
    def right(self):
        return self.x + self.radius

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