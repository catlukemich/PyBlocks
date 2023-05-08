from widget import Button, WidgetListener,  Box
from utils import loadImage
from vectors import Vector2D


COLOR_MODE_BLOCKS = 0
COLOR_MODE_FLOOR = 1
COLOR_MODE_SKY = 2

class ColorModeChooser(WidgetListener):

    def __init__(self, interface, gui, screen, world):
        self.interface = interface
        self.gui = gui
        self.screen = screen
        self.world = world

        self.color_blocks_button = None
        self.color_floor_button = None
        self.color_sky_button = None
        self.active_color_mode_button = None
        self.active_color_mode_background = None

        self.color_mode = COLOR_MODE_BLOCKS

    def build(self):
        w, h = self.screen.get_size()

        left = 290

        self.active_color_mode_background = Box((255, 255, 255, 255))
        self.active_color_mode_background.setPosition(Vector2D(left, h - 30))
        self.active_color_mode_background.setDimensions(Vector2D(30, 30))
        self.gui.addWidget(self.active_color_mode_background)

        background = Box((255, 255, 255, 128))
        background.setPosition(Vector2D(left, h - 30))
        background.setDimensions(Vector2D(90, 30))
        self.gui.addWidget(background)

        self.color_blocks_button = Button(loadImage("img/gui/color_block.png"))
        self.color_blocks_button.setPosition(Vector2D(290, h - 30))
        self.color_blocks_button.addListener(self)
        self.gui.addWidget(self.color_blocks_button)

        left += 30
        self.color_floor_button = Button(loadImage("img/gui/color_floor.png"))
        self.color_floor_button.setPosition(Vector2D(left, h - 30))
        self.color_floor_button.addListener(self)
        self.gui.addWidget(self.color_floor_button)

        left += 30
        self.color_sky_button = Button(loadImage("img/gui/color_sky.png"))
        self.color_sky_button.setPosition(Vector2D(left, h - 30))
        self.color_sky_button.addListener(self)
        self.gui.addWidget(self.color_sky_button)

        self.active_color_mode_button = self.color_blocks_button

    def onWidgetClick(self, widget, event):

        position = widget.getPosition()
        self.active_color_mode_background.setPosition(position)
        self.active_color_mode_button = widget

        if widget is self.color_blocks_button:
            self.interface.color_chooser.markColorSelected(self.interface.selected_blocks_color)
            self.color_mode = COLOR_MODE_BLOCKS

        if widget is self.color_floor_button:
            floor_color = self.world.floor.getColor()
            self.interface.color_chooser.markColorSelected(floor_color)
            self.color_mode = COLOR_MODE_FLOOR

        if widget is self.color_sky_button:
            sky_color = self.world.getSkyColor()
            self.interface.color_chooser.markColorSelected(sky_color)
            self.color_mode = COLOR_MODE_SKY

    def getColorMode(self):
        return self.color_mode