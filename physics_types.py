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
    _vect: Vect

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)) and \
        self._origin == other._origin and \
        math.isclose(self._vect.x, other._vect.x) and \
        math.isclose(self._vect.y, other._vect.y):
            return True
        return False

    @property
    def slope(self) -> float:
        x1, y1 = self._origin.p_x, self._origin.p_y
        next = self._origin.move_through_vect(self._vect)
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
    def vect(self) -> Vect:
        return self._vect
    
    @abstractmethod
    def perpendicular(self) -> AbstractPath:
        pass

    @property
    @abstractmethod
    def length(self) -> float:
        pass

    @abstractmethod
    def point_at_t(self, t: float) -> Point:
        pass
    
    def _det_path(self) -> tuple[float, float]:
        match type(self).__name__:
            case 'Line':
                return (-math.inf, math.inf)
            case 'Segment':
                return (-1, 1)
            case 'Ray':
                return (-math.inf, 1)
            case _:
                return (0, 0)
    
    def intersects(self, other: AbstractPath | AbstractFigure) -> AbstractPath | tuple[Point, Point] | Point | None:
        if isinstance(other, AbstractFigure):
            return self._intersects_shape(other)
        
        else:
            assert isinstance(other, AbstractPath)
            return self._intersects_line(other)
        
    
    
                

    
    def _intersects_line(self, other: AbstractPath) -> Point | AbstractPath | None:
        if c := physics_formula.check_collinear(self, other):
            return c
        
        
        next_point = self._origin.move_through_vect(self._vect)
        x1, y1 = self._origin.p_x, self._origin.p_y
        x2, y2 = next_point.p_x, next_point.p_y

        t1, t2 = self._intersects_helper(other)
        ep = 1e-9
        if t1 == math.inf or t2 == math.inf:
            return None
        
        t1_min, t1_max = self._det_path()
        
        if t1_min-ep <= t1 <= t1_max+ep or t1_min-ep <= t2 <= t1_max+ep:
            x_int = x1 + t1 * (x2 - x1)
            y_int = y1 + t1 * (y2 - y1)
            return Point(x_int, y_int)
        
        return None

    def _intersects_shape(self, other: AbstractFigure) -> Point | None:
        ...
        # find out which line/s and then find the intersection/s

    def _intersects_helper(self, other: AbstractPath) -> tuple[float, float]:
        next_point = self._origin.move_through_vect(self._vect)
        x1, y1 = self._origin.p_x, self._origin.p_y
        x2, y2 = next_point.p_x, next_point.p_y

        other_next_point = other._origin.move_through_vect(other._vect)
        x3, y3 = other._origin.p_x, other._origin.p_y
        x4, y4 = other_next_point.p_x, other_next_point.p_y

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if math.isclose(denom, 0):
            return math.inf, math.inf
        
        
        t1 = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        t2 = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

        return t1, t2
    
    


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
        
    def move_through_vect(self, vect: Vect, *, t: float=1) -> Point:
        new_p_x = self.p_x + (t*vect.x)
        new_p_y = self.p_y + (t*vect.y)

        return Point(new_p_x, new_p_y)
    



class Vect(Validator):
    x: float | int
    y: float | int

    def __init__(self, x: float | int, y: float | int) -> None:
        
        if x == 0 and y == 0:
            raise ValueError('Vect cannot be formed from 0 and 0')
        
        elif not math.isclose(math.hypot(x, y), 1):
            x, y = physics_formula.vect_normal(x, y)
        
        else:
            self.x = x
            self.y = y

        super().__init__(x=x, y=y)
    @classmethod
    def from_pair(cls, l: tuple[float, float]) -> Vect:
        x, y = l
        return cls(x, y)

    def __repr__(self) -> str:
        return f'{type(self).__name__}(x={self.x}, y={self.y})'
    
    def __str__(self) -> str:
        return f'At t interval, moves line {self.x}t through x and {self.y}t through y.'

    def __abs__(self) -> Vect:
        return Vect(self.x, abs(self.y))
    
    def __neg__(self) -> Vect:
        return Vect(-self.x, -self.y)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vect) and math.isclose(self.x, other.x) and math.isclose(self.y, other.y):
            return True
        else: 
            return False
    
    @property
    def perpendicular(self) -> Vect:
        return Vect(-self.y, self.x)
      
    @property
    def antiperpendicular(self) -> Vect:
        """Negative of the perpendicular"""
        return Vect(self.y, -self.x)




class Particle(Point, Tangible, Movable):
    def __init__(self, p_x: float, p_y: float, *, v_x: float, v_y: float, a_x: float, a_y: float) -> None:
        super().__init__(p_x, p_y)

        self._v_x = v_x
        self._v_y = v_y
        self._a_x = a_x
        self._a_y = a_y

        super(Movable).__init__(v_x=v_x, v_y=v_y, a_x=a_x, a_y=a_y)
    @classmethod
    def init_md(cls, p_x: float, p_y: float, *, v_m: float, v_d: Vect, a_m: float, a_d: Vect) -> Particle:
        v_x, v_y = physics_formula.vect_split(v_m, v_d)
        a_x, a_y = physics_formula.vect_split(a_m, a_d)
        
        return cls(p_x, p_y, v_x=v_x, v_y=v_y, a_x=a_x, a_y=a_y)

    @property
    def v_m(self) -> float:
        return math.hypot(self._v_x, self._v_y)

    @property
    def v_d(self) -> Vect:
        return Vect(self._v_x, self._v_y)
    



class Line(AbstractPath):
    def __init__(self, origin: Point, vect: Vect) -> None:
        self._origin = origin
        if vect.x < 0 and vect.y < 0:
            vect = -vect
        self._vect = vect
        self._end = Point(math.inf, math.inf)

        super().__init__(_origin=origin, _vect=vect)
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}(origin={repr(self._origin)}, vect={repr(self._vect)})'

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} with vect {repr(self._vect)}'
   
    @property
    def origin(self) -> Point:
        return self._origin
    
    @property
    def vect(self) -> Vect:
        return self._vect
    
    @property
    def length(self) -> float:
        return math.inf

    def perpendicular(self, origin: Point | None = None) -> Line:
        if not origin:
            origin = self._origin
        return Line(origin, self._vect.perpendicular)
    
    def point_at_t(self, t: float=1) -> Point:
        return self._origin.move_through_vect(self._vect, t=t)



class Segment(AbstractPath):
    _end: Point

    def __init__(self, origin: Point, end: Point) -> None:
        self._origin = origin
        self._end = end

        
        x1, y1 = self._origin.p_x, self._origin.p_y
        x2, y2 = self._end.p_x, self._end.p_y
        d = physics_formula.vect_normal(x2-x1, y2-y1)
        self._vect = Vect.from_pair(d)
    
        super().__init__(_origin=origin, _end=end)

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} and ending on {repr(self._end)}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}(start={repr(self._origin)}, end={repr(self._end)})'
    
    def __eq__(self, other: object) -> bool:
        if super().__eq__(other) and self._end == self._end:
            return True
        return False

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def vect(self) -> Vect:
        return self._vect
    
    @property
    def length(self) -> float:
        return physics_formula.line_length(self._origin, self._end)
    
    @property
    def midpoint(self) -> Point:
        mid_y = (self._end.p_y + self._origin.p_y) / 2
        mid_x = (self._end.p_x + self._origin.p_x) / 2
        return Point(mid_x, mid_y)
        
    @property
    def end(self) -> Point:
        return self._end
    
    def perpendicular(self, origin: Point | None = None) -> Segment:
        '''Default perpendicular.'''
        if not origin:
            origin = self.midpoint
        new_vect = self.vect.perpendicular
        origin = origin.move_through_vect(new_vect, t=-self.length/2)
        end = origin.move_through_vect(new_vect, t=self.length/2)
        return Segment(origin, end)
    
    def antiperpendicular(self, origin: Point | None = None) -> Segment:
        '''Default antiperpendicular.'''
        if not origin:
            origin = self.midpoint
        new_vect = -self.vect.perpendicular
        start = origin.move_through_vect(new_vect, t=-self.length/2)
        end = origin.move_through_vect(new_vect, t=self.length/2)
        return Segment(start, end)
        
    def point_at_t(self, t: float) -> Point:
        p = self._origin.move_through_vect(self._vect, t=t)

        x_min = min(self._origin.p_x, self._end.p_x)
        x_max = max(self._origin.p_x, self._end.p_x)
        y_min = min(self._origin.p_y, self._end.p_y)
        y_max = max(self._origin.p_y, self._end.p_y)

        if not (x_min <= p.p_x <= x_max and y_min <= p.p_y <= y_max):
            raise ValueError(f'No point at t={t}')
        return p
    



class Ray(AbstractPath):
    def __init__(self, origin: Point, vect: Vect) -> None:
        self._origin = origin
        self._vect = vect
        super().__init__(_origin=origin, _vect=vect)

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} and headed to {repr(self._vect)}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}(start={repr(self._origin)}, vect={repr(self._vect)})' 

    @classmethod
    def from_points(cls, origin: Point, end: Point) -> Ray:
        x1, y1 = origin.p_x, origin.p_y
        x2, y2 = end.p_x, end.p_y
        vect = physics_formula.vect_normal(x2-x1, y2-y1)
        return cls(origin, Vect.from_pair(vect))

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def vect(self) -> Vect:
        return self._vect
    
    @property
    def length(self) -> float:
        return math.inf
    
    def perpendicular(self, origin: Point | None = None, t: float = 0) -> Ray:
        '''Default perpendicular.'''
        if not origin:
            origin = self._origin
        new_vect = self.vect.perpendicular
        new_origin = origin.move_through_vect(new_vect, t=t)
        return Ray(new_origin, new_vect)
    
    def antiperpendicular(self, origin: Point | None = None, t: float = 0) -> Ray:
        '''Default antiperpendicular.'''
        if not origin:
            origin = self._origin
        new_vect = -self.vect.perpendicular
        new_origin = origin.move_through_vect(new_vect, t=t)
        return Ray(new_origin, new_vect)
        
    def point_at_t(self, t: float) -> Point:
        p = self._origin.move_through_vect(self._vect, t=t)
        if t < 0:
            raise ValueError(f'No point at t={t}')
        return p


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




class surface(Segment, Particle):
    ...




class physics_formula:
    
    @staticmethod
    def line_slope(start: Point, end: Point):
        ...

    @staticmethod
    def vect_split(magnitude: float, vect: Vect) -> tuple[float, float]:
        m_x = magnitude * vect.x
        m_y = magnitude * vect.y
        return m_x, m_y
    
    @staticmethod
    def line_length(start: Point, end: Point) -> float:
        x1, y1 = start.p_x, start.p_y
        x2, y2 = end.p_x, end.p_y
        
        return math.hypot(y2-y1, x2-x1)
    
    @staticmethod
    def vect_normal(x: float, y: float) -> tuple[float, float]:
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
    def check_collinear(a: AbstractPath, b: AbstractPath) -> AbstractPath | None:
        if a.vect != b.vect:
            return 
        
        if a.origin.p_x 
            if isinstance(a, Segment) and isinstance(b, Segment):
                a, b = physics_formula.compare_collinear_segments(a, b)
                return Segment()

            
            elif isinstance(a, Segment) or isinstance(b, Segment):
                return a if isinstance(a, Segment) else b
            
            elif isinstance(a, Ray) or isinstance(b, Ray):
                return a if isinstance(a, Ray) else b

            else:
                return a
            
    @staticmethod
    def compare_collinear_segments(a: Segment, b: Segment) -> tuple[point, point]:
        x1, y1 = a.origin.p_x, a.origin.p_y
        x2, y2 = a.end.p_x, a.end.p_y
        x3, y3 = b.origin.p_x, b.origin.p_y
        x4, y4 = b.end.p_x, b.end.p_y

        new_origin_x = 

        return 
    
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