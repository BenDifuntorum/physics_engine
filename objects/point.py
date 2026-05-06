from __future__ import annotations
from dataclasses import dataclass
import math

from .vect import Vect


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __repr__(self) -> str:
        return f'Point(x={self.x}, y={self.y})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return False
        
        if (math.isclose(self.x, other.x) and math.isclose(self.y, other.y)):
            return True
        
        return False
    
    def __hash__(self) -> int:
        return hash(("Point", self.x, self.y))
    
    def __add__(self, other: object) -> Point:
        if not isinstance(other, Vect):
            raise ValueError("Can only add Point and Vect")
        
        return Point(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other: object) -> Vect:
        if not isinstance(other, Point):
            raise ValueError("Can only subtract Point and Point")
        
        return Vect(self.x-other.x, self.y-other.y)
    
    def __mul__(self, scalar: float) -> Point:
        return Point(self.x*scalar, self.y*scalar)
    
    def __rmul__(self, scalar: float) -> Point:
        return self * scalar
    
    def __truediv__(self, scalar: float) -> Point:
        if scalar == 0:
            raise ZeroDivisionError('Point object cannot be divided by zero')
        return Point(self.x/scalar, self.y/scalar)
    
    def __floordiv__(self, scalar: float) -> Point:
        if scalar == 0:
            raise ZeroDivisionError('Point object cannot be divided by zero')
        return Point(self.x//scalar, self.y//scalar)
    
    