import pygame

from sprites import ImageSprite
from vectors import Vector3D
from utils import loadImage


class Floor:

    def __init__(self, scene, size):
        self.size = size
        self.scene = scene
        self.tiles = []

        self.color = (255, 255, 255)
        self.visible = False
        self.createTiles()
        self.setColor((200, 200, 200))

    def setTileImage(self, image):
        for y in range(0, self.size):
            for x in range(0, self.size):
                index = y * self.size + x
                self.tiles[index].setImage(image)

    def createTiles(self):
        self.tiles.clear()
        tile_image = loadImage("img/floor.png")
        for y in range(0, self.size):
            for x in range(0,self.size):
                tile = Tile(tile_image, x, y)
                tile.setLocation(Vector3D(x, y, 0))
                self.tiles.append(tile)

    def setColor(self, color):
        self.color = color
        for tile in self.tiles:
            tile.setColor(color)

    def getColor(self):
        return self.color

    def show(self):
        if not self.visible:
            self.visible = True
            for tile in self.tiles:
                self.scene.addSprite(tile)

    def hide(self):
        if self.visible:
            self.visible = False
            for tile in self.tiles:
                self.scene.removeSprite(tile)


class Tile(ImageSprite):

    def __init__(self, img, x=0, y=0):
        ImageSprite.__init__(self, img)
        self.original_image = img
        self.x = x
        self.y = y
        self.setLayer(0)

    def setColor(self, color):
        size = self.image.get_size()
        colored_image = pygame.Surface(size, pygame.SRCALPHA)
        colored_image.blit(self.original_image, (0,0))
        colored_image.fill(color, special_flags=pygame.BLEND_MULT)
        self.setImage(colored_image)
