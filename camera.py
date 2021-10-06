import pygame as py
from settings import *

# collide function
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
# Map
class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename,'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE



# Camera Movement
class Camera:
    def __init__(self,width,height):
        self.camera = py.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def update(self,target):
        x =  -target.rect.x + int(WIDTH / 2)

        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT+19), y)  # bottom
        self.camera = py.Rect(x, y, self.width, self.height)