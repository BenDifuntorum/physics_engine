import pyxel
from physics import PhysicsModel, Ball
import argparse


class TesterModel(PhysicsModel):
    def __init__(self, fps: int, width: int, height: int):
        super().__init__(fps, width, height)

        pyxel.init(width, height, fps=fps, title='PHYSICS ENGINE TESTER', quit_key=pyxel.KEY_Q)

    def _init_ball(self):
        '''For testing purposes, the ball is initialized at the center of the screen.
        The ball is not moving at the start of the game.'''
        if type(self) != PhysicsModel and type(self) != TesterModel:
            raise ValueError('Override this method!')
        self._ball = Ball(
            x=self._width//2, 
            y=self._height//2, 
            v_x=0, 
            v_y=0, 
            a_x=0, 
            a_y=0,
            radius=5, 
            )
        
    @property
    def fps(self):
        return self._fps

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height


class View:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
    
    def sample_bounce(self, circle: Ball):
        pyxel.cls(col=pyxel.COLOR_BLACK)
        pyxel.circ(x=circle.x, y=circle.y, r=circle.r, col=pyxel.COLOR_WHITE)


class Controller:
    def __init__(self, model: TesterModel, view: View):
        self._view = view
        self._model = model
        self._frame = 0
        self._count = 0


        pyxel.run(self.update, self.draw)

    def update(self):
        self._frame += 1
        
        self._model.height_update()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self._model.jump()
            
        if pyxel.btn(pyxel.KEY_D):
            self._model.push_right()

        if pyxel.btn(pyxel.KEY_A):
            self._model.push_left()
        
        if pyxel.btn(pyxel.KEY_S):
            self._model.push_down()

        if pyxel.btn(pyxel.KEY_W):
            self._model.push_up()
    
        if pyxel.btnp(pyxel.KEY_P):
            print(self._model.closest_surface)

        if pyxel.btnp(pyxel.KEY_H):
            print(self._model.ball_dist_from_every_surface)

        




        # if self._frame <= 10:
        #     print(f'v_y after {self._frame} frames: {self._model.ball.v_y}')
        
        # if self._frame == 11:
        #     print()
        
        
        # if self._frame % (self._model.fps // 2) == 0:
        #     self._count += 1
        #     print(f'Frame {self._count}:')
        #     print(f'x={self._model.ball.x}, y={self._model.ball.y}\nx_v={self._model.ball.v_x}, y_v={self._model.ball.v_y}\nx_a={self._model.ball.a_x}, y_a={self._model.ball.a_y}')


    def draw(self):
        self._view.sample_bounce(self._model.ball)


def init(fps: int, width: int, height: int):
    model = TesterModel(fps, width, height)
    view = View(width, height)
    controller = Controller(model, view)

    return controller


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Physics Engine Tester')
    parser.add_argument('--fps', type=int, default=60, help='Frames per second')
    parser.add_argument('--width', type=int, default=900, help='Width of the window')
    parser.add_argument('--height', type=int, default=900, help='Height of the window')
    args = parser.parse_args()
    init(args.fps, args.width, args.height)

            
        