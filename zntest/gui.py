from tkinter import *


class MainApplication(Frame):
    """
        Class initializing GUI for application taking measurements of Zn concentration called "Zn test".
        Zn test consists of 3 sequential tests in this order: constant voltage (x2) + squarewave voltammetry.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.set_initial_properties()

    def set_initial_properties(self):
        self.master.title('Potentiostat App. Zn test')
        self.master.geometry('600x300')
        self.master.resizable(False, False)
