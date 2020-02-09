from random import randrange

MAP_WIDTH = 800
MAP_HEIGHT = 800

def add_resources():
    randomx = randrange(MAP_WIDTH)
    randomy = randrange(MAP_HEIGHT)
    print("resource at: (" + str(randomx) + ", " + str(randomy) + ")")




add_resources()