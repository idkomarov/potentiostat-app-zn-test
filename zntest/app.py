from tkinter import Tk

from zntest.gui import MainApplication


class ZnApplication:

    def __init__(self):
        self.root = Tk()
        MainApplication(self.root)

    def start(self):
        self.root.mainloop()
