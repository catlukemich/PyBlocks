from widget import Button, WidgetListener, BlockButton, Box, TextButton
from utils import loadImage
from vectors import Vector2D, Vector3D
from block import Block, BlockDefinition, BlockDefinitionFactory, BlockHeading
from color_chooser import ColorChooser
from block_chooser import BlockChooser
from color_mode_chooser import ColorModeChooser, COLOR_MODE_BLOCKS, COLOR_MODE_SKY, COLOR_MODE_FLOOR

import tkinter as tk
from tkinter import filedialog




class Interface(WidgetListener):

    def __init__(self, world, gui, screen, viewport, placer):
        self.world = world
        self.gui = gui
        self.screen = screen
        self.viewport = viewport
        self.placer = placer

        self.rotate_left_btn = None
        self.rotate_right_btn = None

        self.definition_factory = BlockDefinitionFactory()
        self.block_chooser = BlockChooser(self, gui, screen, placer, self.definition_factory)
        self.color_chooser = ColorChooser(self, gui, screen)
        self.color_mode_chooser = ColorModeChooser(self, gui, screen, world)
        self.selected_blocks_color = (255,255,255)

        self.load_button = None
        self.save_button = None

    def build(self):
        self.buildRotationControls()
        self.buildBlocksChooser()
        self.buildColorChooser()
        self.buildColorModeChooser()
        self.buildLoadAndSaveControls()

    def buildRotationControls(self):
        w,h = self.screen.get_size()

        background = Box((255,255, 255, 100))
        background.setPosition(Vector2D(10, h - 130))
        background.setDimensions(Vector2D(250, 120))
        self.gui.addWidget(background)

        # Rotation buttons creation:
        self.rotate_left_btn = Button(loadImage("img/gui/rotate_left.png"))
        position = Vector2D(20, h - 120)
        self.rotate_left_btn.setPosition(position)
        self.rotate_left_btn.addListener(self)
        self.gui.addWidget(self.rotate_left_btn)

        self.rotate_right_btn = Button(loadImage("img/gui/rotate_right.png"))
        position = Vector2D(20 + 120, h - 120)
        self.rotate_right_btn.setPosition(position)
        self.rotate_right_btn.addListener(self)
        self.gui.addWidget(self.rotate_right_btn)


    def buildBlocksChooser(self):
        self.block_chooser.build()


    def buildColorChooser(self):
        self.color_chooser.build()

    def buildColorModeChooser(self):
        self.color_mode_chooser.build()

    def buildLoadAndSaveControls(self):
        w, h = self.screen.get_size()

        background = Box((255,255,255,128))
        background.setPosition(Vector2D(640, h - 30))
        background.setDimensions(Vector2D(110, 30))
        self.gui.addWidget(background)

        self.save_button = TextButton("Save", (0,0,0), 18)
        self.save_button.setPosition(Vector2D(644, h - 28))
        self.save_button.addListener(self)
        self.gui.addWidget(self.save_button)

        self.load_button = TextButton("Load", (0,0,0), 18)
        self.load_button.setPosition(Vector2D(700, h - 28))
        self.load_button.addListener(self)
        self.gui.addWidget(self.load_button)

    def setAndApplyColor(self, color):
        mode = self.color_mode_chooser.getColorMode()
        if mode == COLOR_MODE_BLOCKS:
            self.block_chooser.tintButtons(color)
            self.placer.setColor(color)

        if mode == COLOR_MODE_FLOOR:
            self.world.floor.setColor(color)

        if mode == COLOR_MODE_SKY:
            self.world.setSkyColor(color)

    def onWidgetClick(self, widget, event):
        # Rotation buttons handling:
        if widget is self.rotate_left_btn:
            self.viewport.rotateCCW()

        if widget is self.rotate_right_btn:
            self.viewport.rotateCW()



        if widget is self.load_button:
            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename()
            if file_path:
                self.load(file_path)

        if widget is self.save_button:
            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.asksaveasfilename()
            if file_path:
                self.save(file_path)

    def save(self, file_path):
        with open(file_path, "w") as file:

            floor_color = self.world.floor.getColor()
            file.write(str(floor_color[0]) + ", " + str(floor_color[1]) + ", " + str(floor_color[2]) + " \n")
            sky_color = self.world.getSkyColor()
            file.write(str(sky_color[0]) + ", " + str(sky_color[1]) + ", " + str(sky_color[2]) + " \n")

            blocks = self.world.getBlocks()
            for x in range(0, len(blocks)):
                arr_x = blocks[x]
                for y in range(0, len(arr_x)):
                    arr_y = arr_x[y]
                    for z in range(0, len(arr_y)):
                        block = arr_y[z]
                        if block is not None:
                            self.writeBlock(file, block)



    def writeBlock(self, file, block):
        definition = block.getDefinition()
        name = definition.name
        place = block.getPlace()
        color = block.getColor()
        heading = block.getHeading()
        file.write(name + ", ")
        file.write(str(place.x) + ", " + str(place.y) + ", " + str(place.z) + ", ")
        file.write(str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ", ")
        file.write(str(heading) + ", ")
        file.write("\n")


    def load(self, file_path):
        with open(file_path, "r") as file:
            scene = self.world.scene
            blocks = self.world.getBlocks()
            for x in range(0, len(blocks)):
                arr_x = blocks[x]
                for y in range(0, len(arr_x)):
                    arr_y = arr_x[y]
                    for z in range(0, len(arr_y)):
                        block = arr_y[z]
                        if block is not None:
                            scene.removeSprite(block)
            self.world.clearBlocks()

            lines = file.readlines()

            floor_color = lines[0].split(", ")
            r = int(floor_color[0])
            g = int(floor_color[1])
            b = int(floor_color[2])
            color = (r, g, b)
            self.world.floor.setColor(color)

            sky_color = lines[1].split(", ")
            r = int(sky_color[0])
            g = int(sky_color[1])
            b = int(sky_color[2])
            color = (r, g, b)
            self.world.setSkyColor(color)

            for line_no in range(2, len(lines)):
                line = lines[line_no]
                data = line.split(", ")
                name = data[0]
                x = int(data[1])
                y = int(data[2])
                z = int(data[3])
                red = int(data[4])
                green = int(data[5])
                blue = int(data[6])
                heading = int(data[7])

                place = Vector3D(x, y, z)
                definition = self.definition_factory.getDefinition(name)
                block = Block(place, heading, definition)
                block.setColor((red, green, blue))
                block.setLocation(Vector3D(place.x, place.y, place.z + 0.5))

                self.world.setBlock(place.x, place.y, place.z, block)
                scene.addSprite(block)




