from .physics_types import *
import math


p0 = Point(0, 0)
p1 = Point(3, 4)
p2 = Point(5, 1)
p3 = Point(5, 7)
p4 = Point(10, 8)
p5 = Point(2,2)
p6 = Point(1,-3)
p7 = Point(-3,1)
p8 = Point(2,3)
p9 = Point(4,1)
p10 = Point(-1,-3)
p11 = Point(4,3)
p12 = Point(0,3)
p13 = Point(-2,-1)

n0 = Normal(5, 10)
n1 = Normal(-5, 5)
n2 = Normal(1, 2)
n3 = Normal(-4, -3)
n4 = Normal(-1,1)
n5 = Normal(-1,3)

l0 = Line(p0, n0)
l1 = Line(p0, n1)
l2 = Line(p0, n2)
l3 = Line(p1, n0)
l4 = Line(p1, n3)
l5 = Line(p2, n1)
l6 = Line(p2, n2)
l7 = Line(p3, n3)
l8 = Line(p3, n0)
l9 = Line(p4, n1)
l10 = Line(p4, n2)
l11 = Line(p1, n2)
l12 = Line(p2, n3)
l13 = Line(p3, n1)
l14 = Line(p4, n3)
l15 = Line(p0, Normal(1,0))
l16 = Line(Point(0,2),Normal(1,0))

s0 = Segment(Point(2,2), Point(-2,-2))
s1 = Segment(Point(-2,2), Point(2, -2))
s2 = Segment(Point(0,0),Point(0,2))
s3 = Segment(Point(2,2),Point(2,0))
s4 = Segment(Point(0,0),Point(2,0))
s5 = Segment(Point(0,2),Point(2,2))
s6 = Segment(Point(0,0),Point(2,2))
s7 = Segment(Point(0,2),Point(2,4))
s8 = Segment(p1,p3)
s9 = Segment(p2,p4)
s10 = Segment(p1,p4)
s11 = Segment(p2,p3)
s12 = Segment(p1,p7)
s13 = Segment(p6,p5)
s14 = Segment(p5,p9)
s15 = Segment(p1,p7)
s16 = Segment(p8,p9)
s17 = Segment(p2, Point(-2,3))
s18 = Segment(Point(0,-1), Point(2,-5))

r0 = Ray(Point(-2,-2), Normal(1,1))
r1 = Ray(Point(2,2), Normal(-1,-1))
r2 = -r0
r3 = -r1
r4 = Ray(p2,n3)
r5 = Ray(p1,n1)


def test_point():
    
    
    assert p1.p_x == 3
    assert p1.p_y == 4
    assert p0.p_x == 0
    assert p0.p_y == 0

    
    assert p2 + p3 == Point(10, 8)
    assert p2 - p3 == Point(0, -6)
    assert p3 * 2 == Point(10, 14)
    assert p4 / 2 == Point(5, 4)
    assert p4 - p3 == p2

def test_normal():
    try:
        _ = Normal(0, 0)
    except ValueError:
        pass

    assert n0 == n2
    assert math.isclose(n1.x, -math.sqrt(2)/2)
    assert math.isclose(n1.y, math.sqrt(2)/2)
    assert abs(n3) == Normal(4, 3)
    assert abs(Normal(4, 3)) == Normal(4, 3)
    assert -n3 == Normal(4, 3)
    assert n0.perpendicular == Normal(-10, 5)
    assert n0.antiperpendicular == Normal(10, -5)

def test_line():
    assert l0.origin == p0
    assert l1.normal == n1
    assert math.isclose(l14.slope, n3.y/n3.x)

def test_segment():

    assert s1 == s0.perpendicular