try:
    from physics_types import Ball, Surface, Point, SurfaceType
except ImportError:
    from physics_engine.physics_types import Ball, Surface, Point, SurfaceType

from dataclasses import dataclass

import math


@dataclass
class _Constants:
    """Constants for the physics model. Calculated against the fps of the game."""
    GRAVITY = 4000
    BOUNCE_FACTOR_X = 1
    BOUNCE_FACTOR_Y = 1
    FRICTIONAL_CONSTANT = 1
    SPEED_LIMIT_X = 2000
    JUMP_HEIGHT = 1100
    SIDEWARD_PUSH_ACCELERATION = 2100


class PhysicsModel:
    def __init__(self, fps: int, width: int, height: int):
        self._gravity = _Constants.GRAVITY / fps**2
        self._bounce_factor_x = _Constants.BOUNCE_FACTOR_X 
        self._bounce_factor_y = _Constants.BOUNCE_FACTOR_Y
        self._frictional_constant = _Constants.FRICTIONAL_CONSTANT ** (1/fps)
        self._surfaces = [
            Surface(start=Point(0, 0), end=Point(width, 0), surface_type=SurfaceType.IN),
            Surface(start=Point(width, 0), end=Point(width, height), surface_type=SurfaceType.IN),
            Surface(start=Point(width, height), end=Point(0, height), surface_type=SurfaceType.IN),
            Surface(start=Point(0, height), end=Point(0, 0), surface_type=SurfaceType.IN),
            ]
        
        self._width = width
        self._height = height
        self._fps = fps
        self._init_ball()

    @property
    def surfaces(self):
        return self._surfaces

    @property
    def gravity(self):
        return self._gravity

    @property
    def ball(self):
        return self._ball

    @property
    def ball_dist_from_every_surface(self):
        distances: list[float] = []
        for surface in self._surfaces:
            x1, x2, y1, y2 = surface.start.p_x, surface.end.p_x, surface.start.p_y, surface.end.p_y
            x3, y3 = self._ball.p_x, self._ball.p_y
            
            determinant: float = (y2 - y1)*x3 - (x2 - x1)*y3 + ((x2*y1) - (y2*x1))
            length: float = ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5
            
            match surface.surface_type:
                case SurfaceType.IN:
                    dist = -determinant / length
            
                case SurfaceType.OUT:
                    dist = determinant / length

                case SurfaceType.DOUBLE:
                    dist = abs(determinant / length)
       
            distances.append(dist)

        return distances

    @property
    def ball_dist_from_next_surface(self) -> float:
        distances = self.ball_dist_from_every_surface
        dist = min(distances)
        return dist
    

    @property
    def closest_surface(self) -> Surface:
        dist = self.ball_dist_from_next_surface
        distances = self.ball_dist_from_every_surface
        return self._surfaces[distances.index(dist)]


    def _surface_details(self) -> tuple[float, float, float, float]:
        x1, x2, y1, y2 = (
            self.closest_surface.start.p_x, 
            self.closest_surface.end.p_x, 
            self.closest_surface.start.p_y, 
            self.closest_surface.end.p_y)
        
        return x1, y1, x2, y2
    
    @staticmethod
    def unit_vector(a: float):
        dir_x, dir_y = (
            math.cos(math.radians(a)),
            -math.sin(math.radians(a))
        )
        return dir_x, dir_y
    
    def ray_intersection(self):
        dir_x, dir_y = self.unit_vector(self._ball.v_d)
        
        x3, y3 = self._ball.p_x, self._ball.p_y
        x4, y4 = self._ball.p_x + dir_x, self._ball.p_y + dir_y

        t, u = self.raycast(*self._surface_details(), x3, y3, x4, y4)
        intersection = (x3 + u * dir_x, y3 + u * dir_y)
        
        del(t)
        print(intersection)

    @staticmethod
    def raycast(x1: float, y1: float, 
                x2: float, y2: float, 
                x3: float, y3: float, 
                x4: float, y4: float) -> tuple[float, float]:
        
        denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
        if denom == 0:
            return (float('inf'), float('inf'))
        
        else:
            t: float = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / denom
            u: float = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)) / denom
            print(t, u)
            return (t, u)
    

    def check_bounce(self):
        # Check if the ball is going to bounce off the surface
        dir_x, dir_y = self.unit_vector(self._ball.v_d)

        x3, y3 = self._ball.p_x, self._ball.p_y
        x4, y4 = self._ball.p_x + dir_x, self._ball.p_y + dir_y
        
        t, u = self.raycast(*self._surface_details(), x3, y3, x4, y4)
        if t == float('inf') or u == float('inf'):
            pass
        else:
            max_distance = self._ball.v_m
            epsilon = 1e-2
            if epsilon <= t <= 1 - epsilon and 0 <= u <= max_distance:
                self.bounce()
            else:
                pass

    def bounce(self):
        # The ball is going to bounce
        # Get the normal vector of the surface
        x1, x2, y1, y2 = self.closest_surface.start.p_x, self.closest_surface.end.p_x, self.closest_surface.start.p_y, self.closest_surface.end.p_y
        
        # Calculate the normal vector
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        nx = -dy / length
        ny = dx / length

        # Calculate the dot product of the velocity and the normal vector
        dot_product = (self._ball.v_x * nx + self._ball.v_y * ny)

        # Reflect the velocity vector off the surface
        self._ball.v_x -= 2 * dot_product * nx * self._bounce_factor_x
        self._ball.v_y -= 2 * dot_product * ny * self._bounce_factor_y

    def _init_ball(self):
        '''For testing purposes, the ball is initialized at the center of the screen.
        The ball is not moving at the start of the game.'''
        if type(self) != PhysicsModel:
            raise ValueError('Override this method!')
        self._ball = Ball(
            p_x=self._width//2, 
            p_y=self._height, 
            v_x=0, 
            v_y=0, 
            a_x=0, 
            a_y=0,
            r=5, 
            )
        
    def height_update(self):
        self.check_bounce()
        self._accelerate_x()
        self._accelerate_y()
        self._move_x()
        self._move_y()

    def _move_x(self):
        self._ball.p_x += self._ball.v_x

    def _move_y(self):
        self._ball.p_y += self._ball.v_y

    def _accelerate_x(self):
        self._ball.v_x += self._ball.a_x
    
    def _accelerate_y(self):
        self._ball.v_y += self._ball.a_y

    def _accelerate_m(self):
        self._ball.v_m += self._ball.a_m

    def accelerate_to_gravity(self):
        self._ball.a_y = self._gravity


    def jump(self):
        self._ball.v_y = -_Constants.JUMP_HEIGHT/self._fps

    def push_right(self):
        if self._ball.v_x < _Constants.SPEED_LIMIT_X/self._fps:
            self._ball.v_x += _Constants.SIDEWARD_PUSH_ACCELERATION/(self._fps**2)

    def push_left(self):
        if self._ball.v_x > -_Constants.SPEED_LIMIT_X/self._fps:
            self._ball.v_x -= _Constants.SIDEWARD_PUSH_ACCELERATION/(self._fps**2)

    def push_down(self):
        if self._ball.v_y < _Constants.SPEED_LIMIT_X/self._fps:
            self._ball.v_y += _Constants.SIDEWARD_PUSH_ACCELERATION/(self._fps**2)

    def push_up(self):
        if self._ball.v_y > -_Constants.SPEED_LIMIT_X/self._fps:
            self._ball.v_y -=_Constants.SIDEWARD_PUSH_ACCELERATION/(self._fps**2)
