from floor import Floor
from utils import loadImage


class World:

    def __init__(self, scene, size, height):
        self.scene = scene
        self.size = size
        self.height = height

        self.sky_color = (200,200,200)
        self.blocks = None
        self.clearBlocks()

        self.floor = Floor(scene, size)

    def getSize(self):
        return self.size

    def getHeight(self):
        return self.height

    def setSkyColor(self, color):
        self.sky_color = color

    def getSkyColor(self):
        return self.sky_color

    def show(self):
        self.floor.show()

    def getBlock(self, x, y, z):
        try:
            return self.blocks[x][y][z]
        except IndexError:
            return None

    def setBlock(self, x, y, z, block):
        if x < self.size and y < self.size and z < self.height:
            self.blocks[x][y][z] = block

    def getBlocks(self):
        return self.blocks

    def clearBlocks(self):
        size = self.size
        height = self.height
        blocks = []
        for x in range(0, size):
            blocks.append([])
            for y in range(0, size):
                blocks[x].append([])
                for z in range(0, height):
                    blocks[x][y].append(None)

        self.blocks = blocks