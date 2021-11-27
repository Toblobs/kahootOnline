#Hosted on Github at @Toblobs
#A Synergy Studios Project

import tkinter as tk
#-------------------------------------------------------------------------------------#

all_widgets = []

class kScreen:

    """Holds all the widgets in one place. The
       screen can hide and unhide everything inside of it,
       and can check whether a widget is in it."""

    def __init__(self):
        pass

    def check_widget_in(self, widget):
        
        return (widget.screen == self)
    
    def show_all(self):
        
        for w in all_widgets:
            if w.screen == self:
                w.hide()

    def hide_all(self):
        
        for w in all_widgets:
            if w.screen == self:
                w.show()



class kWidget:

    """A parent class that holds general attributes
       for all tkinter widgets."""

    def __init__(self, win, rel, screen):
        
        self.win = win
        
        self.relx = rel[0]
        self.rely = rel[1]
        
        self.relwidth = rel[2]
        self.relheight = rel[3]

        self.screen = screen

    def hide(self):
        pass

    def show(self):
        pass

##########################################################################

class kCanvas():

    """A canvas. Does not inherit from class <Widget>
       as it needs seperate coords code."""

    def __init__(self, win, height, width, screen):

        self.height = height
        self.width = width

        self.rel = None #Not needed

        #Initalisation of widget

        self.widget = tk.Canvas(win, height = self.height, width = self.width)
        all_widgets.append(self)

    def show(self):
        self.widget.pack()

    def hide(self):
        self.widget.pack_forget()

        
class kFrame(kWidget):

    """A frame. Inherits from class <Widget>
       Makes a tkinter Frame on __init__."""

    def __init__(self, win, bg, rel, screen):

        super().__init__(win, rel, screen)

        self.bg = bg

        #Initalisation of widget

        self.widget = tk.Frame(win, bg = self.bg)
        all_widgets.append(self)

    def show(self):
        self.widget.place(relx = self.relx, rely = self.rely,
                          relwidth = self.relwidth, relheight = self.relheight)

    def hide(self):
        self.widget.place_forget()
        

class kLabel(kWidget):

    """A label. Inherits from class <Widget>
       Makes a tkinter Label on __init__. Is text-based."""

    def __init__(self, win, bg, rel, text, font, screen):
        
        super().__init__(win, rel, screen)

        self.bg = bg

        self.text = text
        self.font = font
        
        #Initialisation of widget
        
        self.widget = tk.Label(win, bg = self.bg, text = self.text, font = self.font)
        all_widgets.append(self)

    def show(self):
        self.widget.place(relx = self.relx, rely = self.rely,
                          relwidth = self.relwidth, relheight = self.relheight)
    def hide(self):
        self.widget.place_forget()


class kImage(kWidget):

    """A image. Inherits from class <Widget>
       Makes a tkinter Label on __init__. Is image-based."""

    def __init__(self, win, rel, image, screen):

        super().__init__(win, rel, screen)

        self.image = image

        #Initialisation of widget

        self.widget = tk.Label(win, image = self.image)
        all_widgets.append(self)

    def show(self):
        self.widget.place(relx = self.relx, rely = self.rely,
                          relwidth = self.relwidth, relheight = self.relheight)
    def hide(self):
        self.widget.place_forget()
        

class kEntry:
    pass

class kButton:
    pass

#-------------------------------------------------------------------------------------#
