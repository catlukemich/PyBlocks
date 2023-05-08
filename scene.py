
class Scene:

    def __init__(self):
        self.sprites = []

    def update(self, clock):
        for sprite in self.sprites:
            sprite.update(clock)

    def addSprite(self, sprite):
        if not sprite in self.sprites:
            self.sprites.append(sprite)

    def removeSprite(self, sprite):
        try:
            self.sprites.remove(sprite)
        except ValueError:
            pass