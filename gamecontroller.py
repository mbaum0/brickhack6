
import logging
import time, math, pygame as pg
from gamestate import THE_GAMESTATE, Projectile, Resource
from random import randrange
from gamesettings import *
from clientmessages import KeyEventMessage, MouseEventMessage, Keys, Trigger

clock = pg.time.Clock()


"""
    This class is used specifically to track a players delta movements
"""
class Movement:
    def __init__(self, player, dx, dy):
        self.player = player
        self.dx = dx
        self.dy = dy

"""
    This function handles events issued from the users. These include both key and mouse inputs. Also, each player's
    positions are updated who's deltas are non-zero. 
    
    @:param game_updater_q: a queue of game events
"""
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
        update_projectiles()
        add_resources()
        time.sleep(.01)

def add_resources():
    # TODO: Add delay to resource repopulate
    if len(THE_GAMESTATE.resources) < MAX_RESOURCES:
        randomx = randrange(WIDTH)
        randomy = randrange(HEIGHT)
        THE_GAMESTATE.resources.append(Resource(1, randomx, randomy, 1))

def update_projectiles():
    bullets = THE_GAMESTATE.projectiles
    for bullet in bullets:
        if bullet.frames > 0:
            bullet.x += int(bullet.vel * math.cos(bullet.angle))
            bullet.y += int(bullet.vel * math.sin(bullet.angle))
            bullet.frames -= 1
        else:
            bullets.pop(bullets.index(bullet))


"""
    This function handles all keyboard input from the user. When a movement key is pressed, the delta parameter of
    the player is updated. This is done as opposed to directly updating the player position in order to easily
    handle a player holding down an input key and not doing unnecessary processing.
    
    @:param event           : the player input event of class KeyEventMessage from clientmessages.py
    @:param id              : the server id of the player who issued the event
    @:param moving_players  : a dictionary containing a all of the players with non-zero delta positions
"""
def handleKeyPress(event, id, moving_players):
    if not id in moving_players.keys():
        move = Movement(THE_GAMESTATE.players[id], 0, 0)
    else:
        move = moving_players[id]
    if event.command is Keys.UP_PRESS:
        move.dy = -1.5
    elif event.command is Keys.DOWN_PRESS:
        move.dy = 1.5
    elif event.command is Keys.LEFT_PRESS:
        move.dx = -1.5
    elif event.command is Keys.RIGHT_PRESS:
        move.dx = 1.5
    elif event.command is Keys.UP_RELEASE or event.command is Keys.DOWN_RELEASE:
        move.dy = 0
    elif event.command is Keys.RIGHT_RELEASE or event.command is Keys.LEFT_RELEASE:
        move.dx = 0

    moving_players[id] = move

    # Remove non moving player from movements dictionary
    #if move.dx == 0 and move.dy == 0:
        #del moving_players[id]


"""
    This function handles all mouse click input from the user. When a mouse click event is received, calculate the 
    direction to which a projectile will be fired, and add a projectile 

    @:param     event   : the player input event of class MouseEventMessage from clientmessages.py
    @:param     id      : the server id of the player who issued the event
"""
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

