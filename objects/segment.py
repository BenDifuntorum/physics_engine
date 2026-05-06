from __future__ import annotations
import math

from .point import Point

class Segment:
    def __init__(self, origin: Point, end: Point) -> None:
        self._origin = origin
        self._end = end

    def __hash__(self) -> int:
        return hash((self._origin, self._end))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Segment):
            return False
        
        if self.origin == other.origin and self.end == other.end:
            return True
        
        return False

    @property
    def slope(self):
        direction_vector = (self.end - self.origin).normal
        if direction_vector.x == 0:
            if direction_vector.y >= 0:
                return math.inf
            
            return -math.inf

        return math.hypot(direction_vector.y/direction_vector.x)
    
    @property
    def origin(self):
        return self._origin
    
    @property
    def end(self):
        return self._end