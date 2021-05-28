from json.decoder import JSONDecodeError

import serial.tools.list_ports
from potentiostat import Potentiostat
from serial.serialutil import SerialException


def get_available_ports():
    return [i.device for i in serial.tools.list_ports.comports()]


def connect(port):
    pstat_obj = None
    try:
        pstat_obj = Potentiostat(port)
    except SerialException or JSONDecodeError:
        pass
    return pstat_obj
