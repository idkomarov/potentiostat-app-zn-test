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


class ConstantVoltageProperties:
    """
        Class initializing constant voltage properties frame.
    """

    # TODO: add input values validation
    def __init__(self, parent, test_number):
        self.frame = LabelFrame(parent, text=f'Constant Voltage Test #{test_number} Properties')
        self.frame.pack(side=LEFT)

        self.current_range_label = Label(self.frame, text='Current range')
        self.current_range_label.pack(side=TOP)

        self.current_range_combo = Combobox(self.frame, values=('',), state='readonly')
        self.current_range_combo.pack(side=TOP)

        self.sample_rate_label = Label(self.frame, text='Sample rate (samples/sec)')
        self.sample_rate_label.pack(side=TOP)

        # TODO: check sample rate range
        self.sample_rate_input_value = IntVar(value=100)
        self.sample_rate_input = Spinbox(self.frame, from_=1, to=200, increment=50,
                                         textvariable=self.sample_rate_input_value)
        self.sample_rate_input.pack(side=TOP)

        self.quite_value_label = Label(self.frame, text='Quite Value (V)')
        self.quite_value_label.pack(side=TOP)

        # TODO: check quite value range
        self.quite_value_input_value = DoubleVar(value=-1.000)
        self.quite_value_input = Spinbox(self.frame, from_=-10.0, to=10.0, increment=1.5,
                                         textvariable=self.quite_value_input_value, format='%.3f')
        self.quite_value_input.pack(side=TOP)

        self.quite_time_label = Label(self.frame, text='Quite Time (ms)')
        self.quite_time_label.pack(side=TOP)

        # TODO: check quite time range
        self.quite_time_input_value = IntVar(value=1000)
        self.quite_time_input = Spinbox(self.frame, from_=0, to=10000, increment=1000,
                                        textvariable=self.quite_time_input_value)
        self.quite_time_input.pack(side=TOP)

        self.value_label = Label(self.frame, text='Value (V)')
        self.value_label.pack(side=TOP)

        # TODO: check value range
        self.value_input_value = DoubleVar(value=-1.000)
        self.value_input_value.trace("w", lambda name, index, mode: self.update_quite_value())
        self.value_input = Spinbox(self.frame, from_=-10.0, to=10.0, increment=1.5, textvariable=self.value_input_value,
                                   format='%.3f')
        self.value_input.pack(side=TOP)

        self.duration_label = Label(self.frame, text='Duration (ms)')
        self.duration_label.pack(side=TOP)

        # TODO: check duration range
        self.duration_input_value = IntVar(value=20000)
        self.duration_input = Spinbox(self.frame, from_=1000, to=100000, increment=5000,
                                      textvariable=self.duration_input_value)
        self.duration_input.pack(side=TOP)

        self.is_show_plot_value = BooleanVar(value=1)
        self.show_plot_checkbox = Checkbutton(self.frame, text='Create & show plot', variable=self.is_show_plot_value)
        self.show_plot_checkbox.pack(side=TOP)

        self.disable_all_elements()

    def disable_all_elements(self):
        for element in self.frame.winfo_children():
            element.config(state=DISABLED)

    def enable_all_elements(self):
        for element in self.frame.winfo_children():
            element.config(state=NORMAL)
        self.quite_value_input.config(state=DISABLED)
        self.quite_time_input.config(state=DISABLED)

    def set_current_range_values(self, values):
        self.current_range_combo.config(values=values)
        self.current_range_combo.config(state='readonly')
        self.current_range_combo.current(int(len(values) / 2))

    def update_quite_value(self):
        self.quite_value_input.set(self.value_input_value.get())


class SquareWaveVoltammetrySingleTestProperties:
    """
        Class initializing square wave voltammetry single test properties frame.
    """

    def __init__(self, parent):
        self.frame = LabelFrame(parent, text=f'Square Wave Voltammetry Properties')
        self.frame.pack(side=LEFT, anchor=N)

        self.current_range_label = Label(self.frame, text='Current range')
        self.current_range_label.pack(side=TOP)

        self.current_range_combo = Combobox(self.frame, values=('',), state='readonly')
        self.current_range_combo.pack(side=TOP)

        self.sample_rate_label = Label(self.frame, text='Sample rate (samples/sec)')
        self.sample_rate_label.pack(side=TOP)

        # TODO: check sample rate range
        self.sample_rate_input_value = IntVar(value=100)
        self.sample_rate_input = Spinbox(self.frame, from_=1, to=200, increment=50,
                                         textvariable=self.sample_rate_input_value)
        self.sample_rate_input.pack(side=TOP)

        self.quite_value_label = Label(self.frame, text='Quite Value (V)')
        self.quite_value_label.pack(side=TOP)

        # TODO: check quite value range
        self.quite_value_input_value = StringVar(value=-1.000)
        self.quite_value_input = Spinbox(self.frame, from_=-10.0, to=10.0, increment=1.5,
                                         textvariable=self.quite_value_input_value, format='%.3f')
        self.quite_value_input.pack(side=TOP)

        self.quite_time_label = Label(self.frame, text='Quite Time (ms)')
        self.quite_time_label.pack(side=TOP)

        # TODO: check quite time range
        self.quite_time_input_value = IntVar(value=1000)
        self.quite_time_input = Spinbox(self.frame, from_=0, to=10000, increment=1000,
                                        textvariable=self.quite_time_input_value)
        self.quite_time_input.pack(side=TOP)

        self.amplitude_label = Label(self.frame, text='Amplitude (V)')
        self.amplitude_label.pack(side=TOP)

        # TODO: check amplitude range
        self.amplitude_input_value = DoubleVar(value=0.05)
        self.amplitude_input = Spinbox(self.frame, from_=0, to=10, increment=0.01,
                                       textvariable=self.amplitude_input_value, format='%.3f')
        self.amplitude_input.pack(side=TOP)

        self.start_value_label = Label(self.frame, text='Start value (V)')
        self.start_value_label.pack(side=TOP)

        # TODO: check start value range
        self.start_value_input_value = StringVar(value=-1.000)
        self.start_value_input_value.trace('w', lambda name, index, mode: self.update_quite_value())
        self.start_value_input = Spinbox(self.frame, from_=-10.0, to=10.0, increment=1.5,
                                         textvariable=self.start_value_input_value,
                                         format='%.3f')
        self.start_value_input.pack(side=TOP)

        self.final_value_label = Label(self.frame, text='Final value (V)')
        self.final_value_label.pack(side=TOP)

        # TODO: check final value range
        self.final_value_input_value = StringVar(value=1.000)
        self.final_value_input = Spinbox(self.frame, from_=-10.0, to=10.0, increment=1.5,
                                         textvariable=self.final_value_input_value,
                                         format='%.3f')
        self.final_value_input.pack(side=TOP)

        self.step_value_label = Label(self.frame, text='Step value (V)')
        self.step_value_label.pack(side=TOP)

        # TODO: do update step value range
        self.step_value_input_value = DoubleVar(value=0.005)
        self.step_value_input = Spinbox(self.frame, from_=0.001, to=10.0, increment=0.005,
                                        textvariable=self.step_value_input_value,
                                        format='%.3f')
        self.step_value_input.pack(side=TOP)

        self.window_label = Label(self.frame, text='Window')
        self.window_label.pack(side=TOP)

        self.window_input_value = DoubleVar(value=0.2)
        self.window_input = Spinbox(self.frame, from_=0.0, to=1.0, increment=0.1, textvariable=self.window_input_value,
                                    format='%.2f')
        self.window_input.pack(side=TOP)

        self.is_show_plot_value = BooleanVar(value=1)
        self.show_plot_checkbox = Checkbutton(self.frame, text='Create & show plot', variable=self.is_show_plot_value)
        self.show_plot_checkbox.pack(side=TOP)

        self.disable_all_elements()

    def disable_all_elements(self):
        for element in self.frame.winfo_children():
            element.config(state=DISABLED)

    def enable_all_elements(self):
        for element in self.frame.winfo_children():
            element.config(state=NORMAL)
        self.quite_value_input.config(state=DISABLED)
        self.quite_time_input.config(state=DISABLED)

    def set_current_range_values(self, values):
        self.current_range_combo.config(values=values)
        self.current_range_combo.config(state='readonly')
        self.current_range_combo.current(int(len(values) / 2))

    def update_quite_value(self):
        self.quite_value_input.set(self.start_value_input_value.get())


class MainApplication:
    """
        Class initializing application main window.
    """

    def __init__(self, parent):
        self.parent = parent

        self.pstat = None

        self.set_initial_properties()

        self.connection = Connection(parent, self.set_pstat_obj)

        self.tests = LabelFrame(self.parent, text='Tests')
        self.tests.pack(side=TOP, anchor=NW)
        self.tests.description_label = Label(self.tests, text='Set tests properties')
        self.tests.description_label.pack(side=TOP, anchor=NW, padx=5)

        self.constant_voltage_test_1_properties = ConstantVoltageProperties(self.tests, 1)
        self.constant_voltage_test_2_properties = ConstantVoltageProperties(self.tests, 2)
        self.square_wave_voltammetry_test_properties = SquareWaveVoltammetrySingleTestProperties(self.tests)

    def set_initial_properties(self):
        self.parent.title('Potentiostat App. Zn test')
        self.parent.geometry('634x600')
        self.parent.resizable(False, False)

    def set_pstat_obj(self, pstat):
        self.pstat = pstat
        available_current_ranges = self.pstat.get_all_curr_range()

        self.constant_voltage_test_1_properties.enable_all_elements()
        self.constant_voltage_test_1_properties.set_current_range_values(available_current_ranges)

        self.constant_voltage_test_2_properties.enable_all_elements()
        self.constant_voltage_test_2_properties.set_current_range_values(available_current_ranges)

        self.square_wave_voltammetry_test_properties.enable_all_elements()
        self.square_wave_voltammetry_test_properties.set_current_range_values(available_current_ranges)
