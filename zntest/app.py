from tkinter import Tk

from zntest.gui import MainApplication


class ZnApplication:
    """
        Class initializing GUI for application taking measurements of Zn concentration called "Zn test".
        Zn test consists of 3 sequential tests in this order: constant voltage (x2) + squarewave voltammetry.
    """

    def __init__(self):
        self.root = Tk()
        MainApplication(self.root)

    def start(self):
        self.root.mainloop()
