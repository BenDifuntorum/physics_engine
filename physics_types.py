from __future__ import annotations
from abc import abstractmethod
import math

class Normal:
    def __init__(self, x: float, y: float) -> None:
        if not math.isclose(physics_formula.vect_length((x, y)), 1):
            self.x, self.y = physics_formula.vect_normal((x, y))

        else:
            self.x = x
            self.y = y
            

class Point:
    def __init__(self, p_x: float, p_y: float) -> None:
        self.p_x = p_x
        self.p_y = p_y

    def __str__(self) -> str:
        return f'{type(self).__name__} at {self.p_x}, {self.p_y}'
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}:{{x:{self.p_x}, y:{self.p_y}}}'
    
    def __add__(self, other: Point) -> Point:
        new_p_x = self.p_x + other.p_x
        new_p_y = self.p_y + other.p_y
        return Point(new_p_x, new_p_y)
    
    def __sub__(self, other: Point) -> Point:
        new_p_x = self.p_x - other.p_x
        new_p_y = self.p_y - other.p_y
        return Point(new_p_x, new_p_y)
    
    def __mul__(self, other: float) -> Point:
        new_p_x = self.p_x * other
        new_p_y = self.p_y * other
        return Point(new_p_x, new_p_y)
    
    def __div__(self, other: float) -> Point:
        new_p_x = self.p_x / other
        new_p_y = self.p_y / other
        return Point(new_p_x, new_p_y)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point) and self.p_x == other.p_x and self.p_y == other.p_y:
            return True
        else:
            return False


class Particle(Point):
    def __init__(self, p_x: float, p_y: float, *, v_x: float, v_y: float, a_x: float, a_y: float) -> None:
        super().__init__(p_x, p_y)
        self._v_x = v_x
        self._v_y = v_y
        self._a_x = a_x
        self._a_y = a_y

    @classmethod
    def init_md(cls, p_x: float, p_y: float, *, v_m: float, v_d: Normal, a_m: float, a_d: Normal) -> Particle:
        v_x, v_y = physics_formula.vect_split(v_m, v_d)
        a_x, a_y = physics_formula.vect_split(a_m, a_d)
        
        return Particle(p_x, p_y, v_x=v_x, v_y=v_y, a_x=a_x, a_y=a_y)

    @property
    def v_m(self) -> float:
        return math.sqrt(self._v_x**2 + self._v_y**2)

    @property
    def v_d(self) -> Normal:
        return Normal(self._v_x, self._v_y)
    

class Line:
    def __init__(self, *, o: Point, d: Normal) -> None:
        self.origin = o
        self.direction = d

    def __repr__(self) -> str:
        return f'{type(self).__name__}{{origin={self.origin}, direction={self.direction}}}'

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {self.origin} with unit vector {self.direction}'

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

class Ball(Circle, Particle):
    ...

class physics_formula:
    
    @staticmethod
    def line_slope(start: Point, end: Point):
        ...

    @staticmethod
    def vect_split(magnitude: float, normal: Normal) -> tuple[float, float]:
        m_x = magnitude * normal.x
        m_y = magnitude * normal.y
        return m_x, m_y
    
    @staticmethod
    def vect_length(base: tuple[float, float]) -> float:
        return math.sqrt(base[0]**2 + base[1]**2)
    
    @staticmethod
    def vect_normal(base: tuple[float, float]) -> tuple[float, float]:
        length = physics_formula.vect_length(base)
        x = base[0]/length
        y = base[1]/length

        return x, y
    
    @staticmethod
    def to_rad(angle: float) -> float:
        return -math.radians(angle)
    
    @staticmethod
    def to_deg(angle: float) -> float:
        return -math.degrees(angle)