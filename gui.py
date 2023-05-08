from input import MouseListener, KeyboardListener


class Gui(MouseListener):

    def __init__(self, input, screen):
        self.input = input
        self.screen = screen
        self.widgets = []
        self.hover_widget = None
        self.focus_widget = None

    def enable(self):
        self.input.addMouseListener(self)

    def disable(self):
        self.input.removeMouseListener(self)

    def addWidget(self, widget):
        self.widgets.append(widget)

    def removeWidget(self, widget):
        self.widgets.remove(widget)

    def draw(self):
        for widget in self.widgets:
            widget.draw(self.screen)

    def mouseMotion(self, event):
        consumed = False
        self.widgets.reverse()
        for widget in self.widgets:
            if widget.containsPoint(event.pos[0], event.pos[1]):
                self.setHoverWidget(widget, event)
                consumed = True
                break
        else:
            self.setHoverWidget(None, event)
        self.widgets.reverse()
        return consumed

    def setHoverWidget(self, widget, event):
        if widget is not self.hover_widget:
            if self.hover_widget is not None:
                self.hover_widget.mouseOut(event)
            if widget is not None:
                widget.mouseOver(event)
        self.hover_widget = widget

    def mouseClick(self, event):
        if self.hover_widget is not None:
            self.hover_widget.mouseClick(event)
            return True # Consumed

    def mouseButtonDown(self, event):
        if self.hover_widget is not None:
            self.hover_widget.mousePress(event)

    def mouseButtonUp(self, event):
        if self.hover_widget is not None:
            self.hover_widget.mouseRelease(event)