from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

import zntest.utils as utils


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
                                              postcommand=self.set_device_ports_combobox_values, state='readonly')
        self.device_ports_combobox.current(0)
        self.device_ports_combobox.pack(side=LEFT, padx=5)

        self.connection_button = Button(self.frame, text='Connect',
                                        command=lambda: self.click_connection_button(set_pstat_obj_fun))
        self.connection_button.pack(side=LEFT, padx=5)

    def set_device_ports_combobox_values(self):
        ports = utils.get_available_ports()
        ports.insert(0, 'None')
        self.device_ports_combobox['values'] = ports
        self.device_ports_combobox.current(0)

    def click_connection_button(self, set_pstat_obj_fun):
        combobox_value = self.device_ports_combobox.get()
        if combobox_value != 'None':
            pstat = utils.connect(combobox_value)
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


class ConstantVoltageSingleTestProperties:
    """
        Class initializing constant voltage single test properties frame.
    """

    def __init__(self, parent, test_number):
        self.frame = LabelFrame(parent, text=f'Constant Voltage Test #{test_number} Properties')
        self.frame.pack(side=LEFT, anchor=N)

        self.current_range_label = Label(self.frame, text='Current range')
        self.current_range_label.pack(side=TOP)

        self.current_range_combo = Combobox(self.frame, values=('',), state='readonly')
        self.current_range_combo.pack(side=TOP)

        self.sample_rate_label = Label(self.frame, text='Sample rate (samples/sec)')
        self.sample_rate_label.pack(side=TOP)

        # TODO: check sample rate range
        self.sample_rate_input_value = StringVar(value=100)
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
        self.quite_time_input_value = StringVar(value=1000)
        self.quite_time_input = Spinbox(self.frame, from_=0, to=10000, increment=1000,
                                        textvariable=self.quite_time_input_value)
        self.quite_time_input.pack(side=TOP)

        self.value_label = Label(self.frame, text='Value (V)')
        self.value_label.pack(side=TOP)

        # TODO: check value range
        self.value_input_value = StringVar(value=-1.000)
        self.value_input_value.trace('w', lambda name, index, mode: self.update_quite_value())
        self.value_input = Spinbox(self.frame, from_=-10.0, to=10.0, increment=1.5, textvariable=self.value_input_value,
                                   format='%.3f')
        self.value_input.pack(side=TOP)

        self.duration_label = Label(self.frame, text='Duration (ms)')
        self.duration_label.pack(side=TOP)

        # TODO: check duration range
        self.duration_input_value = StringVar(value=5000)
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

    def is_valid(self):
        properties_name = self.frame['text']
        try:
            sample_rate = int(self.sample_rate_input_value.get())
            if not (1 <= sample_rate <= 200):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nSample rate value must be in range [1; 200]')
                return FALSE

            quite_value = float(self.quite_value_input_value.get())
            if not (-10.0 <= quite_value <= 10.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nQuite value must be in range [-10; 10]')
                return FALSE

            quite_time = int(self.quite_time_input.get())
            if not (0 <= quite_time <= 10000):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nQuite time must be in range [0; 10000]')
                return FALSE

            value = float(self.value_input_value.get())
            if not (-10.0 <= value <= 10.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nQuite value must be in range [-10; 10]')

            duration = int(self.duration_input_value.get())
            if not (1000 <= duration <= 100000):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nQuite value must be in range [1000; 10000]')

        except ValueError as ve:
            messagebox.showerror('The error occurred!', f'{properties_name}\n{ve.__str__().capitalize()}')
            return FALSE

        return TRUE


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
        self.sample_rate_input_value = StringVar(value=100)
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
        self.quite_time_input_value = StringVar(value=1000)
        self.quite_time_input = Spinbox(self.frame, from_=0, to=10000, increment=1000,
                                        textvariable=self.quite_time_input_value)
        self.quite_time_input.pack(side=TOP)

        self.amplitude_label = Label(self.frame, text='Amplitude (V)')
        self.amplitude_label.pack(side=TOP)

        # TODO: check amplitude range
        self.amplitude_input_value = StringVar(value=0.05)
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
        self.step_value_input_value = StringVar(value=0.005)
        self.step_value_input = Spinbox(self.frame, from_=0.001, to=10.0, increment=0.005,
                                        textvariable=self.step_value_input_value,
                                        format='%.3f')
        self.step_value_input.pack(side=TOP)

        self.window_label = Label(self.frame, text='Window')
        self.window_label.pack(side=TOP)

        self.window_input_value = StringVar(value=0.2)
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

    def is_valid(self):
        properties_name = self.frame['text']
        try:
            sample_rate = int(self.sample_rate_input_value.get())
            if not (1 <= sample_rate <= 200):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nSample rate value must be in range [1; 200]')
                return FALSE

            quite_value = float(self.quite_value_input_value.get())
            if not (-10.0 <= quite_value <= 10.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nQuite value must be in range [-10; 10]')
                return FALSE

            quite_time = int(self.quite_time_input.get())
            if not (0 <= quite_time <= 10000):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nQuite time must be in range [0; 10000]')
                return FALSE

            amplitude = float(self.amplitude_input_value.get())
            if not (0.0 <= amplitude <= 10.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nAmplitude must be in range [0.0; 10.0]')
                return FALSE

            start_value = float(self.start_value_input_value.get())
            if not (-10.0 <= start_value <= 10.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nStart value must be in range [-10; 10]')
                return FALSE

            final_value = float(self.final_value_input_value.get())
            if not (-10.0 <= final_value <= 10.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nFinal value must be in range [-10; 10]')
                return FALSE

            step_value = float(self.step_value_input_value.get())
            if not (-10.0 <= step_value <= 10.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nStep value must be in range [0.001; 10.0]')
                return FALSE

            window = float(self.window_input_value.get())
            if not (0.0 <= window <= 1.0):
                messagebox.showerror('The error occurred!',
                                     f'{properties_name}\nWindow must be in range [0.0; 1.0]')
                return FALSE

        except ValueError as ve:
            messagebox.showerror('The error occurred!', f'{properties_name}\n{ve.__str__().capitalize()}')
            return FALSE

        return TRUE


class ZnTestOptions:
    """
        Class initializing 'Zn test' options frame including run test button.
    """

    def __init__(self, parent, constant_voltage_test_1_properties, constant_voltage_test_2_properties,
                 square_wave_voltammetry_test_properties, run_test_fun):
        self.constant_voltage_test_1_properties = constant_voltage_test_1_properties
        self.constant_voltage_test_2_properties = constant_voltage_test_2_properties
        self.square_wave_voltammetry_test_properties = square_wave_voltammetry_test_properties
        self.run_test_fun = run_test_fun

        self.frame = LabelFrame(parent, text='Test options')
        self.frame.pack(side=LEFT, anchor=NW)

        self.compound_label = Label(self.frame, text='Compound')
        self.compound_label.pack(side=TOP)

        self.compound_input_value = StringVar(value='ABC')
        self.compound_input_value.trace('w', lambda name, index, mode: self.limit_compound_entry())
        self.compound_input = Entry(self.frame, textvariable=self.compound_input_value)
        self.compound_input.pack(side=TOP)

        self.is_save_constant_voltage_tests_output_data = BooleanVar(value=1)
        self.is_save_constant_voltage_tests_checkbox = Checkbutton(self.frame, text='Save constant voltage output data',
                                                                   variable=self.is_save_constant_voltage_tests_output_data)
        self.is_save_constant_voltage_tests_checkbox.pack(side=TOP)

        self.is_save_square_wave_voltammetry_test_output_data = BooleanVar(value=1)
        self.is_save_square_wave_voltammetry_test_checkbox = Checkbutton(self.frame,
                                                                         text='Save square voltammetry output data',
                                                                         variable=self.is_save_square_wave_voltammetry_test_output_data)
        self.is_save_square_wave_voltammetry_test_checkbox.pack(side=TOP)

        self.run_test_button = Button(self.frame, text='Run',
                                      command=lambda: self.click_run_test_button())
        self.run_test_button.pack(side=TOP)

        self.disable_all_elements()

    def disable_all_elements(self):
        for element in self.frame.winfo_children():
            element.config(state=DISABLED)

    def enable_all_elements(self):
        for element in self.frame.winfo_children():
            element.config(state=NORMAL)

    def limit_compound_entry(self):
        new_entry_value = self.compound_input_value.get()
        if len(new_entry_value) > 15:
            self.compound_input_value.set(new_entry_value[:15])

    def click_run_test_button(self):
        is_valid_properties = self.constant_voltage_test_1_properties.is_valid() and \
                              self.constant_voltage_test_2_properties.is_valid() and \
                              self.square_wave_voltammetry_test_properties.is_valid()
        if is_valid_properties:
            self.run_test_fun()


class MainApplication:
    """
        Class initializing application main window.
    """

    def __init__(self, parent):
        self.parent = parent

        self.pstat = None

        self.set_initial_properties()

        self.connection = Connection(self.parent, self.set_pstat_obj)

        self.tests = LabelFrame(self.parent, text='Tests')
        self.tests.pack(side=TOP, anchor=NW)
        self.tests.description_label = Label(self.tests, text='Set tests properties')
        self.tests.description_label.pack(side=TOP, anchor=NW, padx=5)

        self.constant_voltage_test_1_properties = ConstantVoltageSingleTestProperties(self.tests, 1)
        self.constant_voltage_test_2_properties = ConstantVoltageSingleTestProperties(self.tests, 2)
        self.square_wave_voltammetry_test_properties = SquareWaveVoltammetrySingleTestProperties(self.tests)
        self.test_options = ZnTestOptions(self.parent,
                                          self.constant_voltage_test_1_properties,
                                          self.constant_voltage_test_2_properties,
                                          self.square_wave_voltammetry_test_properties,
                                          self.run_test)

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

        self.test_options.enable_all_elements()

    def run_constant_voltage_test_1(self):
        context = {}
        context['title'] = self.constant_voltage_test_1_properties.frame['text'][:-11]
        context['current_range'] = self.constant_voltage_test_1_properties.current_range_combo.get()
        context['sample_rate'] = int(self.constant_voltage_test_1_properties.sample_rate_input_value.get())
        context['param'] = {
            'quietValue': float(self.constant_voltage_test_1_properties.quite_value_input_value.get()),
            'quietTime': int(self.constant_voltage_test_1_properties.quite_time_input_value.get()),
            'value': float(self.constant_voltage_test_1_properties.value_input_value.get()),
            'duration': int(self.constant_voltage_test_1_properties.duration_input_value.get()),
        }
        context['create_plot'] = self.constant_voltage_test_1_properties.is_show_plot_value.get()
        context['compound'] = self.test_options.compound_input_value.get()
        context['save_data'] = self.test_options.is_save_constant_voltage_tests_output_data.get()
        utils.run_constant_voltage_test(self.pstat, context)

    def run_constant_voltage_test_2(self):
        context = {}
        context['title'] = self.constant_voltage_test_2_properties.frame['text'][:-11]
        context['current_range'] = self.constant_voltage_test_2_properties.current_range_combo.get()
        context['sample_rate'] = int(self.constant_voltage_test_2_properties.sample_rate_input_value.get())
        context['param'] = {
            'quietValue': float(self.constant_voltage_test_2_properties.quite_value_input_value.get()),
            'quietTime': int(self.constant_voltage_test_2_properties.quite_time_input_value.get()),
            'value': float(self.constant_voltage_test_2_properties.value_input_value.get()),
            'duration': int(self.constant_voltage_test_2_properties.duration_input_value.get()),
        }
        context['create_plot'] = self.constant_voltage_test_2_properties.is_show_plot_value.get()
        context['compound'] = self.test_options.compound_input_value.get()
        context['save_data'] = self.test_options.is_save_constant_voltage_tests_output_data.get()
        utils.run_constant_voltage_test(self.pstat, context)

    def run_square_wave_voltammetry_test(self):
        context = {}
        context['title'] = self.square_wave_voltammetry_test_properties.frame['text'][:-11]
        context['current_range'] = self.square_wave_voltammetry_test_properties.current_range_combo.get()
        context['sample_rate'] = int(self.square_wave_voltammetry_test_properties.sample_rate_input_value.get())
        context['param'] = {
            'quietValue': float(self.square_wave_voltammetry_test_properties.quite_value_input_value.get()),
            'quietTime': int(self.square_wave_voltammetry_test_properties.quite_time_input_value.get()),
            'amplitude': float(self.square_wave_voltammetry_test_properties.amplitude_input_value.get()),
            'startValue': float(self.square_wave_voltammetry_test_properties.start_value_input_value.get()),
            'finalValue': float(self.square_wave_voltammetry_test_properties.final_value_input_value.get()),
            'stepValue': float(self.square_wave_voltammetry_test_properties.step_value_input_value.get()),
            'window': float(self.square_wave_voltammetry_test_properties.window_input_value.get()),
        }
        context['create_plot'] = self.square_wave_voltammetry_test_properties.is_show_plot_value.get()
        context['compound'] = self.test_options.compound_input_value.get()
        context['save_data'] = self.test_options.is_save_constant_voltage_tests_output_data.get()
        utils.run_square_wave_voltammetry_test(self.pstat, context)

    def run_test(self):
        self.run_constant_voltage_test_1()
        self.run_constant_voltage_test_2()
        self.run_square_wave_voltammetry_test()
