
from physics import PhysicsModel, Ball
import pyxel
import argparse

from physics_types import Surface


class TesterModel(PhysicsModel):
    def __init__(self, fps: int, width: int, height: int):
        super().__init__(fps, width, height)

        pyxel.init(width, height, fps=fps, title='PHYSICS ENGINE TESTER', quit_key=pyxel.KEY_Q)

    def _init_ball(self):
        self._ball = Ball.from_bearing(
            p_x=self._width//2, 
            p_y=self._height//2, 
            v_m=0, 
            v_d=0, 
            a_m=0, 
            a_d=0,
            r=5, 
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
    
    def show_screen(self, circle: Ball, platforms: list[Surface]):
        pyxel.cls(col=pyxel.COLOR_BLACK)
        pyxel.circ(x=circle.p_x, y=circle.p_y, r=circle.r, col=pyxel.COLOR_WHITE)
        for platform in platforms:
            pyxel.line(x1=platform.start.p_x, x2=platform.end.p_x, y1=platform.start.p_y, y2=platform.end.p_y, col=pyxel.COLOR_RED)

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
            print(self._model.closest_surface, self._model.ball_dist_from_next_surface)

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
        self._view.show_screen(self._model.ball, self._model.surfaces)


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

            
        