import uuid
import random
import pygame
from gamesettings import *

class GameState:
    def __init__(self, fps, height, width, startHealth, startResources):
        self.fps = fps
        self.height = height
        self.width = width
        self.startHealth = startHealth
        self.startResources = startResources
        self.players = {}
        self.bases = []
        self.resources = []
        self.projectiles = []
        self.walls = []

    def newPlayer(self, name):
        locationX = random.randrange(0, self.width)
        locationY = random.randrange(0, self.height)
        new_id = str(uuid.uuid4())
        tempPlayer = Player(name, new_id, locationX, locationY, self.startHealth, self.startResources, False)
        self.players[new_id] = tempPlayer
        return new_id

    def remove_player(self, id):
        del self.players[id]

    def createBoundWalls(self):
        topWall = Wall(0, 0, self.width, 0)
        botWall = Wall(0, self.height, self.width, self.height)
        rightWall = Wall(0, 0, 0, self.height)
        leftWall = Wall(self.width, 0, self.width, self.height)

        self.walls.append(topWall)
        self.walls.append(botWall)
        self.walls.append(rightWall)
        self.walls.append(leftWall)

class Player:
    def __init__(self, name, clientID, x, y, health, resources, hasSnitch):
        self.name = name
        self.clientID = clientID
        self.x = x
        self.y = y
        self.x_delt = 0
        self.y_delt = 0
        self.health = 100
        self.resources = resources
        self.hasSnitch = hasSnitch


class Base:
    def __init__(self, clientID, level, resources, x, y, health):
        self.clientID = -1
        self.level = 0
        self.resources = 0
        self.x = x
        self.y = y
        self.health = 100


class Resource:
    def __init__(self, resourceID, x, y, value):
        self.resourceID = -1
        self.x = 0
        self.y = 0
        self.value = 0


class Projectile:
    def __init__(self, clientID, x, y, angle):
        self.clientID = -1
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = 1
        self.vel = 10


class Wall:
    def __init__(self, startX, startY, endX, endY):
        self.startX = 0
        self.startY = 0
        self.endX = 0
        self.endY = 0


class Snitch:
    def __init__(self, x, y, visible):
        self.x = 0
        self.y = 0
        self.visible = False


THE_GAMESTATE = GameState(.1, WIDTH, HEIGHT, 10, 1000)
