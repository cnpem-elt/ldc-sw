from csv import reader
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog as fd
import time
import matplotlib.pyplot as plt

def get_data_from_csv(filename):
    csv_value=[]
    value = []
    
    current_samples = []
    temperature_samples = []
    elapsed_time = []
    
    with open(filename) as f:
        for csv_value in f:
            if csv_value.endswith('\n'):
                csv_value = csv_value[:-1]
                row = csv_value.split(';')
                if row:
                    value  = csv_value.split(',')
                try:
                    current_samples.append(float(value[n]))
                    elapsed_time.append(float(value[0]))
                    temperature_samples.append(float(value[4]))
                except ValueError:
                    continue
    return [current_samples, temperature_samples, elapsed_time]

def plot_graph (current_samples, temperature_samples, elapsed_time, graph_name):
    path = askdirectory(title='Select Folder')
    fig, ax = plt.subplots(1, 1, figsize=(25, 10))
    ax.locator_params(axis='y', tight=True, nbins=10)
    ax.locator_params(axis='x', tight=True, nbins=25)
    ax.plot(elapsed_time, current_samples)
    plt.xlabel('Time [s]')
    plt.ylabel('Leakage Current [mA]', color='tab:blue')
    plt.grid()
    ax1 = ax.twinx()
    ax1.set_ylabel('Temperature [°C]', color='tab:red')
    ax1.plot(elapsed_time, temperature_samples, color='tab:red')
    ax1.locator_params(axis='y', tight=True, nbins=10)
    plt.title(graph_name)
    plt.savefig(graph_name)
    plt.show()


if __name__ == "__main__":
    print('🅂🄴🄸 - 🄶🅁🄾🅄🄿')
    print('WARNING:This program only performs temperature drift graph.')
    
    filename = fd.askopenfilename(title='Select File')
    position = range (1,4)
    all_board = []
    
    board_test = (input('Serial number board in test:'))
    while board_test != '' : 
        all_board.append(str(board_test))
        board_test = input('Serial number board in test:')
    
    for n in position:
        m = n-1
        print('plotting in progress #'+all_board[m])  
        [current_samples, temperature_samples, elapsed_time] = get_data_from_csv(filename)
        plot_graph(current_samples, temperature_samples, elapsed_time, (str('LDC temperature drift serial#'+all_board[m])))
        current_samples.clear()
        temperature_samples.clear()
        elapsed_time.clear()
    print('Plotting successful! =)')