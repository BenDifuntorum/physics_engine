from __future__ import annotations
from abc import abstractmethod
import math

class Point:
    def __init__(self, p_x: float, p_y: float) -> None:
        self.p_x = p_x
        self.p_y = p_y

    def __str__(self) -> str:
        return f'{type(self).__name__} at {self.p_x}, {self.p_y}'
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}:{{x:{self.p_x}, y:{self.p_y}}}'
    

class Particle(Point):
    def __init__(self, p_x: float, p_y: float, *, v_x: float, v_y: float, a_x: float, a_y: float) -> None:
        super().__init__(p_x, p_y)
        self._v_x = v_x
        self._v_y = v_y
        self._a_x = a_x
        self._a_y = a_y

    @classmethod
    def md(cls, p_x: float, p_y: float, *, v_m: float, v_d: float, a_m: float, a_d: float) -> Particle
        v_x, v_y = physics_formula.vect_split(v_m, v_d)
        a_x, a_y = physics_formula.vect_split(a_m, a_d)
        
        cls.__init__(p_x, p_y, v_x=v_x, v_y=v_y, a_x=a_x, a_y=a_y)


class Line:
    def __init__(self, *, start: Point, end: Point) -> None:
        self.start = start
        self.end = end
    ...
class Shape:
    ...
class Polygon(Shape):
    ...
class Circle(Shape):
    ...
class Rectangle(Shape):
    ...
class Ray(Line):
    ...
class Segment(Line):
    ...
class Vect(Ray):
    ...
class Angle:
    ...


class physics_formula:
    
    @staticmethod
    def line_slope(start: Point, end: Point):
        ...

    @staticmethod
    def vect_split(magnitude: float, direction: float) -> tuple[float, float]:
        m_x = magnitude * math.cos(math.radians(direction))
        m_y = magnitude * -math.sin(math.radians(direction))
        return m_x, m_y