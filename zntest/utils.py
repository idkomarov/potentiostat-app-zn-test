import csv
import os
from datetime import datetime
from enum import Enum, auto
from json.decoder import JSONDecodeError

import matplotlib.pyplot as plt
import serial.tools.list_ports
from potentiostat import Potentiostat
from serial.serialutil import SerialException


class PstatTests(Enum):
    CONSTANT_VOLTAGE = auto()
    SQUAREWAVE_VOLTAMMETRY = auto()


def get_available_ports():
    return [i.device for i in serial.tools.list_ports.comports()]


def connect(port):
    pstat_obj = None
    try:
        pstat_obj = Potentiostat(port, timeout=1.5)
    except SerialException or JSONDecodeError:
        pass
    return pstat_obj


# TODO: add path with subfolder validation
def check_subfolder_path(subfolder_name):
    return True
    # output_file_folder = os.path.join(os.getcwd(), 'data', 'out', subfolder_name)
    # return os.path.exists(output_file_folder) or os.access(os.path.dirname(output_file_folder), os.W_OK)


def get_pstat_test_name(test_type):
    return {
        PstatTests.CONSTANT_VOLTAGE: 'constant',
        PstatTests.SQUAREWAVE_VOLTAMMETRY: 'squareWave'
    }.get(test_type)


def build_squarewave_plots(t, volt, curr):
    plt.figure(1)
    plt.plot(t, curr)
    plt.xlabel('time (sec)')
    plt.ylabel('current (uA)')
    plt.grid('on')

    plt.figure(2)
    plt.plot(volt, curr)
    plt.xlabel('potential (V)')
    plt.ylabel('current (uA)')
    plt.grid('on')

    plt.show(block=False)


def save_output_data(subfolder_path, pstat_test_name, start_time, compound, t, volt, curr):
    output_file_folder = os.path.join(os.getcwd(), 'data', 'out', subfolder_path, pstat_test_name)
    if os.path.exists(output_file_folder) is False:
        os.makedirs(output_file_folder)

    # save current-potential output
    iv_output_file_name = '{}__{}_I(V).csv'.format(start_time.strftime('%Y-%m-%d__%H-%M-%S'), compound)
    with open(os.path.join(output_file_folder, iv_output_file_name), 'w', encoding='utf-8', newline='') as output_csv:
        writer = csv.writer(output_csv, delimiter=',')
        writer.writerow(['volt', 'current', 'compound'])
        for i in range(len(t)):
            single_potential_value = f'{volt[i]:.4f}'
            single_current_value = f'{curr[i]:.4f}'
            row = [single_potential_value, single_current_value, compound]
            writer.writerow(row)

    # save current-time output
    it_output_file_name = '{}__{}_I(t).csv'.format(start_time.strftime('%Y-%m-%d__%H-%M-%S'), compound)
    with open(os.path.join(output_file_folder, it_output_file_name), 'w', encoding='utf-8', newline='') as output_csv:
        writer = csv.writer(output_csv, delimiter=',')
        writer.writerow(['time', 'current', 'compound'])
        for i in range(len(t)):
            single_time_value = f'{t[i]:.4f}'
            single_current_value = f'{curr[i]:.4f}'
            row = [single_time_value, single_current_value, compound]
            writer.writerow(row)

    # put current-potential output to database
    iv_database_file_path = os.path.join(output_file_folder, 'database_I(V).csv')
    if os.path.exists(iv_database_file_path) is False:
        with open(iv_database_file_path, 'w', newline='', encoding='utf-8') as database_file:
            writer = csv.writer(database_file, delimiter=',')
            writer.writerow(['volt', 'current', 'compound'])

    with open(os.path.join(iv_database_file_path), 'a', encoding='utf-8', newline='') as database_file:
        writer = csv.writer(database_file, delimiter=',')
        for i in range(len(t)):
            single_potential_value = f'{volt[i]:.4f}'
            single_current_value = f'{curr[i]:.4f}'
            row = [single_potential_value, single_current_value, compound]
            writer.writerow(row)

    # put current-time output to database
    it_database_file_path = os.path.join(output_file_folder, 'database_I(t).csv')
    if os.path.exists(it_database_file_path) is False:
        with open(it_database_file_path, 'w', newline='', encoding='utf-8') as database_file:
            writer = csv.writer(database_file, delimiter=',')
            writer.writerow(['time', 'current', 'compound'])

    with open(os.path.join(it_database_file_path), 'a', encoding='utf-8', newline='') as database_file:
        writer = csv.writer(database_file, delimiter=',')
        for i in range(len(t)):
            single_time_value = f'{t[i]:.4f}'
            single_current_value = f'{curr[i]:.4f}'
            row = [single_time_value, single_current_value, compound]
            writer.writerow(row)


def run_pstat_test(pstat, test_type, context):
    pstat_test_name = get_pstat_test_name(test_type)
    if pstat_test_name is None:
        return
    pstat.set_curr_range(context['current_range'])
    pstat.set_sample_rate(context['sample_rate'])

    start_time = datetime.now()
    print('[{}]\t{} is starting'.format(start_time.strftime("%H:%M:%S"), context['title']))
    t, volt, curr = pstat.run_test(pstat_test_name, param=context['param'], display=None)
    print('[{}]\t{} finished'.format(datetime.now().strftime("%H:%M:%S"), context['title']))

    if test_type is PstatTests.SQUAREWAVE_VOLTAMMETRY and \
            context['create_plot']:
        build_squarewave_plots(t, volt, curr)

    if context['save_data']:
        if context['save_to_specific_folder']:
            subfolder_path = context['subfolder_path']
        else:
            subfolder_path = ''
        save_output_data(subfolder_path, pstat_test_name, start_time, context['compound'], t, volt, curr)
