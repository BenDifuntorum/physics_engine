from __future__ import annotations
from abc import ABC, abstractmethod
from types import GenericAlias, UnionType
from typing import get_type_hints, Sequence, get_origin
import math


class Validator:
    '''Validates inputs'''
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
            
            if generic_type := get_origin(expected_type):
                if type(expected_type) == GenericAlias:
                    expected_type = generic_type

                elif type(expected_type) == UnionType:
                    expected_type = generic_type

            if not isinstance(value, expected_type):
                print(attr, expected_type.__name__, type(value).__name__)
                raise TypeError(f"Attribute {attr} must be of type {expected_type.__name__}, "
                                 f"but got {type(value).__name__}")




class AbstractObject(ABC, Validator):
    def __repr__(self) -> str:
        cls = self.__class__
        values: list[str] = []
        
        for attr, value in self.__dict__.items():
            values.append(f'{attr.strip('_')}={value!r}')
        
        return f"{cls.__name__}({', '.join(values)})"
    
    def intersects(self, other: AbstractPath | AbstractFigure) -> AbstractPath | tuple[Point | AbstractPath, ...] | Point | None:
        return physics_formula.find_intersection(self, other)




class AbstractPath(AbstractObject):
    _origin: Point
    _normal: Normal
    _end: Point

    def __contains__(self, other: Point) -> bool:
        if physics_formula.contains_check(other, self):
            return True
        return False
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self._origin == other._origin and self._normal == other._normal
        return False
    
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
    @abstractmethod
    def perpendicular(self) -> AbstractPath:
        pass

    @property
    def slope(self) -> float:
        return physics_formula.line_slope(self)
        
    @property
    @abstractmethod
    def length(self) -> float:
        pass

    @property
    @abstractmethod
    def scalar_bounds(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def point_at_t(self, t: float) -> Point | None:
        pass

    


class AbstractFinitePath(AbstractPath):
    @property
    def scalar_bounds(self) -> tuple[float, float]:
        return (0, 1)

    @classmethod
    @abstractmethod
    def from_pair(cls, pair: tuple[Point, Point]) -> AbstractFinitePath:
        pass

    @property
    def length(self) -> float:
        return physics_formula.line_length(self._origin, self._end)
    
    def point_at_t(self, t: float) -> Point | None:
        p = self._origin.move_through_normal(self._normal, t=t*self.length)

        x_min = min(self._origin.p_x, self._end.p_x)
        x_max = max(self._origin.p_x, self._end.p_x)
        y_min = min(self._origin.p_y, self._end.p_y)
        y_max = max(self._origin.p_y, self._end.p_y)

        if not (x_min <= p.p_x <= x_max and y_min <= p.p_y <= y_max):
            return
        return p



class AbstractDirection(AbstractObject):
    def __add__(self, other: AbstractDirection) -> Vect: 
        return Vect.normdef(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: AbstractDirection) -> Vect:
        return Vect.normdef(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> Vect:
        return Vect.normdef(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: float) -> Vect:
        return Vect.normdef(self.x / scalar, self.y / scalar)
    
    def __str__(self) -> str:
        return f'At t interval, moves line {self.x}t through x and {self.y}t through y.'
    
    @property
    @abstractmethod
    def magnitude(self) -> float:
        pass

    @property
    @abstractmethod
    def normal(self) -> Normal:
        pass

    @property
    @abstractmethod
    def x(self) -> float:
        pass
    
    @property
    @abstractmethod
    def y(self) -> float:
        pass
    
    def dot(self, other: AbstractDirection) -> float:
        return physics_formula.dot_product(self.x, self.y, other.x, other.y)
    
    def cross(self, other: AbstractDirection) -> float:
        return physics_formula.cross_product(self.x, self.y, other.x, other.y)
    
    def project_on(self, other: AbstractDirection) -> Vect:
        scalar = self.dot(other.normal)
        return other.normal * scalar
    
    @property
    @abstractmethod
    def perpendicular(self) -> AbstractDirection:
        pass
      
    @property
    @abstractmethod
    def antiperpendicular(self) -> AbstractDirection:
        """Negative of the perpendicular"""
        pass



class AbstractFigure(AbstractObject):
    _center: Point
    _vertices: tuple[Point, ...]
    _edges: tuple[Segment, ...]

    @property
    @abstractmethod
    def center(self) -> Point:
        pass
    
    @property
    @abstractmethod
    def vertices(self) -> tuple[Point, ...]:
        pass
    
    @property
    @abstractmethod
    def edges(self) -> tuple[Segment, ...]:
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        pass

    @property
    @abstractmethod
    def area(self) -> float:
        pass




class Movable(AbstractObject):
    ...
    # @property
    # @abstractmethod
    # def position(self) -> Point:
    #     pass
    
    # @property
    # @abstractmethod
    # def velocity(self) -> Direct:
    #     pass

    # @property
    # @abstractmethod
    # def angular_velocity(self) -> Direct:
    #     pass

    # @property
    # @abstractmethod
    # def linear_acceleration(self) -> Direct:
    #     pass

    # @property
    # @abstractmethod
    # def radial_acceleration(self) -> float:
    #     pass
    



class Tangible(AbstractObject):
    ...
    # @abstractmethod
    # def collide(self) -> bool:
    #     pass





class Point(AbstractObject):
    p_x: float
    p_y: float

    def __init__(self, p_x: float, p_y: float) -> None:
        self.p_x = p_x
        self.p_y = p_y

        super().__init__(p_x=self.p_x, p_y=self.p_y)

    @classmethod
    def from_pair(cls, pair: tuple[float, float]) -> Point:
        return cls(pair[0], pair[1]) 
    
    def __str__(self) -> str:
        return f'{type(self).__name__} at {repr(self.p_x)}, {repr(self.p_y)}'
    
    def __neg__(self) -> Point:
        return Point(-self.p_x, -self.p_y)
    
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
        if isinstance(other, Point):
            return math.isclose(self.p_x, other.p_x) and math.isclose(self.p_y, other.p_y)
        return False
    
    def __lt__(self, other: Point, normal: Normal) -> bool:
        ref_line = RefLine(self, normal)
        t1, t2  = self.loc_on_line(ref_line), other.loc_on_line(ref_line)
        return t1 < t2 if t1 and t2 else False
    
    def __gt__(self, other: Point, normal: Normal) -> bool:
        ref_line = RefLine(self, normal)
        t1, t2  = self.loc_on_line(ref_line), other.loc_on_line(ref_line)
        return t1 > t2 if t1 and t2 else False
    
    def __le__(self, other: Point, normal: Normal) -> bool:
        ref_line = RefLine(self, normal)
        t1, t2  = self.loc_on_line(ref_line), other.loc_on_line(ref_line)
        return t1 <= t2 if t1 and t2 else False
    
    def __ge__(self, other: Point, normal: Normal) -> bool:
        ref_line = RefLine(self, normal)
        t1, t2  = self.loc_on_line(ref_line), other.loc_on_line(ref_line)
        return t1 >= t2 if t1 and t2 else False
        
    def __hash__(self) -> int:
        return hash((self.p_x, self.p_y))
        
    def move_through_normal(self, normal: Normal, *, t: float=1) -> Point:
        return physics_formula.move_through_normal(self, normal, t)
    
    def loc_on_line(self, line: Line) -> float | None:
        return physics_formula.loc_on_line(self, line)




class Normal(AbstractDirection):
    _x: float
    _y: float

    def __init__(self, x: float, y: float) -> None:
        
        if x == 0 and y == 0:
            raise ValueError('Normal cannot be formed from 0 and 0')
        
        elif not math.isclose(math.hypot(x, y), 1):
            x, y = physics_formula.normal_normalize(x, y)
        
        else:
            self._x = x
            self._y = y

        super().__init__(_x=x, _y=y)

    @classmethod
    def from_pair(cls, l: tuple[float, float]) -> Normal:
        x, y = l
        return cls(x, y)
    
    @classmethod
    def from_vector(cls, v: Vect) -> Normal:
        x, y = v.x, v.y
        return cls(x, y)

    def __abs__(self) -> Normal:
        if self.y > 0:
            return self
        else:
            return -self
    
    def __neg__(self) -> Normal:
        return Normal(-self._x, -self._y)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Normal):
            return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        return False
        
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    @property
    def magnitude(self) -> float:
        return 1
    
    @property
    def normal(self) -> Normal:
        return self
    
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def perpendicular(self) -> Normal:
        return Normal(-self._y, self._x)
      
    @property
    def antiperpendicular(self) -> Normal:
        """Negative of the perpendicular"""
        return Normal(self._y, -self._x)




class Vect(AbstractDirection):
    _magnitude: float
    _normal: Normal

    def __init__(self, mag: float, normal: Normal):
        
        self._magnitude = mag
        self._normal = normal
        
        super().__init__(_magnitude=self._magnitude, _normal=self._normal)

    @classmethod
    def normdef(cls, x: float, y: float):
        normal = Normal(x, y)
        
        if x == 0 and y == 0:
            raise ValueError('Vector cannot be formed from 0 and 0')
        
        if y == 0:
            mag = x / normal.x
        
        elif x == 0:
            mag = y / normal.y

        else:
            mag = (y/normal.y) + (x/normal.x) / 2

        return cls(mag, normal)
    
    @classmethod
    def from_pair(cls, l: tuple[float, float]) -> Vect:
        return cls.normdef(*l)

    def __abs__(self) -> Vect:
        if self.y > 0:
            return self
        else:
            return -self
    
    def __neg__(self) -> Vect:
        return Vect.normdef(-self.x, -self.y)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vect):
            return math.isclose(self._magnitude, other.magnitude) and self._normal == other._normal
        return False
        
    def __hash__(self) -> int:
        return hash((self._magnitude, (self.x, self.y)))
    
    @property
    def magnitude(self):
        return self._magnitude
    
    @property
    def normal(self):
        return self._normal
    
    @property
    def x(self):
        return self._magnitude * self._normal.x
    
    @property
    def y(self):
        return self._magnitude * self._normal.y

    @property
    def perpendicular(self) -> Vect:
        return Vect.normdef(-self.y, self.x)
      
    @property
    def antiperpendicular(self) -> Vect:
        """Negative of the perpendicular"""
        return Vect.normdef(self.y, -self.x)




class Projectile(Tangible, Movable):
    def __init__(self, pos: Point, vel: Vect, acc: Vect, rad: float) -> None:
        self._position = pos
        self._velocity = vel
        self._lin_acc = acc
        self._rad_acc = Vect(rad, vel.normal.perpendicular)

        super().__init__(
            _position = self._position,
            _velocity = self._velocity,
            _lin_acc = self._lin_acc,
            _rad_acc = self._rad_acc)
            

    def _apply_vel(self) -> Point:
        end_x = self._position.p_x + self._velocity.x
        end_y = self._position.p_y + self._velocity.y

        return Point(end_x, end_y)

    def _apply_lin_acc(self) -> Vect:
        init_magnitude = self._velocity.magnitude
        next_vect = self._velocity + self._lin_acc 
        end_vel = Vect(init_magnitude, next_vect.normal)
        
        return end_vel
    
    def _apply_rad_acc(self) -> Vect:
        init_magnitude = self._velocity.magnitude
        next_vect = self._velocity + self._rad_acc 
        end_vel = Vect(init_magnitude, next_vect.normal)
        self._rad_acc = Vect(self._rad_acc.magnitude, end_vel.normal.perpendicular)
        
        return end_vel

    def sim_linear_movement(self) -> None:
        self._velocity += self._apply_lin_acc()
        self._position = self._apply_vel()

    def sim_radial_movement(self) -> None:
        self._velocity = self._apply_rad_acc()
        self._position = self._apply_vel()
    
 


class Line(AbstractPath):
    def __init__(self, origin: Point, normal: Normal) -> None:
        intercept = physics_formula.find_virtual_intercept(origin, normal)
        
        if abs(normal) != Normal(0,1) and isinstance(intercept, Point):
            origin = intercept

        if normal.y < 0:
            normal = -normal
        self._origin = origin
        self._normal = normal

        if self._normal.x == 0:
            end_x = origin.p_x
        else:
            mult_x = self._normal.x / abs(self._normal.x)
            end_x = math.inf * mult_x
        
        if self._normal.y == 0:
            end_y = origin.p_y
        else:
            mult_y = self._normal.y / abs(self._normal.y)
            end_y = math.inf * mult_y

        self._end = Point(end_x, end_y)

        super().__init__(_origin=origin, _normal=normal)
    
    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} with normal {repr(self._normal)}'
    
    def __hash__(self) -> int:
        
        return hash((self._origin, self._normal))
    
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
    



class RefLine(Line):
    def __init__(self, origin: Point, normal: Normal) -> None:
        self._origin = origin
        self._normal = normal

    


class Segment(AbstractFinitePath):
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
    
    def __hash__(self) -> int:
        return hash(frozenset((self._origin, self._end)))
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Segment):
            return (self._origin == other.end or self._end == other.end) and abs(self.normal) == abs(other.normal)
        return False

    @classmethod
    def from_pair(cls, pair: tuple[Point, Point]) -> Segment:
        return cls(pair[0], pair[1])
    
    @property
    def midpoint(self) -> Point:
        mid_y = (self._end.p_y + self._origin.p_y) / 2
        mid_x = (self._end.p_x + self._origin.p_x) / 2
        return Point(mid_x, mid_y)
    
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
    
    


class Ray(AbstractPath):
    def __init__(self, origin: Point, normal: Normal) -> None:
        self._origin = origin
        self._normal = normal
        
        if self._normal.x == 0:
            end_x = origin.p_x
        else:
            mult_x = self._normal.x / abs(self._normal.x)
            end_x = math.inf * mult_x
        
        if self._normal.y == 0:
            end_y = origin.p_y
        else:
            mult_y = self._normal.y / abs(self._normal.y)
            end_y = math.inf * mult_y

        self._end = Point(end_x, end_y)

        super().__init__(_origin=origin, _normal=normal, _end=self._end)
    
    
    @classmethod
    def from_points(cls, origin: Point, end: Point) -> Ray:
        x1, y1 = origin.p_x, origin.p_y
        x2, y2 = end.p_x, end.p_y
        normal = physics_formula.normal_normalize(x2-x1, y2-y1)
        return cls(origin, Normal.from_pair(normal))
    
    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} and headed to {repr(self._normal)}'

    def __hash__(self) -> int:
        return hash(frozenset((self._origin, self._end)))

    def __neg__(self) -> Ray:
        return Ray(self._origin, -self._normal)
    
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
        
    def point_at_t(self, t: float) -> Point | None:
        p = self._origin.move_through_normal(self._normal, t=t)
        if t < 0:
            return
        return p
    



class Direct(AbstractFinitePath):
    def __init__(self, origin: Point, end: Point) -> None:
        self._origin = origin
        self._end = end

        x1, y1 = self._origin.p_x, self._origin.p_y
        x2, y2 = self._end.p_x, self._end.p_y

        d = physics_formula.normal_normalize(x2-x1, y2-y1)
        self._normal = Normal.from_pair(d)

        super().__init__(_origin=origin, _end=end)

    def __hash__(self) -> int:
        return hash((self._origin, self._end))

    def __str__(self) -> str:
        return f'{type(self).__name__} starting on {repr(self._origin)} and ending on {repr(self._end)}'
    
    def __eq__(self, other: object) -> bool:
        if super().__eq__(other) and self._end == self._end:
            return True
        return False
    
    def __neg__(self) -> Direct:
        return Direct(self._end, self._origin)

    @classmethod
    def from_pair(cls, pair: tuple[Point, Point]) -> Direct:
        return cls(pair[0], pair[1])
    
    @property
    def midpoint(self) -> Point:
        mid_y = (self._end.p_y + self._origin.p_y) / 2
        mid_x = (self._end.p_x + self._origin.p_x) / 2
        return Point(mid_x, mid_y)
    
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
    
        


class Shape(AbstractFigure):
    def __new__(cls, *points: Point) -> Point | AbstractPath | Shape | None:
        v = len(points)
        match v:
            case 0:
                return
            
            case 1:
                (p,) = points
                return p
            
            case 2:
                obj = object.__new__(Segment)
                return Segment(*points)
            
            case 3:
                obj = object.__new__(Triangle) 
                obj.__init__(*points)
                return obj
            
            case 4:
                p1, p2, p3, p4 = points
                if abs(Segment(p1, p2).normal) == abs(Segment(p3, p4).normal) and \
                    abs(Segment(p1, p4).normal) == abs(Segment(p2, p3).normal):
                    obj = object.__new__(QuadReg)
                    obj.__init__(*points)
                    return obj
                
            case _:
                pass

        obj = object.__new__(Polygon) 
        obj.__init__(*points)
        return obj

    def __init__(self, *points: Point) -> None:
        edges: list[Segment] = []
        for i in (x := range(len(points))):
            edges.append(Segment(points[i % len(x)], points[(i+1) % len(x)]))

        
        self._center = physics_formula.locate_center(points, edges)
        self._vertices = tuple(points)
        self._edges = tuple(edges)

        super().__init__(_center=self._center, _vertices=self._vertices, _edges=self._edges)

    @property
    def center(self) -> Point:
        return self._center
    
    @property
    def vertices(self) -> tuple[Point, ...]:
        return self._vertices
    
    @property
    def edges(self) -> tuple[Segment, ...]:
        return self._edges

    @property
    def perimeter(self) -> float:
        p = 0
        for edge in self.edges:
            p += edge.length

        return p
    @property
    def area(self) -> float:
        return physics_formula.shoelace_area(self._vertices)

    def intersects(self, other: AbstractPath | AbstractFigure) -> AbstractPath | tuple[Point, Point] | Point | None:
        ...




class Polygon(Shape):
    def __init__(self, *points: Point) -> None:
        super().__init__(*points)




class Circle(AbstractFigure):
    _radius: float
    def __init__(self, center: Point, radius: float) -> None:
        self._center = center
        self._radius = abs(radius)
        self._edges = self.approximate_edge()
        self._vertices = self.approximate_vertices()

        super().__init__(_center=self._center, 
                         _radius=self._radius,
                         _edges=self._edges,
                         _vertices=self._vertices)
    
    def approximate_vertices(self) -> tuple[Point, ...]:
        segments = 32

        return tuple(
        (
            Point(self._center.p_x + self._radius * math.cos(2 * math.pi * i / segments),
            self._center.p_y + self._radius * math.sin(2 * math.pi * i / segments))
        )
        for i in range(segments)
        )

    def approximate_edge(self) -> tuple[Segment, ...]:
        vertices = self.approximate_vertices()
        v = len(vertices)

        segments: list[Segment] = []
        for i in range(v):
            p1 = vertices[i]
            p2 = vertices[(i+1)%v]

            segments.append(Segment(p1,p2))

        return tuple(segments)


    @property
    def center(self) -> Point:
        return self._center
    
    @property
    def vertices(self) -> tuple[Point, ...]:
        return self._vertices
    
    @property
    def edges(self) -> tuple[Segment, ...]:
        return self._edges

    @property
    def perimeter(self) -> float:
        return 2 * math.pi * self._radius

    @property
    def area(self) -> float:
        return math.pi * self._radius ** 2




class Triangle(Shape):
    def __init__(self, *points: Point) -> None:
        super().__init__(*points)




class QuadReg(Shape):
    def __init__(self, *points: Point) -> None:
        super().__init__(*points)




class Ball(Circle, Projectile):
    ...




class Surface(Segment, Tangible):
    ...




class physics_formula:
    
    @staticmethod
    def line_slope(path: AbstractPath):
        x1, y1 = path.origin.p_x, path.origin.p_y
        next = path.origin.move_through_normal(path.normal)
        x2, y2 = next.p_x, next.p_y

        dy, dx = y2-y1, x2-x1
        if math.isclose(dx, 0):
            return math.inf if (dy/dx) >= 0 else -math.inf
        
        else: 
            return dy/dx

    @staticmethod
    def vector_split(v: AbstractDirection, rel: AbstractDirection) -> tuple[Vect, Vect]:
        parallel = v.project_on(rel)
        perpendicular = v - parallel
        return parallel, perpendicular
    
    @staticmethod
    def move_through_normal(point: Point, normal: Normal, t: float) -> Point:
        new_p_x = point.p_x + (t*normal.x)
        new_p_y = point.p_y + (t*normal.y)

        return Point(new_p_x, new_p_y)
    
    @staticmethod
    def loc_on_line(point: Point, line: Line) -> float:
        origin, normal = line.origin, line.normal
        if normal.x == 0:
            return (point.p_y-origin.p_y)/normal.y if math.isclose(point.p_x, origin.p_x) else math.nan
        elif normal.y == 0:
            return (point.p_x-origin.p_x)/normal.x if math.isclose(point.p_y, origin.p_y) else math.nan

        tx = (point.p_x-origin.p_x)/normal.x
        ty = (point.p_y-origin.p_y)/normal.y
        if math.isclose(tx, ty):
            return (tx+ty)/2
        
        else:
            return math.nan
        
    @staticmethod
    def contains_check(p: Point, path: AbstractPath) -> bool:
        ref_line = RefLine(path.origin, path.normal)
        t = physics_formula.loc_on_line(p, ref_line)
        if math.isclose(t, 0):
            return True

        if math.isnan(t):
            return False

        t_min, t_max = path.scalar_bounds
        
        ep = 1e-9
        return t_min - ep <= t <= t_max + ep  
    
    @staticmethod
    def line_length(start: Point, end: Point) -> float:
        x1, y1 = start.p_x, start.p_y
        x2, y2 = end.p_x, end.p_y
        
        return math.hypot(y2-y1, x2-x1)
    
    @staticmethod
    def find_virtual_intercept(origin: Point, normal: Normal) -> Point | None:
        if normal.x == 0:
            return
        intercept_t = -origin.p_x / normal.x
        return physics_formula.move_through_normal(origin, normal, intercept_t)
    
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
    def check_instance_return_point(a: AbstractPath) -> Point:
        if isinstance(a, Line) or isinstance(a, Ray):
            return a.origin.move_through_normal(a.normal)
        
        else:
            return a.end
        
    @staticmethod 
    def find_intersection(a: AbstractObject, b: AbstractObject) -> AbstractPath | tuple[Point | AbstractPath, ...] | Point | None:
        if isinstance(a, AbstractPath) and isinstance(b, AbstractPath):
            return physics_formula.intersects_line(a, b)
        
        elif isinstance(a, AbstractFigure) and isinstance(b, AbstractPath):
            intersections: list[Point | AbstractPath] = []
            for i in a.edges:
                if intersection := physics_formula.intersects_line(i, b):
                    intersections.append(intersection)
            return tuple(intersections)
        
        elif isinstance(a, AbstractPath) and isinstance(b, AbstractFigure):
            intersections: list[Point | AbstractPath] = []
            for i in b.edges:
                if intersection := physics_formula.intersects_line(i, a):
                    intersections.append(intersection)
            return tuple(intersections)
        
        else: 
            assert isinstance(a, AbstractFigure) and isinstance(b, AbstractFigure)
            intersections: list[Point | AbstractPath] = []
            for i in a.edges:
                for j in b.edges:
                    if intersection := physics_formula.intersects_line(i, j):
                        intersections.append(intersection)
            return tuple(intersections)
  
    @staticmethod
    def intersects_line(a: AbstractPath, b: AbstractPath) -> Point | AbstractPath | None:
        if c := physics_formula.check_collinear(a, b):
            return c

        t1, t2 = physics_formula.intersects_check(a, b)
        if t1 == math.inf or t2 == math.inf:
            return None

        t1_min, t1_max = a.scalar_bounds
        t2_min, t2_max = b.scalar_bounds
        
        ep = 1e-9
        if t1_min-ep <= t1 <= t1_max+ep and t2_min-ep <= t2 <= t2_max+ep:
            try:
                return a.point_at_t(t1)
            except ValueError:
                pass
            
        return None

    @staticmethod
    def intersects_check(a: AbstractPath, b: AbstractPath) -> tuple[float, float]:
        def vector(p1: Point, p2: Point) -> Vect:
            return Vect.normdef(p2.p_x - p1.p_x, p2.p_y - p1.p_y)

        p = a.origin
        r = vector(a.origin, physics_formula.check_instance_return_point(a))
        
        q = b.origin
        s = vector(b.origin, physics_formula.check_instance_return_point(b))
        
        r_cross_s = r.cross(s)
        q_minus_p = Vect.normdef(q.p_x - p.p_x, q.p_y - p.p_y)
        
        qmp_cross_r = q_minus_p.cross(r)
        if math.isclose(r_cross_s, 0.0, abs_tol=1e-9):
            if math.isclose(qmp_cross_r, 0.0, abs_tol=1e-9):
                # Lines are collinear — may overlap (handle separately if needed)
                return 0.0, 0.0
            else:
                # Lines are parallel and non-intersecting
                return math.inf, math.inf
        
        t = q_minus_p.cross(s) / r_cross_s
        u = q_minus_p.cross(r) / r_cross_s

        return t, u
    
    @staticmethod
    def check_collinear(a: AbstractPath, b: AbstractPath) -> Point | AbstractPath | None:
        ref_a = Line(a.origin, a.normal)
        ref_b = Line(b.origin, b.normal)
        if abs(a.normal) != abs(b.normal) or a.origin not in ref_b or b.origin not in ref_a:
            return None
        
        elif isinstance(a, AbstractFinitePath) and isinstance(b, AbstractFinitePath) or \
            isinstance(a, AbstractFinitePath) and isinstance(b, Ray) or \
            isinstance(a, Ray) and isinstance(b, AbstractFinitePath) or \
            isinstance(a, Ray) and isinstance(b, Ray):
            # print('AbstractFinitePath | AbstractFinitePath or AbstractFinitePath | Ray')
            if out := physics_formula.compare_ending_paths(a, b):
                return out
        
        elif isinstance(a, Segment) or isinstance(b, Segment):
            # print('Segment | Line ')
            return a if isinstance(a, Segment) else b
        
        elif isinstance(a, Direct) or isinstance(b, Direct):
            # print('Direct | Line ')
            return a if isinstance(a, Direct) else b
        
        elif isinstance(a, Ray) or isinstance(b, Ray):
            # print('Ray | Line or Ray | Ray')
            return a if isinstance(a, Ray) else b

        else:
            # print('Line | Line')
            return a
            
    @staticmethod
    def compare_ending_paths(a: AbstractFinitePath | Ray, b: AbstractFinitePath | Ray) -> Point | AbstractPath | None:
        points = [a.origin, a.end, b.origin, b.end]
        ref_line = RefLine(a.origin, a.normal)
        data = [(point, ref_line) for point in points]

        def key(d: tuple[Point, Line]) -> float:
            p, n = d
            return physics_formula.loc_on_line(p, n)

        sorted_data = sorted(data, key=key)
        sorted_points, _ = (zip(*sorted_data))
        sorting_data: list[float] = []
        
        for point in sorted_points:
            sorting_data.append(physics_formula.loc_on_line(point, ref_line))

        p1, p2 = sorted_points[1:3]

        if p1 == p2:
            return p1

        elif sorting_data[2] == math.inf:
            return Ray(p1, ref_line.normal)
        
        else:
            pass
        
        test_seg = Segment(p1, p2)
        if test_seg == a or test_seg == b:
            return test_seg

        elif p1 in a and p2 in b and p1 in b and p2 in a:
            return Segment(p1, p2)
        
        else:
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
    
    @staticmethod
    def locate_center(vertices: Sequence[Point], edges: Sequence[Segment]) -> Point:
        x_list, y_list = zip(*((point.p_x, point.p_y) for point in vertices))

        n = len(vertices)
        area = 0
        Cx = 0
        Cy = 0

        for i in range(n):
            xi, yi = x_list[i], y_list[i]
            xi1, yi1 = x_list[(i+1)%n], y_list[(i+1)%n]
            cross = physics_formula.cross_product(xi, yi, xi1, yi1)

            area += cross
            Cx += (xi + xi1) * cross
            Cy += (yi + yi1) * cross

        area *= 0.5
        Cx /= (6*area)
        Cy /= (6*area)

        return Point(Cx, Cy)
    
    @staticmethod
    def shoelace_area(vertices: Sequence[Point]) -> float:
        x_list, y_list = zip(*((point.p_x, point.p_y) for point in vertices))
        area = 0
        n = len(vertices)

        for i in range(len(vertices)):
            xi, yi = x_list[i], y_list[i]
            xi1, yi1 = x_list[(i+1)%n], y_list[(i+1)%n]
            cross = physics_formula.cross_product(xi, yi, xi1, yi1)
            area += cross

        return abs(area)

    @staticmethod
    def cross_product(x1: float, y1: float, x2: float, y2: float) -> float:
        return x1*y2 - x2*y1
    
    @staticmethod
    def dot_product(x1: float, y1: float, x2: float, y2: float) -> float:
        return x1*x2 + y1*y2
    

# sample = Projectile(Point(0,0),Vect.normdef(1,0),Vect.normdef(1,1),0.1)    
# sample.sim_radial_movement()
# sample.sim_linear_movement()
