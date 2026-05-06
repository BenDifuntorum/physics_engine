from __future__ import annotations
from pathlib import Path
import json

from controller import Controller
from model import Model
from view import View




CONSTANTS_FILE = Path(__file__).parent / 'constants.json'
CONSTANTS: dict[str, float] = json.loads(CONSTANTS_FILE.__str__())

model = Model(CONSTANTS)
view = View()
controller = Controller(model, view)