# coding utf-8
# LDC Board Test

import matplotlib.pyplot as plt
import numpy as np
import os
import pydrs
import time
from datetime import datetime
from SCPICommands import SCPI

# PyDRS Communication with IIB
drs = pydrs.SerialDRS()
drs.connect('COM2')

# Gets the current directory to save the test data
cwd = os.getcwd()

# SCPI Communication module start
instrument = input("Insert instrument id: ")
scpi = SCPI(instrument)


# LDC Functions
class LDC:
    def __init__(self):
        self.frequency = 10
        self.period = 1 / self.frequency
        self.mean = 0
        self.maximum = 0
        self.minimum = 0
        self.ppc = 0
        self.mean_error = 0
        self.std_dev = 0
        self.test_time = 0
        self.samples = []
        self.time_samples = []
        self.error = []
        print("LDC functions enabled!")

    def read_ground_leakage(self, duration):
        self.samples = []
        self.time_samples = []
        self.error = []
        for x in range(int(self.frequency * duration)):
            current_value = scpi.measure_current()
            self.samples.append(drs.read_bsmp_variable(53, 'float'))
            self.time_samples.append(round(x * self.period, 2))
            self.error.append(current_value[0] - self.samples[x])
            time.sleep(self.period)
            np_samples = np.array(self.samples)
            np_error = np.array(self.error)
        self.test_time = datetime.today()
        self.mean = np_samples.mean() * 1000
        self.maximum = np_samples.max() * 1000
        self.minimum = np_samples.min() * 1000
        self.ppc = (np_samples.max() - np_samples.min()) * 1000
        self.mean_error = abs((np_error.mean()) * 1000)
        self.std_dev = np_samples.std() * 1000
        print("Mean: {0:.3f} mA".format(self.mean))
        print("Maximum: {0:.3f} mA".format(self.maximum))
        print("Minimum: {0:.3f} mA".format(self.minimum))
        print("Peak to peak: {0:.3f} mA".format(self.ppc))
        print("Mean Error: {0:.3f} mA".format(self.mean_error))
        print("Standard Deviation: {0:.3f} mA\n".format(self.std_dev))

    def save_csv_file(self):
        test_name = self.test_time.strftime('%d_%m_%Y-%H_%M_%S')
        name = test_name + '.csv'
        data = [['Leakage Current'], ['Time']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.samples)):
            column0.append(self.samples[row])
            column1.append(self.time_samples[row])
        np.savetxt(name, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        print("CSV file named '{}' saved successfully!".format(name))

    def plot_graphic(self):
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=30)
        ax.plot(self.time_samples, self.samples)
        plt.xlabel('Time [s]')
        plt.ylabel('Leakage Current [A]')
        plt.title('Leakage Current')
        plt.show()

    def save_graphic(self):
        test_name = self.test_time.strftime('%d_%m_%Y-%H_%M_%S')
        name = test_name + '.jpg'
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=30)
        ax.plot(self.time_samples, self.samples)
        plt.xlabel('Time [s]')
        plt.ylabel('Leakage Current [A]')
        plt.title('Leakage Current')
        plt.savefig(name)
        print("Graphic file named '{}' saved successfully!".format(name))


# LDC Functions module start
ldc = LDC()


# Accuracy Test Properties and Functions
class AccuracyTest:
    def __init__(self):
        self.total_mean = []
        self.total_error = []
        self.total_std = []
        self.total_current = []
        self.total_ppc = []
        print("Accuracy Test module activated!")

    def start(self, step, minimum, maximum):
        test_date = datetime.today().strftime("_%d_%m_%Y-%H_%M")
        test_name = "AccuracyTest"+test_date
        os.makedirs(os.path.join(cwd, test_name))
        os.makedirs(os.path.join(cwd, test_name+"\\Samples"))
        os.makedirs(os.path.join(cwd, test_name+"\\Plots"))
        span = maximum - minimum
        total_steps = round(span / step) + 1
        print("Starting test...")
        scpi.enable_output()
        for i in range(int(total_steps)):
            print("Setting current value...")
            current = minimum + (i * step)
            scpi.set_current(current)
            time.sleep(0.15)
            print("Waiting for acquisition...\n")
            print("Values for {0:.3f} mA".format(current * 1000))
            print('--' * 20)
            ldc.read_ground_leakage(10)
            print('--' * 20)
            # Save the files in the requested directories
            os.chdir(os.path.join(cwd, test_name+"\\Plots"))
            ldc.save_graphic()
            os.chdir(os.path.join(cwd, test_name+"\\Samples"))
            ldc.save_csv_file()
            os.chdir(cwd)
            self.total_mean.append(ldc.mean)
            self.total_error.append(ldc.mean_error)
            self.total_std.append(ldc.std_dev)
            self.total_current.append(current)
            self.total_ppc.append(ldc.ppc)
            if (i * step) < span:
                print("Acquisition completed! Moving for next step...\n")
            elif (i * step) == span:
                print("Accuracy Test completed!")
        scpi.disable_output()
