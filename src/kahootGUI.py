#Hosted on Github at @Toblobs
#A Synergy Studios Project

version = '1.0.3'
sound_safe = False

import tkinter as tk
import tkinter.font as font

from kModules.kahootTk import *
from playsound import playsound

from threading import Thread
from time import sleep

root = tk.Tk()
root.title(f'KahootGUI v{version}')

#Use kahootBrandGuide: https://kahoot.com/files/2017/08/Kahoot-BrandGuide-July2019.pdf

palette = {'white':'#f2f2f2', 'black':'#333333', 'true-black':'#000000',
           'purple':'#46178f', 'dark-purple':'#25076b', 'light-purple':'#c2a5df',
           'orange':'#eb670f', 'dark-orange':'#e24104', 'light-orange':'#fad09e',
           'red':'#e21b3c', 'dark-red':'#c60929', 'light-red':'#ff99aa',
           'yellow':'#ffa602', 'dark-yellow':'#d89e00', 'light-yellow':'#ffdd33',
           'blue':'#1368ce', 'dark-blue':'#0542b9', 'light-blue':'#a2d1f2',
           'cyan':'#0aa3a3', 'dark-cyan':'#028282', 'light-cyan':'#99e5e5',
           'green':'#26890c', 'light-green':'#b2df9c', 'dark-green':'#0542b9'}
           
#---------------------------------------------------------------------------------#

class GUI:

    """Runs the GUI."""

    def __init__(self):

        self.reg_text = None
        self.bold_text = None
        #self.black_text = None

        self.defualt_family = 'Times New Roman'

        #To get exactly halfway, do 0.5  - half of relx/rely.

        self.canvas_screen = kScreen('canvas_screen')
        self.canvas = kCanvas(root, [500, 800, None, None], self.canvas_screen)
        
        self.connect_screen = kScreen('connect_screen')
        self.connect_frame = kFrame(root, palette['purple'], [0, 0, 1, 1], self.connect_screen)

        self.kahoot_logo = kImage(root, [0.1, 0.1, 0.5, 0.5], tk.PhotoImage(file = 'images/kahootLogo-full.png'), self.connect_screen)

        self.game_ip_frame = kFrame(root, palette['white'], [0.33, 0.4, 0.35, 0.20], self.connect_screen)
        self.game_ip = kEntry(self.game_ip_frame.widget, palette['white'], [0.1, 0.15, 0.80, 0.30], None,
                              self.connect_screen)
        self.game_ip_button = kButton(self.game_ip_frame.widget, palette['black'], [0.1, 0.50, 0.80, 0.30], "Enter", None,
                                      'game-ip-button', self.connect_screen)

        self.playlist = ['kOST-Doot.mp3', 'kOST-Lobby.mp3', 'kOST-BlackOut.mp3']

        self.state = 'Game IP'
        
        
    def render_fonts(self):

        """Renders all the fonts into the GUI."""

        #Render fonts in
        
        try:
            self.reg_text = font.Font(family = 'Montserrat')
            self.bold_text = font.Font(family = 'Montserrat', weight = 'bold')
            
        except:
            print(f"Font Error: Couldn't find font 'Montserrat'. Using {self.default_family}")
            self.reg_text = font.Font(family = self.default_family)
            self.bold_text = font.Font(family = self.default_family, weight = 'bold')

        # Apply fonts to widgets

        self.game_ip.widget['font'] = self.bold_text
        self.game_ip_button.widget['font'] = self.bold_text

    def render_effects(self):

        """Renders all the special effects on widgets to the GUI."""

        #self.game_ip_frame.widget['bd'] = 5
        #self.game_ip_frame.widget['relief'] = 'groove'

        self.game_ip.widget['highlightbackground'] = palette['red']
        self.game_ip.widget['bd'] = 3
        self.game_ip.widget['justify'] = 'center'
        
        #self.game_ip.widget['relief'] = 'flat'

        self.game_ip_button.widget['fg'] = palette['white']

        

    def play_sounds(self, playlist):

        if sound_safe:
            
            if self.state == 'Game IP':
                playsound(playlist[0])

            elif self.state == 'Lobby':
                playsound(playlist[1])


    def loop_widgets(self, arg):

        """The main loop of the program which loops the widgets to form a game."""

        while True:

            if self.state == 'Game IP':
                self.canvas.show()

                self.connect_frame.show()

                self.game_ip_frame.show()
                self.game_ip.show()
                self.game_ip_button.show()
                
        
    def start(self):

        """Starts the GUI."""

        self.render_fonts()
        self.render_effects()

        sound = Thread(target = self.play_sounds, args = (self.playlist,))
        sound.start()

        widget_loop = Thread(target = self.loop_widgets, args = (None,))
        widget_loop.start()
        
        #self.connect_screen.show_all()

        root.protocol('WM_DELETE_WINDOW', quit)
        root.mainloop()
        

   

g = GUI()
g.start()
