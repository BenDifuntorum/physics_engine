from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Vect:
    x: float
    y: float

    def __post_init__(self):
        if self.x == 0 and self.y == 0:
            raise ValueError('Zero Vectors are not allowed.')

    def __hash__(self) -> int:
        return hash(("Vect", self.x, self.y))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vect):
            return False
        
        if math.isclose(self.x, other.x) and math.isclose(self.y, other.y):
            return True
        
        return False
    
    def __add__(self, other: object) -> Vect:
        if not isinstance(other, Vect):
            raise ValueError('Vect can only be added to Vect')
        
        return Vect(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other: object):
        if not isinstance(other, Vect):
            raise ValueError('Vect can only be subtracted from Vect')
        
        return Vect(self.x-other.x, self.y-other.y) 
    
    def __mul__(self, scalar: float) -> Vect:
        return Vect(self.x*scalar, self.y*scalar)
    
    def __rmul__(self, scalar: float) -> Vect:
        return self * scalar
    
    def __truediv__(self, scalar: float) -> Vect:
        if scalar == 0:
            raise ZeroDivisionError('Vect object cannot be divided by zero')
        return Vect(self.x/scalar, self.y/scalar)
    
    def __floordiv__(self, scalar: float) -> Vect:
        if scalar == 0:
            raise ZeroDivisionError('Vect object cannot be divided by zero')
        return Vect(self.x//scalar, self.y//scalar)
    
    @property
    def magnitude(self):
        return math.hypot(self.x, self.y)

    @property
    def normal(self) -> Vect:
        return Vect(self.x/self.magnitude, self.y/self.magnitude)        
    
