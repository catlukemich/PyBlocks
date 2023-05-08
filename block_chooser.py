from utils import loadImage
from vectors import Vector2D, Vector3D
from widget import  WidgetListener, BlockButton, Box
from block import Block, BlockDefinitionFactory, BlockHeading

class BlockChooser(WidgetListener):

    def __init__(self, interface, gui, screen, placer, block_definition_factory):
        self.interface = interface
        self.gui = gui
        self.screen = screen
        self.placer = placer

        self.definition_factory = block_definition_factory
        self.standard_block_button = None
        self.cone_block_button = None
        self.slope_block_button = None
        self.cylinder_block_button = None
        self.corner_block_button = None
        self.portal_block_button = None
        self.active_block_background = None
        self.selected_block_color = (255,255,255)

    def build(self):
        w,h = self.screen.get_size()

        background = Box((255,255, 255, 100))
        background.setPosition(Vector2D(290, h - 130))
        background.setDimensions(Vector2D(320, 70))
        self.gui.addWidget(background)

        self.active_block_background = Box((255,255,255,255))
        self.active_block_background.setDimensions(Vector2D(50, 50))
        self.gui.addWidget(self.active_block_background)

        # Block type selection buttons:
        left = 300
        self.standard_block_button = BlockButton(loadImage("img/gui/block.png"))
        position = Vector2D(left, h - 120)
        self.standard_block_button.setPosition(position)
        self.standard_block_button.addListener(self)
        self.gui.addWidget(self.standard_block_button)
        self.active_block_background.setPosition(position)

        left += 50
        self.cone_block_button = BlockButton(loadImage("img/gui/cone.png"))
        position = Vector2D(left, h - 120)
        self.cone_block_button.setPosition(position)
        self.cone_block_button.addListener(self)
        self.gui.addWidget(self.cone_block_button)

        left += 50
        self.slope_block_button = BlockButton(loadImage("img/gui/slope.png"))
        position = Vector2D(left, h - 120)
        self.slope_block_button.setPosition(position)
        self.slope_block_button.addListener(self)
        self.gui.addWidget(self.slope_block_button)

        left += 50
        self.cylinder_block_button = BlockButton(loadImage("img/gui/cylinder.png"))
        position = Vector2D(left, h - 120)
        self.cylinder_block_button.setPosition(position)
        self.cylinder_block_button.addListener(self)
        self.gui.addWidget(self.cylinder_block_button)

        left += 50
        self.corner_block_button = BlockButton(loadImage("img/gui/corner.png"))
        position = Vector2D(left, h - 120)
        self.corner_block_button.setPosition(position)
        self.corner_block_button.addListener(self)
        self.gui.addWidget(self.corner_block_button)

        left += 50
        self.portal_block_button = BlockButton(loadImage("img/gui/portal.png"))
        position = Vector2D(left, h - 120)
        self.portal_block_button.setPosition(position)
        self.portal_block_button.addListener(self)
        self.gui.addWidget(self.portal_block_button)

        self.all_blocks_buttons = [
            self.standard_block_button,
            self.cone_block_button,
            self.slope_block_button,
            self.cylinder_block_button,
            self.corner_block_button,
            self.portal_block_button
        ]

    def tintButtons(self, color):
        for button in self.all_blocks_buttons:
            button.tint(color)

        self.selected_block_color = color

    def onWidgetClick(self, widget, event):
        # Block buttons click handling:
        place = Vector3D(0, 0, 0)
        heading = BlockHeading.NORTH
        factory = self.definition_factory

        if widget is self.standard_block_button:
            definition = factory.getDefinition("Standard block")
            block = Block(place, heading, definition)
            self.placer.setBlock(block)

        if widget is self.cylinder_block_button:
            definition = factory.getDefinition("Cylinder block")
            block = Block(place, heading, definition)
            self.placer.setBlock(block)

        if widget is self.cone_block_button:
            definition = factory.getDefinition("Cone block")
            block = Block(place, heading, definition)
            self.placer.setBlock(block)

        if widget is self.slope_block_button:
            definition = factory.getDefinition("Slope block")
            block = Block(place, heading, definition)
            self.placer.setBlock(block)

        if widget is self.corner_block_button:
            definition = factory.getDefinition("Corner block")
            block = Block(place, heading, definition)
            self.placer.setBlock(block)

        if widget is self.portal_block_button:
            definition = factory.getDefinition("Portal block")
            block = Block(place, heading, definition)
            self.placer.setBlock(block)

        position = widget.getPosition()
        self.active_block_background.setPosition(position)
