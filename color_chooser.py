from widget import Button, ColorButton, WidgetListener, Box
from vectors import Vector2D


class ColorChooser(WidgetListener):

    def __init__(self, interface, gui, screen):
        self.interface = interface
        self.gui = gui
        self.screen = screen
        self.color_buttons = []
        self.active_color_background = None

    def build(self):
        w, h = self.screen.get_size()

        self.active_color_background = Box((255,255,255,255))
        self.active_color_background.setDimensions(Vector2D(30, 30))
        self.gui.addWidget(self.active_color_background)

        self.color_buttons = [
            ColorButton((255, 255, 255)),
            ColorButton((255, 0, 0)),
            ColorButton((0, 255, 0)),
            ColorButton((0, 0, 255)),
            ColorButton((255, 255, 0)),
            ColorButton((255, 128, 0)),
            ColorButton((255, 0, 255)),
            ColorButton((0, 255, 255)),
            ColorButton((200, 200, 200))
        ]

        left = 400
        top = h - 25

        background = Box((255, 255, 255, 100))
        background.setPosition(Vector2D(left - 5, h - 30))
        background.setDimensions(Vector2D(230, 30))
        self.gui.addWidget(background)

        self.active_color_background.setPosition(Vector2D(left - 5, top - 5))
        for color_button in self.color_buttons:
            position = Vector2D(left, top)
            color_button.setPosition(position)
            color_button.addListener(self)
            self.gui.addWidget(color_button)
            left += 25

    def markColorSelected(self, color):
        for color_button in self.color_buttons:
            candidate_color = color_button.getColor()

            if candidate_color[0] == color[0] and candidate_color[1] == color[1] and candidate_color[2] == color[2]:
                position = color_button.getPosition()
                self.active_color_background.setPosition(Vector2D(position.x - 5, position.y - 5))
                break

    def onWidgetClick(self, widget, event):
        color = widget.color
        self.interface.setAndApplyColor(color)
        position = widget.getPosition()
        self.active_color_background.setPosition(Vector2D(position.x - 5, position.y - 5))