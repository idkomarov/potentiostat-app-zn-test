import csv
import os
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
    print('[{}]\t{} is starting'.format(start_time.strftime("%H:%M:%S"), context['title']))
    t, volt, curr = pstat.run_test(test_name, param=context['param'], display=None)
    print('[{}]\t{} is finished'.format(datetime.now().strftime("%H:%M:%S"), context['title']))

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

    if context['save_data']:
        output_file_name = '{}__{}.csv'.format(context['compound'], start_time.strftime('%Y-%m-%d__%H-%M-%S'))
        output_file_folder = os.path.join(os.getcwd(), 'data', 'out', 'constant')
        if os.path.exists(output_file_folder) is False:
            os.makedirs(output_file_folder)

        with open(os.path.join(output_file_folder, output_file_name), 'w', encoding='utf-8', newline='') as output_csv:
            writer = csv.writer(output_csv, delimiter=',')
            writer.writerow(['time', 'volt', 'current', 'compound'])
            for i in range(len(t)):
                single_time_value = f'{t[i]:.4f}'
                single_potential_value = f'{volt[i]:.4f}'
                single_current_value = f'{curr[i]:.4f}'
                row = [single_time_value, single_potential_value, single_current_value, context['compound']]
                writer.writerow(row)

        database_file_path = os.path.join(os.getcwd(), 'data', 'out', 'constant', 'database.csv')
        with open(os.path.join(database_file_path), 'a', encoding='utf-8', newline='') as output_csv:
            writer = csv.writer(output_csv, delimiter=',')
            writer.writerow(['time', 'volt', 'current', 'compound'])
            for i in range(len(t)):
                single_time_value = f'{t[i]:.4f}'
                single_potential_value = f'{volt[i]:.4f}'
                single_current_value = f'{curr[i]:.4f}'
                row = [single_time_value, single_potential_value, single_current_value, context['compound']]
                writer.writerow(row)
            writer.writerow([])
            writer.writerow([])


def run_square_wave_voltammetry_test(pstat, context):
    test_name = 'squareWave'
    pstat.set_curr_range(context['current_range'])
    pstat.set_sample_rate(context['sample_rate'])

    start_time = datetime.now()
    print('[{}]\t{} is starting'.format(start_time.strftime("%H:%M:%S"), context['title']))
    t, volt, curr = pstat.run_test(test_name, param=context['param'], display=None)
    print('[{}]\t{} finished'.format(datetime.now().strftime("%H:%M:%S"), context['title']))

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

    if context['save_data']:
        output_file_name = '{}__{}.csv'.format(context['compound'], start_time.strftime('%Y-%m-%d__%H-%M-%S'))
        output_file_folder = os.path.join(os.getcwd(), 'data', 'out', 'squarewave')
        if os.path.exists(output_file_folder) is False:
            os.makedirs(output_file_folder)

        with open(os.path.join(output_file_folder, output_file_name), 'w', encoding='utf-8', newline='') as output_csv:
            writer = csv.writer(output_csv, delimiter=',')
            writer.writerow(['time', 'volt', 'current', 'compound'])
            for i in range(len(t)):
                single_time_value = f'{t[i]:.4f}'
                single_potential_value = f'{volt[i]:.4f}'
                single_current_value = f'{curr[i]:.4f}'
                row = [single_time_value, single_potential_value, single_current_value, context['compound']]
                writer.writerow(row)
