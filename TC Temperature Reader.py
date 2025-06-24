"""
File:                       TC Temperature Reader.py

Library Call Demonstrated:  mcculw.ul.t_in()

Purpose:                    Reads multiple temperature input channels.

Demonstration:              Displays the temperature input.

Other Library Calls:        mcculw.ul.release_daq_device()

"""
from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mcculw import ul
from mcculw.enums import TempScale
from mcculw.device_info import DaqDeviceInfo

try:
    from console_examples_util import config_first_detected_device
except ImportError:
    from .console_examples_util import config_first_detected_device


def Two_Room_Thermo_Sync():
    # By default, the example detects and displays all available devices and
    # selects the first device listed. Use the dev_id_list variable to filter
    # detected devices by device ID (see UL documentation for device IDs).
    # If use_device_detection is set to False, the board_num variable needs to
    # match the desired board number configured with Instacal. (This comes from the MCC Example code)
    use_device_detection = True
    dev_id_list = []
    board_num = 0

    try:
        if use_device_detection:
            config_first_detected_device(board_num, dev_id_list) # checks for device

        daq_dev_info = DaqDeviceInfo(board_num)

        print('\nActive DAQ device: ', daq_dev_info.product_name, ' (',
              daq_dev_info.unique_id, ')\n', sep='')

        ai_info = daq_dev_info.get_ai_info()
        if ai_info.num_temp_chans <= 0:
            raise Exception('Error: The DAQ device does not support '
                            'temperature input')
        
        channels = [0,1,3,6,22,23,24,29,30,31]
        samples = 1 # seconds
        total_time = 21600 # seconds ( Still need to convert to hours)
        readings = total_time // samples

        # Lists to store time and temperatures
        timestamps = []
        temperatures = {channel: [] for channel in channels}

        #Set up for graph
        plt.ion()
        fig, ax = plt.subplots()
        lines = {}
        colors = ['b','g','r','c','m','y','k']

        # Setup for each channel to be plotted
        for idx, ch in enumerate(channels):
            line, = ax.plot([], [], label=f"Channel {ch}", color=colors[idx % len(colors)])
            lines[ch] = line

        ax.set_title("Real-Time Temperature of Two-Room (\u00b0F)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Temperature")
        ax.grid(True)
        ax.legend()

        start_time = time.time()

        # For loop to start collecting the data and timestamp it
        for i in range(readings):
            current_time = time.time() - start_time
            timestamps.append(current_time)

            print(f"\nReading {i+1}/{readings} at {current_time:.1f} seconds:")


            for channel in channels:
                # Get the value from the device
                value = ul.t_in(board_num, int(channel), TempScale.FAHRENHEIT)
                temperatures[channel].append(value)
                # Display the value
                print('Channel', channel, 'Value (deg F):', f"{value:.2f}")
                lines[channel].set_xdata(timestamps)
                lines[channel].set_ydata(temperatures[channel])
            
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.01)
            time.sleep(samples)
    
    except Exception as e:
        print('\n', e)
    finally:
        if use_device_detection:
            ul.release_daq_device(board_num)
        
        # save data to CSV 
        if timestamps and any(temperatures.values()):
            timestamp_save = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"C:/Cristian Hernandez/Python Code for Two-Room/Tests/TC_Temp_Reader_{timestamp_save}.csv" # Directory of saved file

            try:
                with open(filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Time (s)"] + [f"Channel {ch}" for ch in channels])
                    for i in range(len(timestamps)):
                        row = [f"{timestamps[i]:.2f}"] + [ f"{temperatures[ch][i]:.2f}"
                            if i < len(temperatures[ch])
                            else "" 
                            for ch in channels 
                        ]
                        writer.writerow(row)
                print(f"\nData saved to {filename}")
            except Exception as file_error:
                print(f'Failed to save: {file_error}')
        # To display graph
        plt.ioff()
        plt.show()


if __name__ == '__main__':
    Two_Room_Thermo_Sync()