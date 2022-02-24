#!/usr/bin/env python3
# accuracy-test.py

import matplotlib.pyplot as plt
import numpy as np
import os
import time
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askdirectory
from ldc import Commands
from scpi import Supply

# Gets the current directory to return in the end of the test
cwd = os.getcwd()

# LDC Commands start
ldc = Commands()

instrument = input("Insert instrument id: ")
scpi = Supply(instrument)


# Accuracy Test Properties and Functions
class AccuracyTest:
    """
    Sets up the variables and commands to execute the accuracy test of the LDC board
    """

    def __init__(self):
        self.total_mean = []
        self.total_error = []
        self.total_std = []
        self.total_current = []
        self.total_ppc = []
        self.test_name = ''
        self.total_steps = 0
        self.path = ''
        print("Accuracy Test module activated!")

    def start(self, step, minimum, maximum, duration, testname='AccuracyTest'):
        """
        Executes the accuracy test of the LDC board

        :param testname: Sets the name for the folder to receive the data of the test
        :type testname: str
        :param step: Current step for each measure of the test, in Amperes
        :type step: float
        :param minimum: Minimum current value for accuracy test, in Amperes
        :type minimum: float
        :param maximum: Maximum current value for accuracy test, in Amperes
        :type maximum: float
        :param duration: Duration of the measure in each step, in seconds
        :type duration: int
        """
        Tk().withdraw()
        self.test_name = testname
        self.path = askdirectory(title='Select Folder')
        test_date = datetime.today().strftime("%d/%m/%Y - %H:%M")
        os.makedirs(os.path.join(self.path, self.test_name))
        os.makedirs(os.path.join(self.path, self.test_name+"\\Samples"))
        os.makedirs(os.path.join(self.path, self.test_name+"\\Plots"))
        os.chdir(os.path.join(self.path, self.test_name))
        # Saves a file with the test information
        info_file = open('INFO.txt', 'w+')
        info_file.write(testname+"\n"+test_date+"\nSEI - Electronics Systems and Instrumentation")
        info_file.close()
        os.chdir(cwd)
        span = maximum - minimum
        self.total_steps = round(span/step) + 1
        print("Starting test...")
        scpi.enable_output()
        for i in range(int(self.total_steps)):  # Loop to read the ground leakage in each step
            current = minimum + (i*step)
            scpi.set_current(current)
            print("Values for {0:.3f} mA".format(current*1000))
            test_name = '{0:.1f}mA Leakage Current'.format(current*1000)
            print('--'*20)
            time.sleep(0.15)
            ldc.read_ground_leakage(duration)
            # Change to the created directories and saves all acquired information
            os.chdir(os.path.join(self.path, self.test_name+"\\Plots"))
            ldc.save_graph(test_name)
            os.chdir(os.path.join(self.path, self.test_name+"\\Samples"))
            ldc.save_csv_file(test_name)
            os.chdir(cwd)
            self.total_mean.append(ldc.mean)
            self.total_error.append(ldc.mean_error)
            self.total_std.append(ldc.std_dev)
            self.total_current.append(current*1000)
            self.total_ppc.append(ldc.ppc)
            if (i*step) < span:
                print("Acquisition completed! Moving to the next step...\n")
            elif (i*step) == span:
                print("Accuracy Test completed!")
        scpi.disable_output()
        AccuracyTest.save_graphs(self)
        AccuracyTest.save_csv_files(self)

    def save_graphs(self):
        """
        Saves all the specific plots at the end of the accuracy test. The graphics are:\n
        - Source Current x Mean Leakage Current
        - Source Current x Mean Current Error
        - Source Current X Current Standard Deviation
        """
        # Saves the Plot of Source Current X Mean Leakage Current
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=20)
        ax.plot(self.total_current, np.arange(0, self.total_steps, 1), marker='o', label='Source Current')
        ax.plot(self.total_mean, np.arange(0, self.total_steps, 1), marker='o', label='Mean Leakage Current')
        plt.xlabel('Source Current [mA]')
        plt.ylabel('Test Steps')
        plt.title('Source Current X Leakage Current Mean')
        os.chdir(os.path.join(self.path, self.test_name+"\\Plots"))
        jpgname = 'SourceCurrent_X_MeanLeakageCurrent.jpg'
        plt.legend()
        plt.savefig(jpgname)
        plt.close()
        os.chdir(cwd)
        print("Graphic file named '{}' saved successfully!".format(jpgname))

        # Saves the Plot of Source Current X Mean Current Error
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=20)
        ax.plot(self.total_current, self.total_error)
        plt.xlabel('Source Current [mA]')
        plt.ylabel('Mean Current Error [mA]')
        plt.title('Source Current X Mean Current Error')
        os.chdir(os.path.join(self.path, self.test_name+"\\Plots"))
        jpgname = 'SourceCurrent_X_MeanCurrentError.jpg'
        plt.savefig(jpgname)
        plt.close()
        os.chdir(cwd)
        print("Graphic file named '{}' saved successfully!".format(jpgname))

        # Saves the Plot of Source Current X Current Standard Deviation
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=20)
        ax.plot(self.total_current, self.total_std)
        plt.xlabel('Source Current [mA]')
        plt.ylabel('Leakage Current Standard Deviation [mA]')
        plt.title('Source Current X Current Standard Deviation')
        os.chdir(os.path.join(self.path, self.test_name+"\\Plots"))
        jpgname = 'SourceCurrent_X_CurrentStandardDeviation.jpg'
        plt.savefig(jpgname)
        plt.close()
        os.chdir(cwd)
        print("Graphic file named '{}' saved successfully!".format(jpgname))

    def save_csv_files(self):
        """
        Saves all the csv files of the specific graphics data at the end of the accuracy test.
        """
        # Saves the csv file of Source Current and Mean Leakage Current data
        csvname = 'SourceCurrent_X_MeanLeakageCurrent.csv'
        data = [['Source Current'], ['Mean Leakage Current']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.total_mean)):
            column0.append(self.total_current[row])
            column1.append(self.total_mean[row])
        os.chdir(os.path.join(self.path, self.test_name+"\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' saved successfully!".format(csvname))

        # Saves the csv file of Source Current and Mean Current Error data
        csvname = 'SourceCurrent_X_CurrentErrorMean.csv'
        data = [['Source Current'], ['Mean Current Error']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.total_error)):
            column0.append(self.total_current[row])
            column1.append(self.total_error[row])
        os.chdir(os.path.join(self.path, self.test_name+"\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' saved successfully!".format(csvname))

        # Saves the csv file of Source Current and Current Standard Deviation data
        csvname = 'SourceCurrent_X_CurrentStandardDeviation.csv'
        data = [['Source Current'], ['Current Standard Deviation']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.total_std)):
            column0.append(self.total_current[row])
            column1.append(self.total_std[row])
        os.chdir(os.path.join(self.path, self.test_name+"\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' saved successfully!".format(csvname))


if __name__ == '__main__':
    acc = AccuracyTest()
    tstep = float(input("Insert the current step, in Amperes: "))
    tminimum = float(input("Insert the minimum current of the test, in Amperes: "))
    tmaximum = float(input("Insert the maximum current of the test, in Amperes: "))
    tduration = int(input("Insert the duration of the measure steps, in seconds: "))
    testnum = int(input("Insert the test number: "))
    tname = "AccuracyTest-"+str(testnum)
    apply_degauss = int(input("Apply the degaussing process? 1(yes)/0(No):"))
    if apply_degauss == 1:
        ldc.degauss()
    elif apply_degauss == 0:
        pass
    acc.start(tstep, tminimum, tmaximum, tduration, tname)
