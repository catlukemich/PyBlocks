from vectors import Vector2D, Vector3D


class Sprite:

    def __init__(self):
        self.location = Vector3D()  # Location of the sprite in isometric 3d world coordinates
        self.scene = None
        self.parent = None
        self.layer = 0

    def update(self, clock):
        pass

    def draw(self, viewport, screen):
        pass

    def setLayer(self, layer):
        self.layer = layer

    def getLayer(self):
        return self.layer

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

    def getPick(self, viewport, mouse_x, mouse_y):
        pass


class ImageSprite(Sprite):

    def __init__(self, image=None):
        super().__init__()
        self.image = image  # The image to render this sprite

    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def draw(self, viewport, screen):
        location = self.getLocation()
        position = viewport.project(location)
        (w, h) = self.image.get_size()
        screen.blit(self.image, (position.x - w / 2, position.y - h / 2))

    def getPick(self, viewport, mouse_x, mouse_y):
        location = self.getLocation()
        position = viewport.project(location)
        (w, h) = self.image.get_size()

        top_left = Vector2D(position.x - w / 2, position.y - h / 2)
        bottom_right = Vector2D(position.x + w / 2, position.y + h / 2)
        mouse = Vector2D(mouse_x, mouse_y)

        if mouse > top_left and mouse < bottom_right:

            mouse_relative = mouse - top_left
            color = self.image.get_at((int(mouse_relative.x), int(mouse_relative.y)))
            if color.a == 0:
                return None
            else:
                return ImagePickResult(self)
        else:
            return None


class ImagePickResult:

    def __init__(self, sprite):
        self.sprite = sprite


