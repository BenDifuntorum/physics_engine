from physics_types import Ball, Surface
from dataclasses import dataclass

@dataclass
class Constants:
    """Constants for the physics model. Calculated against the fps of the game."""
    GRAVITY = 4000
    BOUNCE_FACTOR_X = 1
    BOUNCE_FACTOR_Y = 0.87
    FRICTIONAL_CONSTANT = 0.95
    SPEED_LIMIT_X = 540
    JUMP_HEIGHT = 1100
    SIDEWARD_PUSH_ACCELERATION = 2100


class PhysicsModel:
    def __init__(self, fps: int, width: int, height: int):
        self._gravity = Constants.GRAVITY / fps**2
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
    def closest_surface(self) -> Surface:
        dist = self.ball_dist_from_next_surface
        
        if dist == self._ball.left-0:
            return Surface.LEFT

        elif dist == self._width-self._ball.right:
            return Surface.RIGHT

        elif dist == self._ball.top-0:
            return Surface.TOP

        else:
            assert dist == self._height-self._ball.bottom
            return Surface.BOTTOM

    @property
    def ball_dist_from_next_surface(self):
        return min(
            self._ball.left-0, 
            self._width-self._ball.right, 
            self._ball.top-0, 
            self._height-self._ball.bottom)


    def _init_ball(self):
        '''For testing purposes, the ball is initialized at the center of the screen.
        The ball is not moving at the start of the game.'''
        self._ball = Ball(
            x=self._width//2, 
            y=self._height//2, 
            v_x=0, 
            v_y=0, 
            a_x=0, 
            a_y=self._gravity,
            radius=5, 
            )
        
    def _conf_adjust(self):
        if self.ball_dist_from_next_surface < abs(self._ball.v_y) or self.ball_dist_from_next_surface < abs(self._ball.v_x):
            self._adjust()

    def _adjust(self):
        match self.closest_surface:
            case Surface.LEFT:
                self._ball.x = self._ball.radius 

            case Surface.RIGHT:
                self._ball.x = self._width - self._ball.radius 

            case Surface.TOP:
                self._ball.y = self._ball.radius 

            case Surface.BOTTOM:
                self._ball.y = self._height - self._ball.radius 

        if abs(self._ball.v_x) < 0.000001:
            self._ball.v_x = 0
        if abs(self._ball.v_y) < 0.000001:
            self._ball.v_y = 0


    def height_update(self):
        if self.ball_dist_from_next_surface < 0:
            self._bounce()
        self._accelerate_x()
        self._accelerate_y()
        self._move_x()
        self._move_y()

    def _move_x(self):
        self._ball.x += self._ball.v_x

    def _move_y(self):
        self._ball.y += self._ball.v_y

    def _bounce_x(self, bounce_factor: float = Constants.BOUNCE_FACTOR_X):
        self._ball.v_x *= -bounce_factor
        self._ball.v_y *= Constants.FRICTIONAL_CONSTANT

    def _bounce_y(self, bounce_factor: float = Constants.BOUNCE_FACTOR_Y):
        self._ball.v_y *= -bounce_factor
        self._ball.v_x *= Constants.FRICTIONAL_CONSTANT

    def _accelerate_x(self):
        self._ball.v_x += self._ball.a_x
    
    def _accelerate_y(self):
        self._ball.v_y += self._ball.a_y

    def accelerate_to_gravity(self):
        self._ball.a_y = self._gravity

    def _bounce(self):
        if self.closest_surface in (Surface.TOP, Surface.BOTTOM):
            self._bounce_y()
        
        else:
            assert self.closest_surface in (Surface.LEFT, Surface.RIGHT)
            self._bounce_x()
        
        self._conf_adjust()



    def jump(self):
        self._conf_adjust()
        
        self._ball.v_y = -Constants.JUMP_HEIGHT/self._fps



    def push_right(self):
        if self._ball.v_x < Constants.SPEED_LIMIT_X/self._fps:
            self._ball.v_x += Constants.SIDEWARD_PUSH_ACCELERATION/(self._fps**2)

    def push_left(self):
        if self._ball.v_x > -Constants.SPEED_LIMIT_X/self._fps:
            self._ball.v_x -= Constants.SIDEWARD_PUSH_ACCELERATION/(self._fps**2)