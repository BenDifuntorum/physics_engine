import math
from .point import Point
from .vect import Vect

class Line:
    def __init__(self, origin: Point, slope: Vect) -> None:
        self._slope = slope.normal
        self._y_intercept = origin.y - (origin.x * self.slope.y/self.slope.x)

    def __hash__(self) -> int:
        return hash((self._y_intercept, self._slope))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Line):
            return False
        
        if self._slope == other.slope and self._y_intercept == other.y_intercept:
            return True
        
        return False
    
    @property
    def length(self):
        return math.inf

    @property
    def slope(self):
        return self._slope
    
    @property
    def y_intercept(self):
        return self._y_intercept
    
    

    
    
    
