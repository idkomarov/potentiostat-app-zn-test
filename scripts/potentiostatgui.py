import tkinter


class PotentiostatGUI:
    """
    Class describing GUI for application taking measurements of Zn concentration called "Zn test".
    Zn test consists of 3 consecutive tests in this order: constant voltage voltammetry (x2) + squarewave voltammetry.
    """

    def __init__(self):
        app = tkinter.Tk()
        app.title('Potentiostat App. Zn test')
        app['bg'] = '#fff'
        app.geometry('600x300')
        app.resizable(width=False, height=False)

        self.app = app

    def start(self):
        self.app.mainloop()
