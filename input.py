import pygame


class MouseListener:

    def mouseButtonDown(self, event):
        pass

    def mouseButtonUp(self, event):
        pass

    def mouseMotion(self, event):
        pass

    def mouseClick(self, event):
        pass

    def mouseGained(self, event):
        pass

    def mouseLost(self, event):
        pass


class KeyboardListener:

    def keyDown(self, event):
        pass

    def keyUp(self, event):
        pass


class Input:

    def __init__(self):
        self.key_listeners = []
        self.mouse_listeners = []
        self.last_mouse_button = None
        self.last_mb_x = 0
        self.last_mb_y = 0
        self.last_mouse_owner = None

    def addMouseListener(self, listener):
        self.mouse_listeners.append(listener)

    def addKeyboardListener(self, listener):
        self.key_listeners.append(listener)

    def removeMouseListener(self, listener):
        self.mouse_listeners.remove(listener)

    def removeKeyboardListener(self, listener):
        self.key_listeners.remove(listener)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.initMouseClick(event)
            self.dispatchMouseButtonDown(event)

        if event.type == pygame.MOUSEBUTTONUP:
            self.dispatchMouseButtonUp(event)
            clicked = self.endMouseClick(event)
            if clicked:
                self.dispatchClick(event)

        if event.type == pygame.MOUSEMOTION:
            self.dispatchMouseMotion(event)

        if event.type == pygame.KEYDOWN:
            self.dispatchKeyDown(event)

        if event.type == pygame.KEYUP:
            self.dispatchKeyUp(event)

    def initMouseClick(self, event):
        self.last_mouse_button = event.button
        self.last_mb_x = event.pos[0]
        self.last_mb_y = event.pos[1]

    def endMouseClick(self, event):
        mb_x = event.pos[0]
        mb_y = event.pos[1]
        mb = event.button
        dx = abs(self.last_mb_x - mb_x)
        dy = abs(self.last_mb_y - mb_y)
        if dx < 3 and dy < 3 and mb == self.last_mouse_button:
            self.dispatchClick(event)

    def dispatchClick(self, event):
        for listener in self.mouse_listeners:
            consumed = listener.mouseClick(event)
            if consumed:
                break

    def dispatchMouseButtonDown(self, event):
        for listener in self.mouse_listeners:
            consumed = listener.mouseButtonDown(event)
            if consumed: break

    def dispatchMouseButtonUp(self, event):
        for listener in self.mouse_listeners:
            consumed = listener.mouseButtonUp(event)
            if consumed: break

    def dispatchMouseMotion(self, event):
        for listener in self.mouse_listeners:
            consumed = listener.mouseMotion(event)
            if consumed:
                self.reassignMouseOwner(listener, event)
                break

    def reassignMouseOwner(self, listener, event):
        if listener is not self.last_mouse_owner:
            listener.mouseGained(event)
            if self.last_mouse_owner is not None:
                self.last_mouse_owner.mouseLost(event)
        self.last_mouse_owner = listener

    def dispatchKeyDown(self, event):
        for listener in self.key_listeners:
            consumed = listener.keyDown(event)
            if consumed: break

    def dispatchKeyUp(self, event):
        for listener in self.key_listeners:
            consumed = listener.keyUp(event)
            if consumed:
                break