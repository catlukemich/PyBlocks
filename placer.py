import pygame.draw

from block import Block, BlockDefinition, BlockPickResult, BlockSide, BlockHeading
from sprites import Sprite, ImageSprite, ImagePickResult
from vectors import Vector3D, Vector2D
from utils import loadImage
from input import MouseListener
from viewport import Rotation
from floor import Tile

class Placer(MouseListener):

    def __init__(self, input, world, viewport):
        self.input = input
        self.world = world
        self.scene = world.scene
        self.viewport = viewport
        self.enabled = False
        self.highlight = Highlight()
        self.rails = OrientationRails(world)
        path = "img/blocks/block.png"
        definition = BlockDefinition("Standard block", path, path, path, path)
        self.block = Block(Vector3D(0, 0, 0), BlockHeading.NORTH, definition) # The block that will be cloned at click
        self.block_preview = BlockPreview(self.block, self.scene)

    def setBlock(self, block):
        self.scene.removeSprite(self.block_preview)
        color = self.block.getColor()
        block.setColor(color)
        self.block = block
        self.block_preview.setBlock(block)
        self.scene.addSprite(self.block_preview)

    def setColor(self, color):
        self.block.setColor(color)

    def enable(self):
        self.input.addMouseListener(self)
        self.scene.addSprite(self.highlight)
        self.scene.addSprite(self.block_preview)

    def disable(self):
        self.input.removeMouseListener(self)
        self.scene.removeSprite(self.highlight)
        self.scene.removeSprite(self.block_preview)

    def mouseMotion(self, event):
        results = self.viewport.pickSprites(event.pos[0], event.pos[1])
        if len(results) == 0:
            self.highlight.hide()
            self.rails.setBlock(None)
        else:
            self.highlight.show()
            result = results[0]
            place, location = self.getBlockPlaceAndLocation(result)

            self.block_preview.setLocation(location)
            self.block_preview.setPlace(place)

            self.highlight.setSprite(result.sprite)
            if isinstance(result.sprite, Tile):
                self.highlight.setSide(BlockSide.TOP)
                self.rails.hide()
            elif isinstance(result.sprite, Block):
                self.highlight.setSide(result.side)
                self.rails.setBlock(self.block)
                self.rails.show()
                self.rails.reset()
                self.block_preview.show()
                self.block_preview.reset()
            return True
        return False

    def mouseLost(self, event):
        self.rails.hide()
        self.highlight.hide()
        self.block_preview.hide()

    def mouseGained(self, event):
        self.rails.show()
        self.highlight.show()
        self.block_preview.show()

    def mouseButtonDown(self, event):
        if event.button == 4:
            self.block_preview.rotateCW()
        if event.button == 5:
            self.block_preview.rotateCCW()

    def mouseClick(self, event):
        if event.button == 1:
            self.placeBlock(event)

        elif event.button == 3:
            self.removeBlock(event)

    def placeBlock(self, event):
        results = self.viewport.pickSprites(event.pos[0], event.pos[1])
        if len(results) == 0: return
        result = results[0]
        place, location = self.getBlockPlaceAndLocation(result)
        self.placeNewBlock(place, location)

    def getBlockPlaceAndLocation(self, result):
        if isinstance(result, BlockPickResult):
            side = result.side
            location = result.sprite.getLocation()
            old_place = result.sprite.place

            rotation = self.viewport.getRotation()
            rotation_type = rotation.type
            if rotation_type == Rotation.NORTH:
                if side == BlockSide.LEFT:
                    new_location = Vector3D(location.x, location.y + 1, location.z)
                    new_place = Vector3D(old_place.x, old_place.y + 1, old_place.z)
                elif side == BlockSide.RIGHT:
                    new_location = Vector3D(location.x + 1, location.y, location.z)
                    new_place = Vector3D(old_place.x + 1, old_place.y, old_place.z)

            if rotation_type == Rotation.SOUTH:
                if side == BlockSide.LEFT:
                    new_location = Vector3D(location.x, location.y - 1, location.z)
                    new_place = Vector3D(old_place.x, old_place.y - 1, old_place.z)
                elif side == BlockSide.RIGHT:
                    new_location = Vector3D(location.x - 1, location.y, location.z)
                    new_place = Vector3D(old_place.x - 1, old_place.y, old_place.z)

            if rotation_type == Rotation.EAST:
                if side == BlockSide.LEFT:
                    new_location = Vector3D(location.x + 1, location.y, location.z)
                    new_place = Vector3D(old_place.x + 1, old_place.y, old_place.z)
                elif side == BlockSide.RIGHT:
                    new_location = Vector3D(location.x, location.y - 1, location.z)
                    new_place = Vector3D(old_place.x, old_place.y - 1, old_place.z)

            if rotation_type == Rotation.WEST:
                if side == BlockSide.LEFT:
                    new_location = Vector3D(location.x - 1, location.y, location.z)
                    new_place = Vector3D(old_place.x - 1, old_place.y, old_place.z)
                elif side == BlockSide.RIGHT:
                    new_location = Vector3D(location.x, location.y + 1, location.z)
                    new_place = Vector3D(old_place.x, old_place.y + 1, old_place.z)

            if side == BlockSide.TOP:
                new_location = Vector3D(location.x, location.y, location.z + 1)
                new_place = Vector3D(old_place.x, old_place.y, old_place.z + 1)


        elif isinstance(result, ImagePickResult):
            location = result.sprite.getLocation()
            new_location = Vector3D(location.x, location.y, location.z + 0.5)
            new_place = Vector3D(location.x, location.y, 0)

        return new_place, new_location


    def placeNewBlock(self, place, location):
        old_block = self.world.getBlock(place.x, place.y, place.z)
        world_size = self.world.getSize()
        world_height = self.world.getHeight()
        is_in_world = \
            place.x < world_size and place.y < world_size and place.z < world_height and \
            place.x >= 0 and place.y >= 0 and place.z >= 0
        if old_block is None and is_in_world:
            new_block = self.block.clone()
            new_block.setPlace(place)
            new_location = Vector3D(location.x, location.y, location.z)
            new_block.setLocation(new_location)
            self.scene.addSprite(new_block)

            self.world.setBlock(place.x, place.y, place.z, new_block)

    def removeBlock(self, event):
        results = self.viewport.pickSprites(event.pos[0], event.pos[1])
        for result in results:
            if isinstance(result, BlockPickResult):
                block = result.sprite
                self.scene.removeSprite(block)
                place_x = block.place.x
                place_y = block.place.y
                place_z = block.place.z
                self.world.setBlock(place_x, place_y, place_z, None)
                break


    def update(self):
        pass


class BlockPreview(Sprite):

    def __init__(self, block, scene):
        Sprite.__init__(self)
        self.block = block
        self.scene = scene
        block.setLayer(3)
        self.time = 0
        self.visible = True
        self.setLayer(3)

    def show(self):
        self.scene.addSprite(self)

    def hide(self):
        self.scene.removeSprite(self)

    def reset(self):
        self.time = 0
        self.visible = True

    def setBlock(self, block):
        self.block = block
        block.setLayer(3)

    def setLocation(self, location):
        self.block.setLocation(location)

    def setPlace(self, place):
        self.block.setPlace(place)

    def rotateCW(self):
        self.block.rotateCW()

    def rotateCCW(self):
        self.block.rotateCCW()

    def getPick(self, viewport, mouse_x, mouse_y):
        return None

    def draw(self, viewport, screen):
        if self.visible:
            self.block.draw(viewport, screen)

    def update(self, clock):
        self.time += clock.get_time()
        if self.time > 300:
            self.visible = not self.visible
            self.time = 0



class Highlight(ImageSprite):

    def __init__(self):
        ImageSprite.__init__(self, loadImage("img/highlight_flat.png"))
        self.sprite = None
        self.side = BlockSide.TOP
        self.visible = False
        self.setLayer(2)

    def setSprite(self, sprite):
        self.sprite = sprite
        if isinstance(sprite, Tile):
            sprite_loc = sprite.getLocation()
            highlight_loc = Vector3D(sprite_loc.x, sprite_loc.y, sprite_loc.z - 0.5)
            self.setLocation(highlight_loc)
        if isinstance(sprite, Block):
            sprite_loc = sprite.getLocation()
            new_location = Vector3D(sprite_loc.x, sprite_loc.y, sprite_loc.z)
            self.setLocation(new_location)

    def setSide(self, side):
        if side == BlockSide.TOP:
            self.setImage(loadImage("img/highlight_flat.png"))
        if side == BlockSide.LEFT:
            self.setImage(loadImage("img/highlight_left.png"))
        if side == BlockSide.RIGHT:
            self.setImage(loadImage("img/highlight_right.png"))
        self.side = side

    def getSide(self):
        return self.side

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, viewport, screen):
        if self.visible:
            ImageSprite.draw(self, viewport, screen)

    def getPick(self, viewport, mouse_x, mouse_y):
        return None


class OrientationRails():

    def __init__(self, world):
        self.world = world
        self.scene = world.scene
        self.blocks = []
        self.block = None
        self.visible = True

    def reset(self):
        for block in self.blocks:
            block.reset()

    def setBlock(self, block):
        self.block = block
        self.realign()

    def realign(self):
        self.hide()
        self.show()

    def show(self):
        if self.visible: return
        if self.block is None: return
        self.visible = True
        self.showBlocks()

    def hide(self):
        if not self.visible: return
        self.visible = False
        self.hideBlocks()

    def showBlocks(self):
        num_blocks = self.block.place.z
        for i in range(0, num_blocks):
            own_block_place = self.block.getPlace()
            existing_block = self.world.getBlock(own_block_place.x, own_block_place.y, i)
            if existing_block is None:
                block = OrientationRailsBlock()
                self.blocks.append(block)
                own_block_loc = self.block.getLocation()
                block_loc = Vector3D(own_block_loc.x, own_block_loc.y, i + 0.5)
                block.setLocation(block_loc)

        for block in self.blocks:
            self.scene.addSprite(block)

    def hideBlocks(self):
        for block in self.blocks:
            self.scene.removeSprite(block)
        self.blocks.clear()



class OrientationRailsBlock(ImageSprite):

    def __init__(self):
        ImageSprite.__init__(self, loadImage("img/rail_block.png"))
        self.time = 0
        self.visible = True
        self.setLayer(1)

    def reset(self):
        self.visible = True
        self.time = 0

    def getPick(self, viewport, mouse_x, mouse_y):
        return None

    def update(self, clock):
        self.time += clock.get_time()
        if self.time > 300:
            self.visible = not self.visible
            self.time = 0

    def draw(self, viewport, screen):
        if self.visible:
            image = self.getImage()
            image.set_alpha(128)
            ImageSprite.draw(self, viewport, screen)
