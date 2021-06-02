from json.decoder import JSONDecodeError

import serial.tools.list_ports
from potentiostat import Potentiostat
from serial.serialutil import SerialException

from datetime import datetime


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


def run_square_wave_voltammetry_test(pstat, context):
    test_name = 'squareWave'
    pstat.set_curr_range(context['current_range'])
    pstat.set_sample_rate(context['sample_rate'])

    start_time = datetime.now()
    print('{}:\t{} is starting'.format(start_time.strftime("%H:%M:%S"), context['title']))
    t, volt, curr = pstat.run_test(test_name, param=context['param'], display=None)
    print('{}:\t{} finished'.format(datetime.now().strftime("%H:%M:%S"), context['title']))
