from enum import Enum

class ConnectMessage:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class KeyEventMessage:
    def __init__(self, command, button_state):
        self.command = command
        self.button_state = button_state

class MouseEventMessage:
    def __init__(self, x, y, button_state):
        self.x = x
        self.y = y
        self.button_state = button_state

class Keys(Enum):
    UP_PRESS = 1
    DOWN_PRESS = 2
    LEFT_PRESS = 3
    RIGHT_PRESS = 4
    UP_RELEASE = 5
    DOWN_RELEASE = 6
    LEFT_RELEASE = 7
    RIGHT_RELEASE = 8


class Trigger(Enum):
    PRESSED = 1
    RELEASED = 2