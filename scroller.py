from input import MouseListener
from viewport import Rotation

class Scroller(MouseListener):

    def __init__(self, input, viewport):
        self.input = input
        self.viewport = viewport
        self.enabled = False
        self.rmb_down = False

    def enable(self):
        self.input.addMouseListener(self)

    def disable(self):
        self.input.removeMouseListener(self)

    def mouseButtonDown(self, event):
        if event.button == 3:
            self.rmb_down = True

    def mouseMotion(self, event):
        if self.rmb_down:
            self.scroll(event.rel[0], event.rel[1])

    def scroll(self, mouse_dx, mouse_dy):
            c = self.viewport.getCenter()

            rotation = self.viewport.getRotation()

            if rotation.type == Rotation.NORTH:
                if mouse_dx != 0:
                    c.x += 0.25 * mouse_dx
                    c.y -= 0.25 * mouse_dx
                if mouse_dy != 0:
                    c.x += 0.25 * mouse_dy
                    c.y += 0.25 * mouse_dy

            elif rotation.type == Rotation.SOUTH:
                if mouse_dx != 0:
                    c.x -= 0.25 * mouse_dx
                    c.y += 0.25 * mouse_dx
                if mouse_dy != 0:
                    c.x -= 0.25 * mouse_dy
                    c.y -= 0.25 * mouse_dy

            elif rotation.type == Rotation.EAST:
                if mouse_dx != 0:
                    c.y -= 0.25 * mouse_dx
                    c.x -= 0.25 * mouse_dx
                if mouse_dy != 0:
                    c.y -= 0.25 * mouse_dy
                    c.x += 0.25 * mouse_dy

            elif rotation.type == Rotation.WEST:
                if mouse_dx != 0:
                    c.y += 0.25 * mouse_dx
                    c.x += 0.25 * mouse_dx
                if mouse_dy != 0:
                    c.y += 0.25 * mouse_dy
                    c.x -= 0.25 * mouse_dy

            self.viewport.setCenter(c)

    def mouseButtonUp(self, event):
        if event.button == 3:
            self.rmb_down = False

