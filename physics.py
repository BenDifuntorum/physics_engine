from physics_types import Ball, Surface, Point, SurfaceType
from dataclasses import dataclass

@dataclass
class _Constants:
    """Constants for the physics model. Calculated against the fps of the game."""
    GRAVITY = 4000
    BOUNCE_FACTOR_X = 1
    BOUNCE_FACTOR_Y = 1
    FRICTIONAL_CONSTANT = 1
    SPEED_LIMIT_X = 540
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
            Surface(start=Point(0, height), end=Point(0, 0), surface_type=SurfaceType.IN)
            ]
        
        self._width = width
        self._height = height
        self._fps = fps
        self._init_ball()


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
            x1, x2, y1, y2 = surface.start.x, surface.end.x, surface.start.y, surface.end.y
            x3, y3 = self._ball.x, self._ball.y
            
            determinant: float = (y2 - y1)*x3 - (x2 - x1)*y3 + ((x2*y1) - (y2*x1))
            length: float = ((y2 - y1)**2 + (x2 - x1)**2) ** 0.5
            dist = determinant / length
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
        
    # @property
    # def ball_dist_from_next_surface_x(self):
    #     return min(
    #         self._ball.left-0, 
    #         self._width-self._ball.right)
    
    # @property
    # def ball_dist_from_next_surface_y(self):
    #     return min(
    #         self._ball.top-0, 
    #         self._height-self._ball.bottom)

    # @property
    # def ball_dist_from_next_surface(self):
    #     return min(
    #         self.ball_dist_from_next_surface_x,
    #         self.ball_dist_from_next_surface_y)


    def _init_ball(self):
        '''For testing purposes, the ball is initialized at the center of the screen.
        The ball is not moving at the start of the game.'''
        if type(self) != PhysicsModel:
            raise ValueError('Override this method!')
        self._ball = Ball(
            x=self._width//2, 
            y=self._height, 
            v_x=0, 
            v_y=0, 
            a_x=0, 
            a_y=0,
            radius=5, 
            )
        
    def _conf_adjust(self):
        pass
        # if self.ball_dist_from_next_surface < abs(self._ball.v_y) or self.ball_dist_from_next_surface < abs(self._ball.v_x):
        #     self._adjust()

    def _adjust(self):
        pass
        # match self.closest_surface:
        #     case SurfaceType.LEFT:
        #         self._ball.x = self._ball.radius 

        #     case SurfaceType.RIGHT:
        #         self._ball.x = self._width - self._ball.radius 

        #     case SurfaceType.TOP:
        #         self._ball.y = self._ball.radius 

        #     case SurfaceType.BOTTOM:
        #         self._ball.y = self._height - self._ball.radius 
    
        # if abs(self._ball.v_x) < 0.000001:
        #     self._ball.v_x = 0
        # if abs(self._ball.v_y) < 0.000001:
        #     self._ball.v_y = 0


    def height_update(self):
        # if self.ball_dist_from_next_surface < 0:
        #     self._bounce()
        self._accelerate_x()
        self._accelerate_y()
        self._move_x()
        self._move_y()

    def _move_x(self):
        self._ball.x += self._ball.v_x

    def _move_y(self):
        self._ball.y += self._ball.v_y

    # def _bounce_x(self, bounce_factor: float = 0):
    #     if bounce_factor == 0:
    #         bounce_factor = self._bounce_factor_x

    #     self._ball.v_x *= -bounce_factor
    #     self._ball.v_y *= self._frictional_constant

    # def _bounce_y(self, bounce_factor: float = 0):
    #     if bounce_factor == 0:
    #         bounce_factor = self._bounce_factor_y

    #     self._ball.v_y *= -bounce_factor
    #     self._ball.v_x *= self._frictional_constant

    def _accelerate_x(self):
        self._ball.v_x += self._ball.a_x
    
    def _accelerate_y(self):
        self._ball.v_y += self._ball.a_y

    def accelerate_to_gravity(self):
        self._ball.a_y = self._gravity

    # def _bounce(self):
    #     if self.ball_dist_from_next_surface < (self._ball.v_x**2 + self._ball.v_y**2)**0.5:
    #         self._bounce()
        
        
    #     self._conf_adjust()


    def jump(self):
        self._conf_adjust()
        
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
            self._ball.v_y -= _Constants.SIDEWARD_PUSH_ACCELERATION/(self._fps**2)