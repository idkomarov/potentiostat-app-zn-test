from datetime import datetime
from json.decoder import JSONDecodeError

import matplotlib.pyplot as plt
import serial.tools.list_ports
from potentiostat import Potentiostat
from serial.serialutil import SerialException


def get_available_ports():
    return [i.device for i in serial.tools.list_ports.comports()]


def connect(port):
    pstat_obj = None
    try:
        pstat_obj = Potentiostat(port, timeout=1.5)
    except SerialException or JSONDecodeError:
        pass
    return pstat_obj


def run_constant_voltage_test(pstat, context):
    test_name = 'constant'
    pstat.set_curr_range(context['current_range'])
    pstat.set_sample_rate(context['sample_rate'])

    start_time = datetime.now()
    print('{}:\t{} is starting'.format(start_time.strftime("%H:%M:%S"), context['title']))
    t, volt, curr = pstat.run_test(test_name, param=context['param'], display=None)
    print('{}:\t{} is finished'.format(datetime.now().strftime("%H:%M:%S"), context['title']))

    if context['create_plot']:
        plt.figure(1)
        plt.plot(t, volt)
        plt.xlabel('time (sec)')
        plt.ylabel('potential (V)')
        plt.grid('on')

        plt.figure(2)
        plt.plot(t, curr)
        plt.xlabel('time (sec)')
        plt.ylabel('current (uA)')
        plt.grid('on')

        plt.figure(3)
        plt.plot(volt, curr)
        plt.xlabel('potential (V)')
        plt.ylabel('current (uA)')
        plt.grid('on')

        plt.show(block=False)


def run_square_wave_voltammetry_test(pstat, context):
    test_name = 'squareWave'
    pstat.set_curr_range(context['current_range'])
    pstat.set_sample_rate(context['sample_rate'])

    start_time = datetime.now()
    print('{}:\t{} is starting'.format(start_time.strftime("%H:%M:%S"), context['title']))
    t, volt, curr = pstat.run_test(test_name, param=context['param'], display=None)
    print('{}:\t{} finished'.format(datetime.now().strftime("%H:%M:%S"), context['title']))

    if context['create_plot']:
        plt.figure(1)
        plt.plot(t, volt)
        plt.xlabel('time (sec)')
        plt.ylabel('potential (V)')
        plt.grid('on')

        plt.figure(2)
        plt.plot(t, curr)
        plt.xlabel('time (sec)')
        plt.ylabel('current (uA)')
        plt.grid('on')

        plt.figure(3)
        plt.plot(volt, curr)
        plt.xlabel('potential (V)')
        plt.ylabel('current (uA)')
        plt.grid('on')

        plt.show(block=False)
