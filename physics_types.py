from __future__ import annotations
from typing import Self
import math


class Normal:
    def __init__(self, x: float, y: float) -> None:
        if not math.isclose(math.hypot(x, y), 1):
            self = physics_formula.vect_normal(x, y)

        else:
            self.x = x
            self.y = y

    def __repr__(self) -> str:
        return f'{type(self).__name__}(x={self.x}, y={self.y})'
    
    def __str__(self) -> str:
        return f'At t interval, moves line {self.x}t through x and {self.y}t through y.'

    def __abs__(self) -> Normal:
        return Normal(self.x, abs(self.y))
    
    def __neg__(self) -> Normal:
        return Normal(-self.x, -self.y)
    
    @property
    def perpend(self) -> Normal:
        return Normal(self.y, -self.x)
    
    
            
    
class Point:
    def __init__(self, p_x: float, p_y: float) -> None:
        self.p_x = p_x
        self.p_y = p_y

    def __str__(self) -> str:
        return f'{type(self).__name__} at {repr(self.p_x)}, {repr(self.p_y)}'
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}(x={self.p_x}, y{self.p_y})'
    
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
        
    def __neg__(self) -> Point:
        return Point(-self.p_x, -self.p_y)
        
    def move_through_normal(self, normal: Normal, *, t: float=1) -> Point:
        new_p_x = self.p_x + (t*normal.x)
        new_p_y = self.p_y + (t*normal.y)

        return Point(new_p_x, new_p_y)



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
        
        return cls(p_x, p_y, v_x=v_x, v_y=v_y, a_x=a_x, a_y=a_y)

    @property
    def v_m(self) -> float:
        return math.hypot(self._v_x, self._v_y)

    @property
    def v_d(self) -> Normal:
        return Normal(self._v_x, self._v_y)
    

class Line:
    def __init__(self, o: Point, d: Normal) -> None:
        self.origin = o
        self.direction = d

    def __repr__(self) -> str:
        return f'{type(self).__name__}(origin={repr(self.origin)}, direction={repr(self.direction)})'

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self.origin)} with normal vector {repr(self.direction)}'

    @classmethod
    def from_points(cls, *, start: Point, end: Point) -> Self:
        x1, y1 = start.p_x, start.p_y
        x2, y2 = end.p_x, end.p_y

        d = physics_formula.vect_normal(y2-y1, x2-x1)
        
        return cls(start, d)


    @property
    def slope(self):
        x1, y1 = self.origin.p_x, self.origin.p_y
        next = self.origin.move_through_normal(self.direction)
        x2, y2 = next.p_x, next.p_y

        m = (y2-y1) / (x2-x1)
        if math.isclose(x2-x1, 0):
            return math.inf if m >= 0 else -math.inf
        
        else: 
            return m

    @property
    def perpendicular(self, point: Point | None = None) -> Line:
        if not point:
            point = self.origin
        return Line(point, self.direction.perpend)


    def point_at_t(self, t: float) -> Point:
        return self.origin.move_through_normal(self.direction, t=t)


class Segment(Line):
    def __new__(cls, start: Point, end: Point) -> Self:
        dx, dy = end.p_x - start.p_x, end.p_y - start.p_y
        d = physics_formula.vect_normal(dy, dx)
        return cls.__from_line_args(start, d)

    @classmethod
    def from_vector(cls, *, o: Point, d: Normal) -> Self:
        return cls.__from_line_args(o, d)

    @classmethod
    def __from_line_args(cls, o: Point, d: Normal) -> Self:
        obj = cls.__new__(cls)
        Line.__init__(obj, o, d)
        return obj


    @property
    def midpoint(self):
        ...

class Ray(Line):
    ...

class Vect(Ray):
    ...

class Angle:
    ...        


class Shape:
    ...
class Polygon(Shape):
    ...
class Circle(Shape):
    ...
class Rectangle(Shape):
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
    def line_length(start: Point, end: Point) -> float:
        x1, y1 = start.p_x, start.p_y
        x2, y2 = end.p_x, end.p_y
        
        return math.hypot(y2-y1, x2-x1)
    
    @staticmethod
    def vect_normal(x: float, y: float) -> Normal:
        length = math.hypot(x, y)
        new_x = x/length
        new_y = y/length

        return Normal(new_x, new_y)
    
    @staticmethod
    def to_rad(angle: float) -> float:
        return -math.radians(angle)
    
    @staticmethod
    def to_deg(angle: float) -> float:
        return -math.degrees(angle)