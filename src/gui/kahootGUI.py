#Hosted on Github at @Toblobs
#A Synergy Studios Project

version = '1.0.2'
sound_safe = True

import tkinter as tk
from kModules.kahootTk import *

PURPLE = '#46178F'
WHITE = '#FFFFFF'
BLACK = '#000000'

HELVETICA_16 = ("Helvetica", 16)

all_widgets = []

root = tk.Tk()

#---------------------------------------------------------------------------------#

main_screen = kScreen()

canvas = kCanvas(root, [500, 800, None, None], None)
main_frame = kFrame(root, PURPLE, [0, 0, 1, 1], main_screen)

text_label = kLabel(root, WHITE, [0.4, 0.4, 0.1, 0.1], 'label',
                    HELVETICA_16, main_screen)

logo_photo = tk.PhotoImage(file = 'images/kahootLogo-full.png')
image_label = kImage(root, [0.42, 0.1, 0.13, 0.2], logo_photo, main_screen)

#button = kButton(root, BLACK, [0.6, 0.6, 0.5, 0.3], HELVETICA_16, 'a button',
                 #'/button', main_screen)

canvas.show()
main_frame.show()

text_label.show()
image_label.show()

root.mainloop()
