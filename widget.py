import pygame.draw

from vectors import Vector2D
from utils import loadFont


class Widget:

    def __init__(self):
        self.position = Vector2D()
        self.dimensions = Vector2D()
        self.listeners = []

    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position

    def setDimensions(self, dimensions):
        self.dimensions = dimensions

    def getDimensions(self):
        return self.dimensions

    def addListener(self, listener):
        self.listeners.append(listener)

    def removeListener(self, listener):
        self.listeners.remove(listener)

    def mousePress(self, event):
        for listener in self.listeners:
            listener.onWidgetMousePress(self, event)

    def mouseRelease(self, event):
        for listener in self.listeners:
            listener.onWidgetMouseRelease(self, event)

    def mouseClick(self, event):
        for listener in self.listeners:
            listener.onWidgetClick(self, event)

    def mouseOver(self, event):
        for listener in self.listeners:
            listener.onWidgetMouseOver(self, event)

    def mouseOut(self, event):
        for listener in self.listeners:
            listener.onWidgetMouseOut(self, event)

    def containsPoint(self, point_x, point_y):
        if point_x > self.position.x and point_x < self.position.x + self.dimensions.x and \
            point_y > self.position.y and point_y < self.position.y + self.dimensions.y:
            return True
        else:
            return False


class WidgetListener:

    def onWidgetClick(self, widget, event):
        pass

    def onWidgetMouseOver(self, widget, event):
        pass

    def onWidgetMouseOut(self, widget, event):
        pass

    def onWidgetMousePress(self, widget, event):
        pass

    def onWidgetMouseRelease(self, widget, event):
        pass


class Box(Widget):

    def __init__(self, color):
        Widget.__init__(self)
        self.color = color
        self.surface = None

    def setDimensions(self, dimensions):
        Widget.setDimensions(self, dimensions)
        self.updateSurface()

    def updateSurface(self):
        surface = pygame.Surface((self.dimensions.x, self.dimensions.y), pygame.SRCALPHA)
        surface.fill(self.color)
        self.surface = surface

    def draw(self, screen):
        screen.blit(self.surface, (self.position.x, self.position.y))


class Button(Widget):

    def __init__(self, image):
        Widget.__init__(self)
        self.image = image
        w, h = image.get_size()
        self.dimensions.x = w
        self.dimensions.y = h
        self.has_hover = False
        self.is_mouse_pressed = False
        self.has_hover = False

    def mouseOver(self, event):
        self.has_hover = True

    def mouseOut(self, event):
        self.has_hover = False
        self.is_mouse_pressed = False

    def mousePress(self, event):
        self.is_mouse_pressed = True

    def mouseRelease(self, event):
        self.is_mouse_pressed = False

    def draw(self, screen):
        if self.has_hover:
            if self.is_mouse_pressed:
                pygame.draw.rect(screen, (255,0,0), (self.position.x, self.position.y, self.dimensions.x, self.dimensions.y))
            else:
                pygame.draw.rect(screen, (255,255,255), (self.position.x, self.position.y, self.dimensions.x, self.dimensions.y))
        screen.blit(self.image, (self.position.x, self.position.y))


class BlockButton(Button):

    def __init__(self, image):
        Button.__init__(self, image)
        self.original_image = image

    def tint(self, color):
        size = self.original_image.get_size()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.blit(self.original_image, (0,0))
        self.image.fill(color, special_flags = pygame.BLEND_MULT)


class ColorButton(Widget):

    def __init__(self, color = (255,255,255)):
        Widget.__init__(self)
        self.color = color
        self.setDimensions(Vector2D(20, 20))

    def getColor(self):
        return self.color

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.position.x, self.position.y, self.dimensions.x, self.dimensions.y))
        pygame.draw.rect(screen, self.color, (self.position.x + 1, self.position.y + 1, self.dimensions.x - 2, self.dimensions.y - 2))



class TextButton(Widget):

    def __init__(self, text, color = (0, 0, 0), font_size = 12):
        Widget.__init__(self)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.text_surface = None
        self.background = None
        self.is_mouse_pressed = False
        self.has_hover = False
        self.createSelf()

    def createSelf(self):
        font = loadFont("fonts/qaz.ttf", self.font_size)
        w, h = font.size(self.text)
        self.setDimensions(Vector2D(w + 10, h + 4))
        self.text_surface = font.render(self.text, True, self.color)
        self.background = pygame.Surface((self.dimensions.x, self.dimensions.y), pygame.SRCALPHA)
        self.background.fill((255,255,255,128))

    def draw(self, screen):
        position = self.getPosition()
        dimensions = self.getDimensions()
        screen.blit(self.background, (position.x, position.y))
        pygame.draw.rect(screen, (0, 0, 0), (position.x, position.y, dimensions.x, dimensions.y), 1)
        screen.blit(self.text_surface, (position.x + 5, position.y + 2))

    def recreateBackground(self):
        self.background = pygame.Surface((self.dimensions.x, self.dimensions.y), pygame.SRCALPHA)
        if self.has_hover:
            self.background.fill((255,255,255,255))
        else:
            self.background.fill((255, 255, 255, 128))
        if self.is_mouse_pressed:
            self.background.fill((255, 0, 0, 255))

    def mouseOver(self, event):
        self.has_hover = True
        self.recreateBackground()

    def mouseOut(self, event):
        self.has_hover = False
        self.is_mouse_pressed = False
        self.recreateBackground()

    def mousePress(self, event):
        self.is_mouse_pressed = True
        self.recreateBackground()

    def mouseRelease(self, event):
        self.is_mouse_pressed = False
        self.recreateBackground()
