#Hosted on Github at @Toblobs
#A Synergy Studios Project

#Tut: https://coderslegacy.com/python/python-pygame-tutorial/

import pygame
from pygame.locals import *

version = '1.0.2'


def check_event():
    """Checks for an event in the pygame library."""
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def main():
    """"Main running scripts."""

    ### SETUP
    pygame.init()

    FPS = 30
    FramePerSec = pygame.tick.Clock()

    DISPLAY = pygame.display.set_mode((300,300))

    BLUE  = (0, 0, 255)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    colours = (BLUE, RED, GREEN, BLACK , WHITE)

    DISPLAY.fill(WHITE)
    pygame.display.set_caption("Example")



    ### CLASSES

    
    class Window():
        """A window which holds the shapes and widgets. You
           can hide and show all the aspects of a window."""

        def __init__(self):
            pass

        def hide(self):
            pass

        def show(self):
            pass

    

    
    #---------------------------------------#
    

    while True:
        check_events()

        FramePerSec.tick(FPS)


if __name__ == "__main__":
    main()
