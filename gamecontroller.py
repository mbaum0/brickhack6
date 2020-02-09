from gamestate import GameState
import logging
import time
from gamestate import THE_GAMESTATE

def update_game(game_updater_q):
    while True:
        if not game_updater_q.empty():
            event, id = game_updater_q.get()

        time.sleep(.1)

