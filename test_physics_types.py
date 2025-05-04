from .physics_types import *
import math


point0 = Point(0, 0)
point1 = Point(3, 4)
point2 = Point(5, 1)
point3 = Point(5, 7)
point4 = Point(10, 8)

vect0 = Vect(5, 10)
vect1 = Vect(-5, 5)
vect2 = Vect(1, 2)
vect3 = Vect(-4, -3)

line0 = Line(o=point0, n=vect0)
line1 = Line(o=point0, n=vect1)
line2 = Line(o=point0, n=vect2)
line3 = Line(o=point1, n=vect0)
line4 = Line(o=point1, n=vect3)
line5 = Line(o=point2, n=vect1)
line6 = Line(o=point2, n=vect2)
line7 = Line(o=point3, n=vect3)
line8 = Line(o=point3, n=vect0)
line9 = Line(o=point4, n=vect1)
line10 = Line(o=point4, n=vect2)
line11 = Line(o=point1, n=vect2)
line12 = Line(o=point2, n=vect3)
line13 = Line(o=point3, n=vect1)
line14 = Line(o=point4, n=vect3)

segment0 = Segment(Point(2,2), Point(-2,-2))
segment1 = Segment(Point(-2,2), Point(2, -2))

def test_point():
    
    
    assert point1.p_x == 3
    assert point1.p_y == 4
    assert point0.p_x == 0
    assert point0.p_y == 0

    
    assert point2 + point3 == Point(10, 8)
    assert point2 - point3 == Point(0, -6)
    assert point3 * 2 == Point(10, 14)
    assert point4 / 2 == Point(5, 4)
    assert point4 - point3 == point2

def test_vect():
    try:
        _ = Vect(0, 0)
    except ValueError:
        pass

    assert vect0 == vect2
    assert math.isclose(vect1.x, -math.sqrt(2)/2)
    assert math.isclose(vect1.y, math.sqrt(2)/2)
    assert abs(vect3) == Vect(-4, 3)
    assert -vect3 == Vect(4, 3)
    assert vect0.perpendicular == Vect(-10, 5)
    assert vect0.antiperpendicular == Vect(10, -5)

def test_line():
    assert line0.origin == point0
    assert line1.vect == vect1
    assert math.isclose(line14.slope, vect3.y/vect3.x)

def test_segment():

    assert segment1 == segment0.perpendicular