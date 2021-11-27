#Hosted on Github at @Toblobs
#A Synergy Studios Project

version = '1.0.2'
sound_safe = True

import tkinter as tk
from kahootGUISupport import *

if sound_safe == True:
    from playsound import playsound #Song by Vylet Pony: KAHOOT IT


PURPLE = '#46178F'
WHITE = '#FFFFFF'
BLACK = '#000000'

HELVETICA_16 = ("Helvetica", 16)

all_widgets = []

root = tk.Tk()

#---------------------------------------------------------------------------------#

main_screen = kScreen()

canvas = kCanvas(root, 500, 800, None)
main_frame = kFrame(root, PURPLE, [0, 0, 1, 1], main_screen)

text_label = kLabel(root, WHITE, [0.4, 0.4, 0.1, 0.1], 'label',
                    HELVETICA_16, main_screen)

logo_photo = tk.PhotoImage(file = 'kahootLogo.png')
image_label = kImage(root, [0.42, 0.1, 0.13, 0.2], logo_photo, main_screen)

canvas.show()
main_frame.show()

text_label.show()
image_label.show()

root.mainloop()

#if sound_safe == True:
    #playsound('kahootTheme.mp3') #Song by Vylet Pony: KAHOOT IT
