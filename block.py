import pygame

from sprites import ImageSprite, ImagePickResult
from utils import loadImage
from vectors import Vector3D


block_images_cache = {}


class Block(ImageSprite):

    def __init__(self, place, heading, block_defintion):
        ImageSprite.__init__(self, block_defintion.image_north)
        self.place = place
        self.heading = heading
        self.original_images = []
        self.colored_images = []
        self.definition = block_defintion
        self.imagesFromDefinition(block_defintion)
        self.color = (255, 255, 255)
        self.setLayer(1)

    def imagesFromDefinition(self, definition):
        self.original_images = [definition.image_north, definition.image_south, definition.image_west, definition.image_east]
        self.colored_images = [definition.image_north, definition.image_south, definition.image_west, definition.image_east]

    def draw(self, viewport, screen):
        old_img = self.getImage()

        target_image = self.getTargetImage(viewport)
        self.setImage(target_image)
        ImageSprite.draw(self, viewport, screen)

        self.setImage(old_img)

    def getTargetImage(self, viewport):
        rotation = viewport.getRotation()
        rotation_idx = rotation.type
        heading = self.heading

        images = [self.colored_images[0], self.colored_images[3], self.colored_images[1], self.colored_images[2]]
        image_idx = (heading + rotation_idx) % len(images)
        target_image = images[image_idx]
        return target_image

    def getHeading(self):
        return self.heading

    def setHeading(self, heading):
        self.heading = heading

    def getDefinition(self):
        return self.definition

    def setPlace(self, place):
        self.place = place

    def getPlace(self):
        return self.place

    def setColor(self, color):
        self.color = color
        self.recolorSelf()

    def getColor(self):
        return self.color

    def recolorSelf(self):
        cache = block_images_cache
        hashed_color = hash(self.color)
        if self.definition.name in cache and hashed_color in cache[self.definition.name]:
            images_by_name = cache[self.definition.name]
            if hashed_color in images_by_name:
                images_list = images_by_name[hashed_color]
                self.colored_images = images_list
        else:
            images_list = []
            for index in range(0,4):
                original_image = self.original_images[index]
                size = original_image.get_size()
                colored_image = pygame.Surface(size, pygame.SRCALPHA)
                colored_image.blit(original_image, (0, 0))
                colored_image.fill(self.color, special_flags=pygame.BLEND_MULT)
                images_list.append(colored_image)
            self.colored_images = images_list
            if not self.definition.name in cache:
                cache[self.definition.name] = {}
            cache[self.definition.name][hashed_color] = images_list

    def rotateCW(self):
        self.heading += 1
        self.heading %= 4

    def rotateCCW(self):
        self.heading -= 1
        self.heading %= 4

    def getPick(self, viewport, mouse_x, mouse_y):
        old_img = self.getImage()
        block_image = loadImage("img/blocks/block.png")
        self.setImage(block_image)
        image_pick = ImageSprite.getPick(self, viewport, mouse_x, mouse_y)
        if image_pick is None:
            self.setImage(old_img)
            return None

        block_pick = BlockPickResult(self)
        side_pick = None

        self.setImage(loadImage("img/block_left.png"))
        pick = ImageSprite.getPick(self, viewport, mouse_x, mouse_y)
        if pick is not None:
            block_pick.setSide(BlockSide.LEFT)
            side_pick = block_pick

        self.setImage(loadImage("img/block_right.png"))
        pick = ImageSprite.getPick(self, viewport, mouse_x, mouse_y)
        if pick is not None:
            block_pick.setSide(BlockSide.RIGHT)
            side_pick = block_pick

        self.setImage(loadImage("img/block_top.png"))
        pick = ImageSprite.getPick(self, viewport, mouse_x, mouse_y)
        if pick is not None:
            block_pick.setSide(BlockSide.TOP)
            side_pick = block_pick

        self.setImage(old_img)
        return side_pick

    def clone(self):
        return_block = Block(self.place, self.heading, self.definition)
        return_block.setColor(self.color)
        return return_block


class BlockHeading:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class BlockDefinition:

    def __init__(self, name,  path_north, path_south, path_west, path_east):
        self.name = name
        self.path_north = path_north
        self.path_south = path_south
        self.path_west = path_west
        self.path_east = path_east
        self.image_north = loadImage(path_north)
        self.image_south = loadImage(path_south)
        self.image_west = loadImage(path_west)
        self.image_east = loadImage(path_east)


block_definitions_cache = {}

class BlockDefinitionFactory:

    def getDefinition(self, name):
        if name in block_definitions_cache:
            return block_definitions_cache[name]

        definition = None
        if name == "Standard block":
            path = "img/blocks/block.png"
            definition = BlockDefinition(name, path, path, path, path)

        if name == "Cylinder block":
            path = "img/blocks/cylinder.png"
            definition = BlockDefinition(name, path, path, path, path)

        if name == "Cone block":
            path = "img/blocks/cone.png"
            definition = BlockDefinition(name, path, path, path, path)

        if name == "Slope block":
            path_north = "img/blocks/slope_north.png"
            path_south = "img/blocks/slope_south.png"
            path_west = "img/blocks/slope_west.png"
            path_east = "img/blocks/slope_east.png"
            definition = BlockDefinition(name, path_north, path_south, path_west, path_east)

        if name == "Corner block":
            path_north = "img/blocks/corner_north.png"
            path_south = "img/blocks/corner_south.png"
            path_west  = "img/blocks/corner_west.png"
            path_east  = "img/blocks/corner_east.png"
            definition = BlockDefinition(name, path_north, path_south, path_west, path_east)

        if name == "Portal block":
            path_north = "img/blocks/portal_north.png"
            path_south = "img/blocks/portal_south.png"
            path_west  = "img/blocks/portal_west.png"
            path_east  = "img/blocks/portal_east.png"
            definition = BlockDefinition(name, path_north, path_south, path_west, path_east)

        self.cacheDefinition(name, definition)
        return definition

    def cacheDefinition(self, name, definition):
        block_definitions_cache[name] = definition


class BlockPickResult(ImagePickResult):

    def __init__(self, sprite):
        ImagePickResult.__init__(self, sprite)
        self.side = None

    def setSide(self, side):
        self.side = side


class BlockSide:
    LEFT = 0
    RIGHT = 1
    TOP = 2