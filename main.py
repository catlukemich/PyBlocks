import pygame
from viewport import Viewport
from scene import Scene
from utils import loadImage
from floor import Floor
from sprites import ImageSprite
from scroller import Scroller
from gui import Gui
from placer import Placer
from world import World
from input import Input
from interface import Interface

class Main():

    def __init__(self):
        pygame.init()

        screen = pygame.display.set_mode((1280, 860), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("PyBlocks")

        icon = loadImage("img/icon.png")
        pygame.display.set_icon(icon)

        input = Input()

        gui = Gui(input, screen)
        gui.enable()

        scene = Scene()
        viewport = Viewport(screen, scene)

        world = World(scene, 40, 40)
        world.show()

        scroller = Scroller(input, viewport)
        scroller.enable()

        placer = Placer(input, world, viewport)
        placer.enable()

        interface = Interface(world, gui, screen, viewport, placer)
        interface.build()

        done = False
        clock = pygame.time.Clock()
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                else:
                    input.handleEvent(event)
                    if event.type == pygame.KEYDOWN:
                        if event.key == 97:
                            viewport.rotateCW()
                        elif event.key == 100:
                            viewport.rotateCCW()

            sky_color = world.sky_color
            screen.fill(sky_color)
            scene.update(clock)
            viewport.draw()
            gui.draw()
            pygame.display.flip()

            clock.tick(60)


if __name__ == "__main__":
    main = Main()
