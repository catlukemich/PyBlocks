from functools import cmp_to_key
from vectors import Vector2D, Vector3D

TILE_WIDTH = 64
TILE_HEIGHT = 32
V_STEP = 40

class Viewport():

    def __init__(self, screen, scene):
        self.screen = screen
        self.scene  = scene
        self.rotation = RotationNorth()
        self.center = Vector3D()

    def getCenter(self):
        return self.center

    def setCenter(self, center):
        self.center = center

    def getRotation(self):
        return self.rotation

    def rotateCW(self):
        self.rotation = self.rotation.getRotatedCW()

    def rotateCCW(self):
        self.rotation = self.rotation.getRotatedCCW()

    def project(self, location):
        return self.rotation.project(self, location)

    def draw(self):
        self.scene.sprites.sort(key=cmp_to_key(self.compareSprites))
        for sprite in self.scene.sprites:
            sprite.draw(self, self.screen)

    # Sort the layers:
    def compareSprites(self, sprite1, sprite2):
        return self.rotation.compareSprites(sprite1, sprite2)


    def pickSprites(self, mouse_x, mouse_y):
        results = []

        for sprite in self.scene.sprites:
            pick = sprite.getPick(self, mouse_x, mouse_y)
            if pick is not None:
                results.append(pick)

        results.reverse()
        return results


class Rotation:

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def project(self, location):
        return Vector2D()

    def compareSprites(self, sprite1, sprite2):
        return 0

    def getRotatedCW(self):
        pass

    def getRotatedCCW(self):
        pass


class RotationNorth(Rotation):

    def __init__(self):
        self.type = Rotation.NORTH

    def project(self, viewport, location):
        ''' Project from world location to world position '''
        center = viewport.center
        x = (location.x - location.y - center.x + center.y) * (TILE_WIDTH / 2)
        y = (location.x + location.y - center.x - center.y) * (TILE_HEIGHT / 2) + (center.z - location.z) * V_STEP
        (w, h) = viewport.screen.get_size()
        projected = Vector2D(x + w / 2, y + h / 2);

        return projected

    def compareSprites(self, sprite1, sprite2):
        layer1 = sprite1.layer
        layer2 = sprite2.layer

        if layer1 != layer2:
            return layer1 - layer2

        loc1 = sprite1.getLocation()
        loc2 = sprite2.getLocation()
        sum1 = loc1.x + loc1.y + loc1.z
        sum2 = loc2.x + loc2.y + loc2.z
        if sum1 > sum2:
            return 1
        else:
            return -1

    def getRotatedCW(self):
        return RotationEast()

    def getRotatedCCW(self):
        return RotationWest()


class RotationSouth(Rotation):

    def __init__(self):
        self.type = Rotation.SOUTH

    def project(self, viewport, location):
        ''' Project from world location to world position '''
        center = viewport.center
        x = (-location.x + location.y + center.x - center.y) * (TILE_WIDTH / 2)
        y = (-location.x - location.y + center.x + center.y) * (TILE_HEIGHT / 2) + (center.z - location.z) * V_STEP
        (w, h) = viewport.screen.get_size()
        projected = Vector2D(x + w / 2, y + h / 2);

        return projected

    def compareSprites(self, sprite1, sprite2):
        layer1 = sprite1.layer
        layer2 = sprite2.layer

        if layer1 != layer2:
            return layer1 - layer2

        loc1 = sprite1.getLocation()
        loc2 = sprite2.getLocation()
        sum1 = -loc1.x - loc1.y + loc1.z
        sum2 = -loc2.x - loc2.y + loc2.z
        if sum1 > sum2:
            return 1
        else:
            return -1

    def getRotatedCW(self):
        return RotationWest()

    def getRotatedCCW(self):
        return RotationEast()


class RotationEast(Rotation):

    def __init__(self):
        self.type = Rotation.EAST

    def project(self, viewport, location):
        ''' Project from world location to world position '''
        center = viewport.center
        x = (-location.y - location.x + center.y + center.x) * (TILE_WIDTH / 2)
        y = (-location.y + location.x + center.y - center.x) * (TILE_HEIGHT / 2) + (center.z - location.z) * V_STEP
        (w, h) = viewport.screen.get_size()
        projected = Vector2D(x + w / 2, y + h / 2);

        return projected

    def compareSprites(self, sprite1, sprite2):
        layer1 = sprite1.layer
        layer2 = sprite2.layer

        if layer1 != layer2:
            return layer1 - layer2

        loc1 = sprite1.getLocation()
        loc2 = sprite2.getLocation()
        sum1 = -loc1.y + loc1.x + loc1.z
        sum2 = -loc2.y + loc2.x + loc2.z
        if sum1 > sum2:
            return 1
        else:
            return -1

    def getRotatedCW(self):
        return RotationSouth()

    def getRotatedCCW(self):
        return RotationNorth()


class RotationWest(Rotation):

    def __init__(self):
        self.type = Rotation.WEST

    def project(self, viewport, location):
        ''' Project from world location to world position '''
        center = viewport.center
        x = (location.y + location.x - center.y - center.x) * (TILE_WIDTH / 2)
        y = (location.y - location.x - center.y + center.x) * (TILE_HEIGHT / 2) + (center.z - location.z) * V_STEP
        (w, h) = viewport.screen.get_size()
        projected = Vector2D(x + w / 2, y + h / 2);

        return projected

    def compareSprites(self, sprite1, sprite2):
        layer1 = sprite1.layer
        layer2 = sprite2.layer

        if layer1 != layer2:
            return layer1 - layer2

        loc1 = sprite1.getLocation()
        loc2 = sprite2.getLocation()
        sum1 = loc1.y - loc1.x + loc1.z
        sum2 = loc2.y - loc2.x + loc2.z
        if sum1 > sum2:
            return 1
        else:
            return -1

    def getRotatedCW(self):
        return RotationNorth()

    def getRotatedCCW(self):
        return RotationSouth()