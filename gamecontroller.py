from gamestate import GameState
import logging
import time, math
from gamestate import THE_GAMESTATE, Projectile
from clientmessages import KeyEventMessage, MouseEventMessage, Keys, Trigger

class Movement:
    def __init__(self, player, dx, dy):
        self.player = player
        self.dx = dx
        self.dy = dy

def update_game(game_updater_q):
    # Key = player ID
    # Value = Movement obj
    movements = {}
    while True:
        if not game_updater_q.empty():
            event, id = game_updater_q.get()
            if isinstance(event, KeyEventMessage):
                handleKeyPress(event, id, movements)
            elif isinstance(event, MouseEventMessage):
                handleMousePress(event, id)
        # Update player positions
        for id in movements.keys():
            movement = movements[id]
            player = movement.player
            player.x += movement.dx
            player.y += movement.dy
    
        time.sleep(.01)

def handleKeyPress(event, id, moving_players):
    if not id in moving_players.keys():
        move = Movement(THE_GAMESTATE.players[id], 0, 0)
    else:
        move = moving_players[id]
    if event.command is Keys.UP_PRESS:
        move.dy = -3
    elif event.command is Keys.DOWN_PRESS:
        move.dy = 3
    elif event.command is Keys.LEFT_PRESS:
        move.dx = -3
    elif event.command is Keys.RIGHT_PRESS:
        move.dx = 3
    elif event.command is Keys.UP_RELEASE or event.command is Keys.DOWN_RELEASE:
        move.dy = 0
    elif event.command is Keys.RIGHT_RELEASE or event.command is Keys.LEFT_RELEASE:
        move.dx = 0

    moving_players[id] = move

    # Remove non moving player from movements dictionary
    #if move.dx == 0 and move.dy == 0:
        #del moving_players[id]

def handleMousePress(event, id):
    player = THE_GAMESTATE.players[id]
    if not event.trigger is Trigger.PRESSED:
        return
    if (event.x - player.x) == 0:
        slope = event.y - player.y/1
    else:
        slope = (event.y - player.y)/(event.x - player.x)
    theta = math.atan(slope)
    if (event.x - player.x) < 0:
        theta += math.pi
    THE_GAMESTATE.projectiles.append(Projectile(id, player.x, player.y, theta))

