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