from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC, abstractmethod
import math



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
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float):
        return Point(self.x / scalar, self.y / scalar)


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"{type(self).__name__}({self.start}, {self.end})"

    @property
    def length(self) -> float:
        """Returns the length of the line"""
        return ((self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2) ** 0.5

    @property
    def slope(self) -> float:
        """Returns the slope of the line"""
        if self.end.x - self.start.x == 0:
            return float('inf')  # vertical line
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)
    
    @property
    def angle(self) -> float:
        """Returns the angle of the line against the positive x-axis"""
        if self.end.x - self.start.x == 0:
            return math.pi / 2
        return math.atan2(self.end.y - self.start.y, self.end.x - self.start.x)
        
    @property
    def midpoint(self) -> Point:
        """Returns the midpoint of the line"""
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)
    
    
    
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
        x = sum(vertex.x for vertex in self.vertices) / len(self.vertices)
        y = sum(vertex.y for vertex in self.vertices) / len(self.vertices)
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
            area += self.vertices[i].x * self.vertices[j].y
            area -= self.vertices[j].x * self.vertices[i].y
        return abs(area) / 2.0  

    @property
    def perimeter(self) -> float:
        perimeter: float = 0.0
        for edge in self.edges:
            perimeter += edge.length
        return perimeter  

@dataclass
class Circle(Shape):
    x: float
    y: float
    radius: float

    def __post_init__(self):
        if self.radius <= 0:
            raise ValueError("Radius must be positive.")

    def __repr__(self):
        return f"Circle(x={self.x}, y={self.y}, radius={self.radius})"
    
    def __eq__(self, value: object) -> bool:
        return super().__eq__(value)
    
    @property
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius
    
    @property
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    @property
    def center(self) -> Point:
        return Point(self.x, self.y)
    
    @property
    def edges(self) -> tuple[Line, ...]:
        # For a circle, we can represent the edges as a series of lines forming a polygonal approximation
        num_edges = 36  # Number of edges to approximate the circle
        edges: list[Line] = []
        for i in range(num_edges):
            angle1 = (2 * math.pi / num_edges) * i
            angle2 = (2 * math.pi / num_edges) * (i + 1)
            start = Point(self.x + self.radius * math.cos(angle1), self.y + self.radius * math.sin(angle1))
            end = Point(self.x + self.radius * math.cos(angle2), self.y + self.radius * math.sin(angle2))
            edges.append(Line(start, end))
        return tuple(edges)
    
    @property
    def top(self):
        return self.y - self.radius

    @property
    def bottom(self):
        return self.y + self.radius

    @property
    def left(self):
        return self.x - self.radius

    @property
    def right(self):
        return self.x + self.radius

@dataclass
class Ball(Circle):
    v_x: float
    v_y: float
    a_x: float
    a_y: float


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
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


class Surface(Line):
    def __init__(self, *, start: Point, end: Point, surface_types: tuple[SurfaceType, ...], bounce_constant: float = 1.0, friction: float = 1.0):
        super().__init__(start, end)
        self.surface_types: tuple[SurfaceType, ...] = surface_types
        self.bounce_constant: float = bounce_constant
        self.friction: float = friction

    def __repr__(self):
        if self.bounce_constant == 1.0 and self.friction == 1.0:
            return f"Surface(start={self.start}, end={self.end}, surface_types={self.surface_types})"
        
        elif self.bounce_constant == 1.0:
            return f"Surface(start={self.start}, end={self.end}, surface_types={self.surface_types}, friction={self.friction})"
        
        elif self.friction == 1.0:
            return f"Surface(start={self.start}, end={self.end}, surface_types={self.surface_types}, bounce_constant={self.bounce_constant})"
        
        else:
            return f"Surface(start={self.start}, end={self.end}, surface_types={self.surface_types}, bounce_constant={self.bounce_constant}, friction={self.friction})"

    @classmethod
    def from_line(cls, *, line: Line, surface_types: tuple[SurfaceType, ...], bounce_constant: float = 1.0, friction: float = 1.0) -> Surface:
        return cls(start=line.start, end=line.end, surface_types=surface_types, bounce_constant=bounce_constant, friction=friction)

        
    