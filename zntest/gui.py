from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from zntest.utils import *


class Connection:
    """
        Class initializing connection frame.
    """

    def __init__(self, parent, set_pstat_obj_fun):
        self.frame = LabelFrame(parent, text='Connection')
        self.frame.pack(side=TOP, anchor=NW)

        self.description_label = Label(self.frame, text='Select potentiostat connected port')
        self.description_label.pack(side=LEFT, padx=5)

        self.device_ports_combobox = Combobox(self.frame, width=10, values=('None',),
                                              postcommand=self.get_device_ports_combobox_values, state='readonly')
        self.device_ports_combobox.current(0)
        self.device_ports_combobox.pack(side=LEFT, padx=5)

        self.connection_button = Button(self.frame, text='Connect',
                                        command=lambda: self.click_connection_button(set_pstat_obj_fun))
        self.connection_button.pack(side=LEFT, padx=5)

    def get_device_ports_combobox_values(self):
        ports = get_available_ports()
        ports.insert(0, 'None')
        self.device_ports_combobox['values'] = ports
        self.device_ports_combobox.current(0)

    def click_connection_button(self, set_pstat_obj_fun):
        combobox_value = self.device_ports_combobox.get()
        if combobox_value != 'None':
            pstat = connect(combobox_value)
            if pstat is not None:
                set_pstat_obj_fun(pstat)
                self.description_label.pack_forget()
                self.device_ports_combobox['state'] = DISABLED
                self.connection_button['state'] = DISABLED
                self.connection_button['text'] = 'Connected'
            else:
                messagebox.showwarning('Warning!', 'Unable to initialize potentiostat on this port')
        else:
            messagebox.showwarning('Warning!', 'Select one of available ports')


class MainApplication:
    """
        Class initializing application main window.
    """

    def __init__(self, parent):
        self.parent = parent

        self.pstat = None

        self.set_initial_properties()

        self.connection = Connection(parent, self.set_pstat_obj)

    def set_initial_properties(self):
        self.parent.title('Potentiostat App. Zn test')
        self.parent.geometry('600x300')
        self.parent.resizable(False, False)

    def set_pstat_obj(self, pstat):
        self.pstat = pstat
