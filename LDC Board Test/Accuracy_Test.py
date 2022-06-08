#!/usr/bin/env python3
# Accuracy_Test.py

import matplotlib.pyplot as plt
import numpy as np
import os
import time
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askdirectory
from LDC_Commands import LDC

# Gets the current directory to return in the end of the test
cwd = os.getcwd()

# LDC Functions start
ldc = LDC()


# Accuracy Test Properties and Functions
class AccuracyTest:
    """
    Sets up the variables and commands to execute the accuracy test of the LDC board
    """

    def __init__(self):
        self.iib_address_list = []
        self.total_mean = []
        self.total_error = []
        self.total_std = []
        self.total_current = []
        self.total_ppc = []
        self.total_steps = 0
        self.testnum = 0
        self.boards_quantity = 0
        self.path = ''
        print("Accuracy Test module initialized!")

    def start(self, step, minimum, maximum, duration, test_number, iib_address):
        """
        Executes the accuracy test of the LDC board

        :param step: Current step for each measure of the test, in Amperes
        :type step: float
        :param minimum: Minimum current value for accuracy test, in Amperes
        :type minimum: float
        :param maximum: Maximum current value for accuracy test, in Amperes
        :type maximum: float
        :param duration: Duration of the measurement in each step, in seconds
        :type duration: int
        :param test_number: Sets the number of the test
        :type test_number: int
        """
        self.testnum = test_number
        self.iib_address = iib_address
        os.makedirs(os.path.join(self.path, str(iib_address)+"\\"+str(test_number)))
        os.makedirs(os.path.join(self.path, str(iib_address)+"\\"+str(test_number)+"\\Samples"))
        os.makedirs(os.path.join(self.path, str(iib_address)+"\\"+str(test_number)+"\\Plots"))

        span = maximum - minimum
        self.total_steps = round(span/step) + 1
        print("Starting test...")
        ldc.scpi.enable_output()
#       Loop to read the ground leakage in each step
        for i in range(int(self.total_steps)):
            if direction:
                current = maximum - (i*step)
            else:
                current = minimum + (i*step)
            ldc.scpi.set_current(current)
            print("Values for {0:.3f} mA".format(current*1000))
            print('--'*20)
            time.sleep(0.15)
            ldc.read_ground_leakage(duration, iib_address)
            # Change to the created directories and saves all acquired information
            os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(test_number)+"\\Plots"))
            ldc.save_graph(graph_name='Leakage Current Measurement, Iref = {0:.1f}mA'.format(current*1000))
            os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(test_number)+"\\Samples"))
            ldc.save_csv_file(file_name='Leakage_Current_Measurement-Iref_{0:.1f}mA'.format(current*1000))
            os.chdir(cwd)
            self.total_mean.append(ldc.mean)
            self.total_error.append(ldc.mean_error)
            self.total_std.append(ldc.std_dev)
            self.total_current.append(current*1000)
            self.total_ppc.append(ldc.ppc)
            if (i*step) < span:
                if direction:
                    print("Acquisitions at {0:.3f} mA done! Stepping down the current source...\n".format(current*1000))
                else:
                    print("Acquisition at {0:.3f} mA done! Stepping up the current source...\n" .format(current*1000))
            elif (i*step) == span:
                print("Accuracy Test completed!")
        ldc.scpi.disable_output()
        AccuracyTest.save_graphics(self)
        AccuracyTest.save_csv_files(self)

    def save_graphics(self):
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
        plt.title('Source Current X Mean Leakage Current')
        os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(self.testnum)+"\\Plots"))
        jpgname = 'SourceCurrent_X_MeanLeakageCurrent.jpg'
        plt.legend()
        plt.savefig(jpgname)
        plt.close()
        os.chdir(cwd)
        print("Graphic file named '{}' successfully saved!".format(jpgname))

        # Saves the Plot of Source Current X Mean Current Error
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=20)
        ax.plot(self.total_current, self.total_error)
        plt.xlabel('Source Current [mA]')
        plt.ylabel('Mean Current Error [mA]')
        plt.title('Source Current X Mean Current Error')
        os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(self.testnum)+"\\Plots"))
        jpgname = 'SourceCurrent_X_MeanCurrentError.jpg'
        plt.savefig(jpgname)
        plt.close()
        os.chdir(cwd)
        print("Graphic file named '{}' successfully saved!".format(jpgname))

        # Saves the Plot of Source Current X Current Standard Deviation
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=20)
        ax.plot(self.total_current, self.total_std)
        plt.xlabel('Source Current [mA]')
        plt.ylabel('Leakage Current Standard Deviation [mA]')
        plt.title('Source Current X Current Standard Deviation')
        os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(self.testnum)+"\\Plots"))
        jpgname = 'SourceCurrent_X_CurrentStandardDeviation.jpg'
        plt.savefig(jpgname)
        plt.close()
        os.chdir(cwd)
        print("Graphic file named '{}' successfully saved!".format(jpgname))

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
        os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(self.testnum)+"\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' successfully saved!".format(csvname))

        # Saves the csv file of Source Current and the Mean Error of Current data
        csvname = 'SourceCurrent_X_CurrentMeanError.csv'
        data = [['Source Current'], ['Current Mean Error']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.total_error)):
            column0.append(self.total_current[row])
            column1.append(self.total_error[row])
        os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(self.testnum)+"\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' successfully saved!".format(csvname))

        # Saves the csv file of Source Current and Current Standard Deviation data
        csvname = 'SourceCurrent_X_CurrentStandardDeviation.csv'
        data = [['Source Current'], ['Current Standard Deviation']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.total_std)):
            column0.append(self.total_current[row])
            column1.append(self.total_std[row])
        os.chdir(os.path.join(self.path, str(iib_address)+"\\"+str(self.testnum)+"\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' successfully saved!".format(csvname))


if __name__ == '__main__':
    acc = AccuracyTest()
    test_name = str(input("Enter the test name: "))
    folder_path = askdirectory(title='Select Folder')
    acc.path = os.path.join(folder_path, test_name)
    os.makedirs(acc.path)
    test_date = datetime.today().strftime("%d/%m/%Y - %H:%M")
    # Saves a file with the test information
    os.chdir(acc.path)
    info_file = open('INFO.txt', 'w+')
    info_file.write(test_name+"\n"+test_date+"\nSEI - Electronics Systems and Instrumentation")
    info_file.close()
    os.chdir(cwd)
    tminimum = float(input("Enter the minimum current of the test, in Amperes: "))
    tmaximum = float(input("Enter the maximum current of the test, in Amperes: "))
    tstep = float(input("Enter the current step, in Amperes: "))
    tduration = int(input("Enter the duration of the measurement steps, in seconds: "))
    direction = int(input("Enter the test direction: 0 (Ascending) or 1 (Descending): "))
    apply_degauss = int(input("Apply the degaussing process? 1 (Yes) or 0 (No):"))
    test_quantity = int(input("How many times do want to run this test?: "))
    boards_quantity = int(input("How many channels are to be tested?"))
    print(test_quantity, " tests to go!")

    if boards_quantity == 4:
        iib_address_list = [69, 85, 101, 117]
    elif boards_quantity == 3:
        iib_address_list = [69, 85, 101]
    elif boards_quantity == 2:
        iib_address_list = [69, 85]
    elif boards_quantity == 1:
        iib_address_list = [69]
    else:
        print("Out of range choice \n","Choose from 1 to 4")
        boards_quantity=0
        exit()
    for address in iib_address_list:
        iib_address = address
        for n in range(test_quantity):
            if apply_degauss:
                ldc.degauss()
            acc.total_mean.clear()
            acc.total_error.clear()
            acc.total_std.clear()
            acc.total_current.clear()
            acc.total_ppc.clear()
            acc.start(tstep, tminimum, tmaximum, tduration, n+1, iib_address)
            print(test_quantity-n-1, " tests remaining !")
