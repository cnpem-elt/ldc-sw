from csv import reader
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog as fd
import time
import matplotlib.pyplot as plt


def get_data_from_csv(filename):
    current = []
    temp = []
    csv_value=[]
    value = []
    with open(filename) as f:
        for csv_value in f:
            if csv_value.endswith('\n'):
                csv_value = csv_value[:-1]
                row = csv_value.split(';')
                if row:
                    value  = csv_value.split(',')
                try:
                    current.append(float(value[0]))
                    temp.append(float(value[1]))
                except ValueError:
                    continue
    return [current, temp]

def plot_graph(x,y, graph_name):
    path = askdirectory(title='Select Folder')
    print(path)
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.locator_params(axis='y', tight=True, nbins=15)
    ax.locator_params(axis='x', tight=True, nbins=30)
    ax.plot(x, y)
    plt.xlabel('Time [s]')
    plt.ylabel('Leakage Current [mA]')
    plt.grid()
    plt.title(graph_name)
    plt.savefig(path+'/'+ graph_name+'.jpg')
    plt.close()
    return "Graph file named '{}' saved successfully!".format(graph_name+'.jpg')

        

if __name__ == "__main__":
    print('🅂🄴🄸 - 🄶🅁🄾🅄🄿')
    print('WARNING:This program only performs leakage current graph.')
    filename = fd.askopenfilename(title='Select File')
    [current, temp] = get_data_from_csv(filename)
    plot_graph(temp,current,(input('Insert graph name:')))
    
    print(current)
    print(temp)
