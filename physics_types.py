from __future__ import annotations
from enum import Enum, auto
from abc import ABC, abstractmethod
import math


def rad_to_deg(radians: float) -> float:
    """Convert radians to degrees."""
    return radians * (180 / math.pi)

def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians."""
    return degrees * (math.pi / 180)

class Shape(ABC):
    """Abstract base class for all shapes."""
    def __repr__(self):
        return f"{self.__class__.__name__}()"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Shape):
            return False
        return self.__dict__ == value.__dict__
    
    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))


    @property
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass

    @property
    @abstractmethod
    def center(self) -> Point:
        """Returns the center of the shape."""
        pass

    @property
    @abstractmethod
    def edges(self) -> tuple[Line, ...]:
        """Returns the edges of the shape."""
        pass

    @property
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass


class Point:
    def __init__(self, p_x: float, p_y: float):
        self.p_x = p_x
        self.p_y = p_y

    def __repr__(self):
        return f"Point({self.p_x}, {self.p_y})"

    def __sub__(self, other: Point) -> Point:
        return Point(self.p_x - other.p_x, self.p_y - other.p_y)

    def __add__(self, other: Point) -> Point:
        return Point(self.p_x + other.p_x, self.p_y + other.p_y)

    def __mul__(self, scalar: float):
        return Point(self.p_x * scalar, self.p_y * scalar)

    def __truediv__(self, scalar: float):
        return Point(self.p_x / scalar, self.p_y / scalar)


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{type(self).__name__}({self.start}, {self.end})"

    @property
    def length(self) -> float:
        """Returns the length of the line"""
        return ((self.end.p_x - self.start.p_x) ** 2 + (self.end.p_y - self.start.p_y) ** 2) ** 0.5

    @property
    def slope(self) -> float:
        """Returns the slope of the line"""
        if self.end.p_x - self.start.p_x == 0:
            return float('inf')  if self.end.p_y > self.start.p_y else float('-inf')
        return (self.end.p_y - self.start.p_y) / (self.end.p_x - self.start.p_x)
    
    @property
    def angle(self) -> float:
        """Returns the angle of the line against the positive x-axis"""
        if self.end.p_x - self.start.p_x == 0:
            return math.degrees(math.pi / 2) if self.end.p_y > self.start.p_y else math.degrees(3*math.pi / 2)
        raw_deg: float = math.degrees(math.atan2(self.end.p_y - self.start.p_y, self.end.p_x - self.start.p_x))
        return raw_deg + 360 if raw_deg < 0 else raw_deg
    
    @property
    def midpoint(self) -> Point:
        """Returns the midpoint of the line"""
        return Point((self.start.p_x + self.end.p_x) / 2, (self.start.p_y + self.end.p_y) / 2)
    
class Ray(Line):
    """A ray is a line that starts at a point and extends infinitely in one direction."""
    def __init__(self, start: Point, end: Point):
        super().__init__(start, end)
        self._direction = self.angle
    
    @property
    def direction(self) -> float:
        return self._direction

class Vect(Line):
    """A vector is a line with a direction and magnitude."""
    def __init__(self, start: Point, end: Point):
        super().__init__(start, end)
        self._magnitude = self.length
        self._direction = self.angle
    
    @property
    def magnitude(self) -> float:
        return self._magnitude
    
    @property
    def direction(self) -> float:
        return self._direction
    
    
class Polygon(Shape):
    """A polygon is defined by its vertices. The vertices must be provided in order (clockwise or counter-clockwise)."""
    def __init__(self, *vertices: Point):
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")
        self.vertices: tuple[Point, ...] = tuple(vertex for vertex in vertices)

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(map(str, self.vertices))})"
    

    @property
    def center(self) -> Point:
        x = sum(vertex.p_x for vertex in self.vertices) / len(self.vertices)
        y = sum(vertex.p_y for vertex in self.vertices) / len(self.vertices)
        return Point(x, y)
    
    @property
    def edges(self) -> tuple[Line, ...]:
        edges: list[Line] = []
        for i in range(len(self.vertices)):
            start = self.vertices[i]
            end = self.vertices[(i + 1) % len(self.vertices)]
            edges.append(Line(start, end))
        return tuple(edges)
    
    @property
    def area(self) -> float:
        area: float = 0.0
        for i in range(len(self.vertices)):
            j = (i + 1) % len(self.vertices)
            area += self.vertices[i].p_x * self.vertices[j].p_y
            area -= self.vertices[j].p_x * self.vertices[i].p_y
        return abs(area) / 2.0  

    @property
    def perimeter(self) -> float:
        perimeter: float = 0.0
        for edge in self.edges:
            perimeter += edge.length
        return perimeter  


class Circle(Shape):
    def __init__(self, p_x: float, p_y: float, r: float):
        self._p_x: float = p_x
        self._p_y: float = p_y

        self._r: float = r

    def __post_init__(self):
        if self._r <= 0:
            raise ValueError("Radius must be positive.")
        
    @classmethod
    def from_point(cls, point: Point, radius: float) -> Circle:
        return cls(p_x=point.p_x, p_y=point.p_y, r=radius)

    def __repr__(self):
        return f"Circle(x={self._p_x}, y={self._p_y}, radius={self._r})"
    
    def __eq__(self, value: object) -> bool:
        return super().__eq__(value)
    
    @property
    def perimeter(self) -> float:
        return 2 * math.pi * self._r
    
    @property
    def area(self) -> float:
        return math.pi * self._r ** 2
    
    @property
    def center(self) -> Point:
        return Point(self._p_x, self._p_y)
    
    @property
    def edges(self) -> tuple[Line, ...]:
        # For a circle, we can represent the edges as a series of lines forming a polygonal approximation
        num_edges = 36  # Number of edges to approximate the circle
        edges: list[Line] = []
        for i in range(num_edges):
            angle1 = (2 * math.pi / num_edges) * i
            angle2 = (2 * math.pi / num_edges) * (i + 1)
            start = Point(self._p_x + self._r * math.cos(angle1), self._p_y + self._r * math.sin(angle1))
            end = Point(self._p_x + self._r * math.cos(angle2), self._p_y + self._r * math.sin(angle2))
            edges.append(Line(start, end))
        return tuple(edges)
    
    @property
    def top(self):
        return self._p_y - self._r

    @property
    def bottom(self):
        return self._p_y + self._r

    @property
    def left(self):
        return self._p_x - self._r

    @property
    def right(self):
        return self._p_x + self._r


class Ball(Circle):
    def __init__(self, *, p_x: float, p_y: float, v_x: float, v_y: float, a_x: float, a_y: float, r: float):
        super().__init__(p_x=p_x, p_y=p_y, r=r)
        self._v_x = v_x
        self._v_y = v_y
        self._a_x = a_x
        self._a_y = a_y

    def __repr__(self):
        return f"Ball(x={self.p_x}, y={self.p_y}, v_x={self.v_x}, v_y={self.v_y}, a_x={self.a_x}, a_y={self.a_y}, radius={self.r})"
    
    @classmethod
    def from_bearing(cls, *, p_x: float, p_y: float, v_m: float, v_d: float, a_m: float = 0.0, a_d: float = 0.0, r: float = 1.0) -> Ball:
        if r <= 0:
            raise ValueError("Radius must be positive.")
        
        if  v_m < 0 or a_m < 0:
            raise ValueError("Magnitude must be non-negative.")
        
        if v_d < 0 or v_d > 360 or a_d < 0 or a_d > 360:
            raise ValueError("Direction must be between 0 and 360 degrees.")
        
        # Convert polar coordinates to Cartesian coordinates
        # _p_x = p_m * math.cos(math.radians(p_d))
        # _p_y = p_m * math.sin(math.radians(p_d))        
        _v_x = v_m * math.cos(math.radians(v_d))
        _v_y = v_m * -math.sin(math.radians(v_d))
        _a_x = a_m * math.cos(math.radians(a_d))
        _a_y = a_m * -math.sin(math.radians(a_d))

        return cls(p_x=p_x, p_y=p_y, v_x=_v_x, v_y=_v_y, a_x=_a_x, a_y=_a_y, r=r)
    
    @property
    def r(self) -> float:
        return self._r
    
    @property
    def p_x(self) -> float:
        return self._p_x
    
    @property
    def p_y(self) -> float:
        return self._p_y
    
    # @property
    # def p_m(self) -> float:
    #     return (self._p_x**2 + self._p_y**2)**0.5
    
    # @property
    # def p_d(self) -> float:
    #     if self.p_x == 0 and self.p_y == 0:
    #         return 0.0
    #     if self.p_x == 0:
    #         return 270 if self.p_y > 0 else 90
    #     raw_deg: float = math.degrees(-math.atan2(self.p_y, self.p_x))
    
    @property
    def v_x(self) -> float:
        return self._v_x
    
    @property
    def v_y(self) -> float:
        return self._v_y
    
    @property
    def v_m(self) -> float:
        return (self._v_x**2 + self._v_y**2)**0.5
    
    @property
    def v_d(self) -> float:
        if self.v_x == 0 and self.v_y == 0:
            return 0.0
        if self.v_x == 0:
            return 270 if self.v_y > 0 else 90
        raw_deg: float = math.degrees(math.atan2(-self.v_y, self.v_x))
        return raw_deg + 360 if raw_deg < 0 else raw_deg

    @property
    def a_x(self) -> float:
        return self._a_x
    
    @property
    def a_y(self) -> float:
        return self._a_y
    
    @property
    def a_m(self) -> float:
        return (self._a_x**2 + self._a_y**2)**0.5
    
    @property
    def a_d(self) -> float:
        if self.a_x == 0 and self.a_y == 0:
            return 0.0
        if self.a_x == 0:
            return 270 if self.a_y > 0 else 90
        raw_deg: float = math.degrees(math.atan2(-self.a_y, self.a_x))
        return raw_deg + 360 if raw_deg < 0 else raw_deg

    
    @p_x.setter
    def p_x(self, value: float):
        self._p_x = value
        if self.v_m == 0:
            self._v_x = 0
            self._v_y = 0
        if self.a_m == 0:
            self._a_x = 0
            self._a_y = 0

    @p_y.setter
    def p_y(self, value: float):
        self._p_y = value
        if self.v_m == 0:
            self._v_x = 0
            self._v_y = 0
        if self.a_m == 0:
            self._a_x = 0
            self._a_y = 0

    @r.setter
    def r(self, value: float):
        if value <= 0:
            raise ValueError("Radius must be positive.")
        self._r = value
        if self.v_m == 0:
            self._v_x = 0
            self._v_y = 0
        if self.a_m == 0:
            self._a_x = 0
            self._a_y = 0

    @v_x.setter
    def v_x(self, value: float):
        self._v_x = value
        if self.v_m == 0:
            self._v_y = 0

    @v_y.setter
    def v_y(self, value: float):
        self._v_y = value
        if self.v_m == 0:
            self._v_x = 0
    
    @v_m.setter
    def v_m(self, value: float):
        if value < 0:
            raise ValueError("Speed must be non-negative.")
        if self.v_m == 0:
            self._v_x = 0
            self._v_y = 0
        else:
            ratio = value / self.v_m
            self._v_x *= ratio
            self._v_y *= ratio

    @v_d.setter
    def v_d(self, value: float):
        if self.v_m == 0:
            return
        if value < 0:
            value = (value % 360) + 360
        if value > 360:
            value = (value % 360)
        rad = math.radians(value)
        self._v_x = self.v_m * math.cos(rad)
        self._v_y = self.v_m * math.sin(rad)

    @a_x.setter
    def a_x(self, value: float):
        self._a_x = value
        if self.a_m == 0:
            self._a_y = 0

    @a_y.setter
    def a_y(self, value: float):
        self._a_y = value
        if self.a_m == 0:
            self._a_x = 0

    @a_m.setter
    def a_m(self, value: float):
        if value < 0:
            raise ValueError("Acceleration must be non-negative.")
        if self.a_m == 0:
            self._a_x = 0
            self._a_y = 0
        else:
            ratio = value / self.a_m
            self._a_x *= ratio
            self._a_y *= ratio

    @a_d.setter
    def a_d(self, value: float):
        if self.a_m == 0:
            return
        if value < 0:
            value = (value % 360) + 360
        if value > 360:
            value = (value % 360)
        rad = math.radians(value)
        self._a_x = self.a_m * math.cos(rad)
        self._a_y = self.a_m * math.sin(rad)


class Rectangle(Shape):
    def __init__(self, x: float, y: float, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return f"Rectangle(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
    
    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    @property
    def area(self) -> float:
        return self.width * self.height
    
    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2, self.y + self.height / 2)
    
    @property
    def edges(self) -> tuple[Line, ...]:
        top_left = Point(self.x, self.y)
        top_right = Point(self.x + self.width, self.y)
        bottom_left = Point(self.x, self.y + self.height)
        bottom_right = Point(self.x + self.width, self.y + self.height)
        
        return (
            Line(top_left, top_right),
            Line(top_right, bottom_right),
            Line(bottom_right, bottom_left),
            Line(bottom_left, top_left),
        )



class SurfaceType(Enum):
    OUT = auto()
    IN = auto()
    DOUBLE = auto()



class Surface(Line):
    def __init__(self, *, start: Point, end: Point, surface_type: SurfaceType, bounce_constant: float = 1.0, friction: float = 1.0):
        super().__init__(start, end)
        self.surface_type: SurfaceType = surface_type
        self.bounce_constant: float = bounce_constant
        self.friction: float = friction

    def __repr__(self):
        if self.bounce_constant == 1.0 and self.friction == 1.0:
            return f"Surface(start={self.start}, end={self.end}, surface_type={self.surface_type})"
        
        elif self.bounce_constant == 1.0:
            return f"Surface(start={self.start}, end={self.end}, surface_type={self.surface_type}, friction={self.friction})"
        
        elif self.friction == 1.0:
            return f"Surface(start={self.start}, end={self.end}, surface_type={self.surface_type}, bounce_constant={self.bounce_constant})"
        
        else:
            return f"Surface(start={self.start}, end={self.end}, surface_type={self.surface_type}, bounce_constant={self.bounce_constant}, friction={self.friction})"

    @classmethod
    def from_line(cls, *, line: Line, surface_type: SurfaceType, bounce_constant: float = 1.0, friction: float = 1.0) -> Surface:
        return cls(start=line.start, end=line.end, surface_type=surface_type, bounce_constant=bounce_constant, friction=friction)

        
    