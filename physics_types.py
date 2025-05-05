from __future__ import annotations
from abc import ABC, abstractmethod
import math
from typing import get_type_hints

class Validator:
    def __init__(self, **kwargs: object):
        self.__dict__.update(kwargs)  # Set the instance attributes dynamically
        self._validate()

    def _validate(self):
        type_hints = get_type_hints(type(self))
        for attr, expected_type in type_hints.items():
            value = getattr(self, attr)

            if expected_type is float and isinstance(value, int):
                setattr(self, attr, float(value))
                continue

            if not isinstance(value, expected_type):
                raise TypeError(f"Attribute '{attr}' must be of type {expected_type.__name__}, "
                                 f"but got {type(value).__name__}")




class AbstractPath(ABC, Validator):
    _origin: Point
    _normal: Normal

    def __contains__(self, other: Point) -> bool:
        if physics_formula.is_point_on_line(self._origin, self._origin.move_through_normal(self._normal), other):
            return True
        return False
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)) and \
        self._origin == other._origin and \
        math.isclose(self._normal.x, other._normal.x) and \
        math.isclose(self._normal.y, other._normal.y):
            return True
        return False

    @property
    def slope(self) -> float:
        x1, y1 = self._origin.p_x, self._origin.p_y
        next = self._origin.move_through_normal(self._normal)
        x2, y2 = next.p_x, next.p_y

        dy, dx = y2-y1, x2-x1
        if math.isclose(dx, 0):
            return math.inf if (dy/dx) >= 0 else -math.inf
        
        else: 
            return dy/dx
        
    @property
    @abstractmethod
    def origin(self) -> Point:
        pass
    
    @property
    @abstractmethod
    def normal(self) -> Normal:
        pass
    
    @property
    @abstractmethod
    def end(self) -> Point:
        pass
    
    @property
    @abstractmethod
    def perpendicular(self) -> AbstractPath:
        pass

    @property
    @abstractmethod
    def length(self) -> float:
        pass

    @property
    @abstractmethod
    def scalar_bounds(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def point_at_t(self, t: float) -> Point:
        pass
    
    
    
    def intersects(self, other: AbstractPath | AbstractFigure) -> AbstractPath | tuple[Point, Point] | Point | None:
        if isinstance(other, AbstractFigure):
            return self._intersects_shape(other)
        
        else:
            assert isinstance(other, AbstractPath)
            return self._intersects_line(other)
  
    
    def _intersects_line(self, other: AbstractPath) -> Point | AbstractPath | None:
        if c := physics_formula.check_collinear(self, other):
            return c

        t1, t2 = physics_formula.intersects_check(self, other)
        print(t1, t2)
        if t1 == math.inf or t2 == math.inf:
            return None

        t1_min, t1_max = self.scalar_bounds
        t2_min, t2_max = other.scalar_bounds
        
        ep = 1e-9
        if t1_min-ep <= t1 <= t1_max+ep or t2_min-ep <= t2 <= t2_max+ep:
            if isinstance(self, Line) or isinstance(self, Ray):
                l = 1
            else:
                l = self.length
            return self.point_at_t(t1*l)
        
        return None

    def _intersects_shape(self, other: AbstractFigure) -> Point | None:
        ...
        # find out which line/s and then find the intersection/s

    
    
    

class AbstractFigure(ABC, Validator):
    ...




class Movable(ABC, Validator):
    @property
    @abstractmethod
    def v_x(self) -> float:
        pass

    @property
    @abstractmethod
    def v_y(self) -> float:
        pass

    @property
    @abstractmethod
    def a_x(self) -> float:
        pass

    @property
    @abstractmethod
    def a_y(self) -> float:
        pass
    



class Tangible(ABC, Validator):
    ...




class Point(Validator):
    p_x: float | int
    p_y: float | int

    def __init__(self, p_x: float | int, p_y: float | int) -> None:
        self.p_x = p_x
        self.p_y = p_y
        super().__init__(p_x=p_x, p_y=p_y)

    def __str__(self) -> str:
        return f'{type(self).__name__} at {repr(self.p_x)}, {repr(self.p_y)}'
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}(x={self.p_x}, y={self.p_y})'
    
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
    
    def __truediv__(self, other: float) -> Point:
        new_p_x = self.p_x / other
        new_p_y = self.p_y / other
        return Point(new_p_x, new_p_y)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Point) and \
            math.isclose(self.p_x, other.p_x) and \
            math.isclose(self.p_x, other.p_y):
            return True
        else:
            return False
        
    def __neg__(self) -> Point:
        return Point(-self.p_x, -self.p_y)

    @classmethod
    def from_pair(cls, pair: tuple[float, float]) -> Point:
        return cls(pair[0], pair[1]) 
      
    def move_through_normal(self, normal: Normal, *, t: float=1) -> Point:
        new_p_x = self.p_x + (t*normal.x)
        new_p_y = self.p_y + (t*normal.y)

        return Point(new_p_x, new_p_y)
    



class Normal(Validator):
    x: float | int
    y: float | int

    def __init__(self, x: float | int, y: float | int) -> None:
        
        if x == 0 and y == 0:
            raise ValueError('Normal cannot be formed from 0 and 0')
        
        elif not math.isclose(math.hypot(x, y), 1):
            x, y = physics_formula.normal_normalize(x, y)
        
        else:
            self.x = x
            self.y = y

        super().__init__(x=x, y=y)
    @classmethod
    def from_pair(cls, l: tuple[float, float]) -> Normal:
        x, y = l
        return cls(x, y)

    def __repr__(self) -> str:
        return f'{type(self).__name__}(x={self.x}, y={self.y})'
    
    def __str__(self) -> str:
        return f'At t interval, moves line {self.x}t through x and {self.y}t through y.'

    def __abs__(self) -> Normal:
        if self.y > 0:
            return self
        else:
            return -self
    
    def __neg__(self) -> Normal:
        return Normal(-self.x, -self.y)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Normal) and math.isclose(self.x, other.x) and math.isclose(self.y, other.y):
            return True
        else: 
            return False
    
    @property
    def perpendicular(self) -> Normal:
        return Normal(-self.y, self.x)
      
    @property
    def antiperpendicular(self) -> Normal:
        """Negative of the perpendicular"""
        return Normal(self.y, -self.x)




class Particle(Point, Tangible, Movable):
    def __init__(self, p_x: float, p_y: float, *, v_x: float, v_y: float, a_x: float, a_y: float) -> None:
        super().__init__(p_x, p_y)

        self._v_x = v_x
        self._v_y = v_y
        self._a_x = a_x
        self._a_y = a_y

        super(Movable).__init__(v_x=v_x, v_y=v_y, a_x=a_x, a_y=a_y)
    @classmethod
    def init_md(cls, p_x: float, p_y: float, *, v_m: float, v_d: Normal, a_m: float, a_d: Normal) -> Particle:
        v_x, v_y = physics_formula.normal_split(v_m, v_d)
        a_x, a_y = physics_formula.normal_split(a_m, a_d)
        
        return cls(p_x, p_y, v_x=v_x, v_y=v_y, a_x=a_x, a_y=a_y)

    @property
    def v_m(self) -> float:
        return math.hypot(self._v_x, self._v_y)

    @property
    def v_d(self) -> Normal:
        return Normal(self._v_x, self._v_y)
    



class Line(AbstractPath):
    def __init__(self, origin: Point, normal: Normal) -> None:
        self._origin = origin
        if normal.y < 0:
            normal = -normal
        self._normal = normal
        mult_x = self._normal.x / abs(self._normal.x)
        mult_y = self._normal.y / abs(self._normal.y)
        self._end = Point(math.inf*mult_x, math.inf*mult_y)

        super().__init__(_origin=origin, _normal=normal)
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}(origin={repr(self._origin)}, normal={repr(self._normal)})'

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} with normal {repr(self._normal)}'
    
    @property
    def origin(self) -> Point:
        return self._origin
    
    @property
    def normal(self) -> Normal:
        return self._normal
    
    @property
    def end(self) -> Point:
        return self._end
    
    @property
    def length(self) -> float:
        return math.inf
    
    @property
    def scalar_bounds(self) -> tuple[float, float]:
        return (-math.inf, math.inf)

    @property
    def perpendicular(self) -> Line:
        '''Default perpendicular'''
        return self.perpendicular_at(self._origin)

    def perpendicular_at(self, origin: Point) -> Line:
        return Line(origin, self._normal.perpendicular)
    
    def point_at_t(self, t: float=1) -> Point:
        return self._origin.move_through_normal(self._normal, t=t)

    


class Segment(AbstractPath):
    _end: Point

    def __contains__(self, other: Point) -> bool:
        if super().__contains__(other):
            return physics_formula.contains_check(self, other)
        return False
    
    def __init__(self, origin: Point, end: Point) -> None:
        self._origin = origin
        self._end = end
        
        x1, y1 = self._origin.p_x, self._origin.p_y
        x2, y2 = self._end.p_x, self._end.p_y

        d = physics_formula.normal_normalize(x2-x1, y2-y1)
        self._normal = Normal.from_pair(d)
    
        super().__init__(_origin=origin, _end=end)

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} and ending on {repr(self._end)}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}(start={repr(self._origin)}, end={repr(self._end)})'
    
    def __eq__(self, other: object) -> bool:
        if super().__eq__(other) and self._end == self._end:
            return True
        return False

    @classmethod
    def from_pair(cls, pair: tuple[Point, Point]) -> Segment:
        return cls(pair[0], pair[1])

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def normal(self) -> Normal:
        return self._normal
    
    @property
    def length(self) -> float:
        return physics_formula.line_length(self._origin, self._end)
    
    @property
    def scalar_bounds(self) -> tuple[float, float]:
        return (0, 1)
    
    @property
    def midpoint(self) -> Point:
        mid_y = (self._end.p_y + self._origin.p_y) / 2
        mid_x = (self._end.p_x + self._origin.p_x) / 2
        return Point(mid_x, mid_y)
        
    @property
    def end(self) -> Point:
        return self._end
    
    @property
    def perpendicular(self) -> Segment:
        '''Default perpendicular.'''
        return self.perpendicular_at(self.midpoint, self.length)
    
    def perpendicular_at(self, origin: Point, length: float) -> Segment:
        if not origin:
            origin = self.midpoint
        new_normal = self.normal.perpendicular
        new_origin = origin.move_through_normal(new_normal, t=-length/2)
        new_end = origin.move_through_normal(new_normal, t=length/2)
        return Segment(new_origin, new_end)
    
    @property
    def antiperpendicular(self) -> Segment:
        '''Default antiperpendicular.'''
        return self.antiperpendicular_at(self.midpoint, self.length)
    
    def antiperpendicular_at(self, origin: Point, length: float) -> Segment:
        if not origin:
            origin = self.midpoint
        new_normal = -self.normal.perpendicular
        new_origin = origin.move_through_normal(new_normal, t=-length/2)
        new_end = origin.move_through_normal(new_normal, t=length/2)
        return Segment(new_origin, new_end)
        
    def point_at_t(self, t: float) -> Point:
        p = self._origin.move_through_normal(self._normal, t=t)

        x_min = min(self._origin.p_x, self._end.p_x)
        x_max = max(self._origin.p_x, self._end.p_x)
        y_min = min(self._origin.p_y, self._end.p_y)
        y_max = max(self._origin.p_y, self._end.p_y)

        if not (x_min <= p.p_x <= x_max and y_min <= p.p_y <= y_max):
            raise ValueError(f'No point at t={t}')
        return p
    
    


class Ray(AbstractPath):
    def __init__(self, origin: Point, normal: Normal) -> None:
        self._origin = origin
        self._normal = normal
        super().__init__(_origin=origin, _normal=normal)
        
        mult_x = self._normal.x / abs(self._normal.x)
        mult_y = self._normal.y / abs(self._normal.y)
        self._end = Point(math.inf*mult_x, math.inf*mult_y)

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} and headed to {repr(self._normal)}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}(start={repr(self._origin)}, normal={repr(self._normal)})' 

    @classmethod
    def from_points(cls, origin: Point, end: Point) -> Ray:
        x1, y1 = origin.p_x, origin.p_y
        x2, y2 = end.p_x, end.p_y
        normal = physics_formula.normal_normalize(x2-x1, y2-y1)
        return cls(origin, Normal.from_pair(normal))

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def normal(self) -> Normal:
        return self._normal
    
    @property
    def end(self) -> Point:
        return self._end
    
    @property
    def length(self) -> float:
        return math.inf
    
    @property
    def scalar_bounds(self) -> tuple[float, float]:
        return (0, math.inf)
    
    @property
    def perpendicular(self) -> Ray:
        '''Default perpendicular.'''
        return self.perpendicular_at(self._origin, 0)

    def perpendicular_at(self, origin: Point, t: float) -> Ray:
        new_normal = self.normal.perpendicular
        new_origin = origin.move_through_normal(new_normal, t=t)
        return Ray(new_origin, new_normal)
    
    @property
    def antiperpendicular(self) -> Ray:
        '''Default antiperpendicular.'''
        return self.antiperpendicular_at(self._origin, 0)
    
    def antiperpendicular_at(self, origin: Point, t: float) -> Ray:
        new_normal = -self.normal.perpendicular
        new_origin = origin.move_through_normal(new_normal, t=t)
        return Ray(new_origin, new_normal)
        
    def point_at_t(self, t: float) -> Point:
        p = self._origin.move_through_normal(self._normal, t=t)
        if t < 0:
            raise ValueError(f'No point at t={t}')
        return p
    



class Vector(AbstractPath):
    @property
    def scalar_bounds(self) -> tuple[float, float]:
        return (0, 1)




class Shape:
    ...




class Polygon(Shape):
    ...




class Circle(Shape):
    ...




class Triangle(Polygon):
    ...




class Rectangle(Polygon):
    ...




class Ball(Circle, Particle):
    ...




class Surface(Segment, Tangible):
    ...




class physics_formula:
    
    @staticmethod
    def line_slope(start: Point, end: Point):
        ...

    @staticmethod
    def normal_split(magnitude: float, normal: Normal) -> tuple[float, float]:
        m_x = magnitude * normal.x
        m_y = magnitude * normal.y
        return m_x, m_y
    
    @staticmethod
    def line_length(start: Point, end: Point) -> float:
        x1, y1 = start.p_x, start.p_y
        x2, y2 = end.p_x, end.p_y
        
        return math.hypot(y2-y1, x2-x1)
    
    @staticmethod
    def normal_normalize(x: float, y: float) -> tuple[float, float]:
        length = math.hypot(x, y)
        new_x = x/length
        new_y = y/length

        return new_x, new_y
    
    @staticmethod
    def to_rad(angle: float) -> float:
        return -math.radians(angle)
    
    @staticmethod
    def to_deg(angle: float) -> float:
        return -math.degrees(angle)
    
    @staticmethod
    def intersects_check(a: AbstractPath, b: AbstractPath) -> tuple[float, float]:
        next_point = physics_formula.check_instance_return_point(a)
        other_next_point = physics_formula.check_instance_return_point(b)
        
        x1, y1 = a.origin.p_x, a.origin.p_y
        x2, y2 = next_point.p_x, next_point.p_y

        x3, y3 = b.origin.p_x, b.origin.p_y
        x4, y4 = other_next_point.p_x, other_next_point.p_y

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        print(denom)
        if math.isclose(denom, 0):
            return math.inf, math.inf
        
        
        t1 = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        t2 = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

        return t1, t2
    
    @staticmethod
    def check_instance_return_point(a: AbstractPath) -> Point:
        if isinstance(a, Line) or isinstance(a, Ray):
            return a.origin.move_through_normal(a.normal)
        else:
            return a.end

    
    @staticmethod
    def check_collinear(a: AbstractPath, b: AbstractPath) -> AbstractPath | None:
        # print(f'{repr(abs(a.normal))}\n{repr(abs(b.normal))}')
        if abs(a.normal) != abs(b.normal):
            return None
        
        elif isinstance(a, Segment) and isinstance(b, Segment) or \
            isinstance(a, Segment) and isinstance(b, Ray) or \
            isinstance(a, Ray) and isinstance(b, Segment):
            # print('Segment | Segment or Segment | Ray')
            if out := physics_formula.compare_collinear_segments(a, b):
                return out
        
        elif isinstance(a, Segment) or isinstance(b, Segment):
            # print('Segment | Line ')
            return a if isinstance(a, Segment) else b
        
        elif isinstance(a, Ray) or isinstance(b, Ray):
            # print('Ray | Line or Ray | Ray')
            return a if isinstance(a, Ray) else b

        else:
            # print('Line | Line')
            return a
            
    @staticmethod
    def compare_collinear_segments(a: Segment | Ray, b: Segment | Ray) -> Segment | None:
        points = [a.origin, a.end, b.origin, b.end]

        dx = abs(a.end.p_x - a.origin.p_x)
        dy = abs(a.end.p_y - a.origin.p_y)

        def projection(p: Point):
            return (p.p_x - a.origin.p_x) * dx + (p.p_y - a.origin.p_y) * dy

        sorted_points = sorted(points, key=projection)
        p1, p2 = sorted_points[1:3]

        test_seg = Segment(p1, p2)
        if test_seg == a or test_seg == b:
            return test_seg

        if p1 in a and p2 in b and p1 in b and p2 in a:
            return Segment(p1, p2)
        
    @staticmethod
    def contains_check(path: AbstractPath, p: Point) -> bool:
        a = path.origin
        b = physics_formula.check_instance_return_point(path)
        
        dx = b.p_x - a.p_x
        dy = b.p_y - a.p_y

        if abs(dx) >= abs(dy):
            t = (p.p_x - a.p_x) / dx if dx else 0
        
        else:
            t = (p.p_y - a.p_y) / dy if dy else 0
        t_min, t_max = path.scalar_bounds
        
        ep = 1e-9
        return t_min - ep <= t <= t_max + ep

            
    
    @staticmethod
    def closer_to_zero(a: float, b: float) -> float:
        if abs(a) < abs(b):
            return a
        else:
            return b
        
    @staticmethod
    def farther_from_zero(a: float, b: float) -> float:
        if abs(a) > abs(b):
            return a
        else:
            return b
        
    @staticmethod
    def order_pair(a: float, b: float) -> tuple[float, float]:
        if abs(a) < abs(b):
            return a, b
        else:
            return b, a
        
    @staticmethod
    def is_point_on_line(a: Point, b: Point, p: Point, eps: float=1e-9) -> bool:
        # Vector AB
        dx1 = b.p_x - a.p_x
        dy1 = b.p_y - a.p_y
        # Vector AP
        dx2 = p.p_x - a.p_x
        dy2 = p.p_y - a.p_y

        cross = dx1 * dy2 - dy1 * dx2
        return abs(cross) < eps