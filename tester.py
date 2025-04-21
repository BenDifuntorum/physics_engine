import pyxel
from physics import PhysicsModel, Ball
import argparse


class Model(PhysicsModel):
    def __init__(self, fps: int, width: int, height: int):
        super().__init__(fps, width, height)

        pyxel.init(width, height, fps=fps, title='PHYSICS ENGINE TESTER', quit_key=pyxel.KEY_Q)

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
        pyxel.circ(x=circle.x, y=circle.y, r=circle.radius, col=pyxel.COLOR_WHITE)


class Controller:
    def __init__(self, model: Model, view: View):
        self._view = view
        self._model = model
        self._frame = 0
        self._count = 0


        pyxel.run(self.update, self.draw)

    def update(self):
        self._frame += 1
        
        self._model.height_update()
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            # print(f"Before jump: v_y = {self._model.ball.v_y}")  # Debugging
            self._model.jump()
            # print(f"After jump: v_y = {self._model.ball.v_y}")  # Debugging   
            # print(f'Gravity: {self._model._gravity}')
            
            # self._frame = 0

        if pyxel.btn(pyxel.KEY_D):
            self._model.push_right()

        if pyxel.btn(pyxel.KEY_A):
            self._model.push_left()
        
        # if self._frame <= 10:
        #     print(f'v_y after {self._frame} frames: {self._model.ball.v_y}')
        
        # if self._frame == 11:
        #     print()
        
        
        if self._frame % (self._model.fps // 2) == 0:
            self._count += 1
            print(f'Frame {self._count}:')
            print(f'x={self._model.ball.x}, y={self._model.ball.y}\nx_v={self._model.ball.v_x}, y_v={self._model.ball.v_y}\nx_a={self._model.ball.a_x}, y_a={self._model.ball.a_y}')


    def draw(self):
        self._view.sample_bounce(self._model.ball)


def init(fps: int, width: int, height: int):
    model = Model(fps, width, height)
    view = View(width, height)
    controller = Controller(model, view)

    return controller


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Physics Engine Tester')
    parser.add_argument('--fps', type=int, default=60, help='Frames per second')
    parser.add_argument('--width', type=int, default=450, help='Width of the window')
    parser.add_argument('--height', type=int, default=450, help='Height of the window')
    args = parser.parse_args()
    init(args.fps, args.width, args.height)

            
        