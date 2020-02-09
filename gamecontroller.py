from gamestate import GameState
import logging
import time
from gamestate import THE_GAMESTATE
from clientmessages import KeyEventMessage, MouseEventMessage, Keys, ButtonState

def update_game(game_updater_q):
    while True:
        if not game_updater_q.empty():
            event, id = game_updater_q.get()
            player = THE_GAMESTATE.players[id]
            if isinstance(event, KeyEventMessage):
                handleKeyPress(event, id)
            elif isinstance(event, MouseEventMessage):
                pass
            player.y += player.y_delt
            player.x += player.x_delt


        time.sleep(.1)

def handleKeyPress(event, id):
    player = THE_GAMESTATE.players[id]
    if event.command is Keys.UP_PRESS:
        player.y_delt = -5
    elif event.command is Keys.DOWN_PRESS:
        player.y_delt = 5
    elif event.command is Keys.LEFT_PRESS:
        player.x_delt = -5
    elif event.command is Keys.LEFT_PRESS:
        player.x_delt = 5
    elif event.command is Keys.UP_RELEASE or event.command is Keys.DOWN_RELEASE:
        player.y_delt = 0
    elif event.command is Keys.RIGHT_RELEASE or event.command is Keys.LEFT_RELEASE:
        player.x_delt = 0