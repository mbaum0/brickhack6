import pygame as pg
from gamesettings import *

class MakeSprites:
    def __init__(self, gamestate, ID):
        self.all_sprites = pg.sprite.Group()

        # create walls
        self.walls = pg.sprite.Group()

        for wall in gamestate.walls:
            WallSprite(self, wall.x, wall.y)

        # create players from GameState file
        self.players = pg.sprite.Group()

        players = gamestate.players

        for pId in players.keys():
            PlayerSprite(self, pId, players[pId])

        self.player = PlayerSprite(self, ID, gamestate.players[ID])
        self.player.image.fill(BLUE)

        self.projectiles = pg.sprite.Group()

        for proj in gamestate.projectiles:
            ProjectileSprite(self, proj)


class PlayerSprite(pg.sprite.Sprite):
    def __init__(self, spriteList, clientID, player):
        self.groups = spriteList.all_sprites, spriteList.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.spriteList = spriteList
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = player.x
        self.rect.y = player.y
        self.x = player.x
        self.y = player.y
        self.name = player.name
        self.clientID = clientID
        self.health = player.health
        self.resources = player.resources
        self.hasSnitch = player.hasSnitch

class WallSprite(pg.sprite.Sprite):
    def __init__(self, spriteList, x, y):

        self.spriteList = spriteList
        self.groups = spriteList.all_sprites, spriteList.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x_tile = x
        self.y_tile = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class ProjectileSprite(pg.sprite.Sprite):
    def __init__(self, spriteList, projectile):

        self.spriteList = spriteList
        self.groups = spriteList.all_sprites, spriteList.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.clientID = projectile.clientID
        self.x_tile = projectile.x
        self.y_tile = projectile.y
        self.rect.x = projectile.x * PROJECTILESIZE
        self.rect.y = projectile.y * PROJECTILESIZE