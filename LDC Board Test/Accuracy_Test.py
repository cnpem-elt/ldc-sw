# coding utf-8
# LDC Board Test

import matplotlib.pyplot as plt
import numpy as np
import os
import time
from datetime import datetime
from LDC_Commands import LDC

# Gets the current directory to save the test data
cwd = os.getcwd()

# LDC Functions start
ldc = LDC()


# Accuracy Test Properties and Functions
class AccuracyTest:
    def __init__(self):
        self.total_mean = []
        self.total_error = []
        self.total_std = []
        self.total_current = []
        self.total_ppc = []
        self.test_name = ''
        print("Accuracy Test module activated!")

    def start(self, step, minimum, maximum, duration):
        # Prepare the directories and starting values
        test_date = datetime.today().strftime("_%d_%m_%Y-%H_%M")
        self.test_name = "AccuracyTest"+test_date
        os.makedirs(os.path.join(cwd, self.test_name))
        os.makedirs(os.path.join(cwd, self.test_name+"\\Samples"))
        os.makedirs(os.path.join(cwd, self.test_name+"\\Plots"))
        span = maximum - minimum
        total_steps = round(span / step) + 1
        # Do the tests for every specified step
        print("Starting test...")
        ldc.scpi.enable_output()
        for i in range(int(total_steps)):
            print("Setting current value...")
            current = minimum + (i * step)
            ldc.scpi.set_current(current)
            time.sleep(0.15)
            print("Waiting for acquisition...\n")
            print("Values for {0:.3f} mA".format(current * 1000))
            print('--' * 20)
            ldc.read_ground_leakage(duration)
            print('--' * 20)
            # Save the files in the requested directories
            os.chdir(os.path.join(cwd, self.test_name+"\\Plots"))
            ldc.save_graphic()
            os.chdir(os.path.join(cwd, self.test_name+"\\Samples"))
            ldc.save_csv_file()
            os.chdir(cwd)
            self.total_mean.append(ldc.mean)
            self.total_error.append(ldc.mean_error)
            self.total_std.append(ldc.std_dev)
            self.total_current.append(current * 1000)
            self.total_ppc.append(ldc.ppc)
            if (i * step) < span:
                print("Acquisition completed! Moving for next step...\n")
            elif (i * step) == span:
                print("Accuracy Test completed!")
        ldc.scpi.disable_output()

        # Saves the Plot of Source Current X Leakage Current Mean
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=20)
        ax.plot(self.total_current, self.total_mean, label='Source Current')
        plt.xlabel('Source Current [mA]')
        plt.ylabel('Leakage Current Mean [mA]')
        plt.title('Source Current X Leakage Current Mean')
        os.chdir(os.path.join(cwd, self.test_name + "\\Plots"))
        jpgname = 'SourceCurrent_X_LeakageCurrentMean.jpg'
        plt.savefig(jpgname)
        os.chdir(cwd)
        print("Graphic file named '{}' saved successfully!".format(jpgname))

        # Saves the Plot of Source Current X Current Error Mean
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=20)
        ax.plot(self.total_current, self.total_error)
        plt.xlabel('Source Current [mA]')
        plt.ylabel('Leakage Current Error Mean [mA]')
        plt.title('Source Current X Leakage Current Mean')
        os.chdir(os.path.join(cwd, self.test_name + "\\Plots"))
        jpgname = 'SourceCurrent_X_CurrentErrorMean.jpg'
        plt.savefig(jpgname)
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
        os.chdir(os.path.join(cwd, self.test_name + "\\Plots"))
        jpgname = 'SourceCurrent_X_CurrentStandardDeviation.jpg'
        plt.savefig(jpgname)
        os.chdir(cwd)
        print("Graphic file named '{}' saved successfully!".format(jpgname))

        # Saves the csv file of Source Current and Leakage Current Mean data
        csvname = 'SourceCurrent_X_LeakageCurrentMean.csv'
        data = [['Source Current'], ['Leakage Current Mean']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.total_mean)):
            column0.append(self.total_current[row])
            column1.append(self.total_mean[row])
        os.chdir(os.path.join(cwd, self.test_name + "\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' saved successfully!".format(csvname))

        # Saves the csv file of Source Current and Current Error Mean data
        csvname = 'SourceCurrent_X_CurrentErrorMean.csv'
        data = [['Source Current'], ['Current Error Mean']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(self.total_error)):
            column0.append(self.total_current[row])
            column1.append(self.total_error[row])
        os.chdir(os.path.join(cwd, self.test_name + "\\Samples"))
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
        os.chdir(os.path.join(cwd, self.test_name + "\\Samples"))
        np.savetxt(csvname, [p for p in zip(column0, column1)], delimiter=',', fmt='%s')
        os.chdir(cwd)
        print("CSV file named '{}' saved successfully!".format(csvname))
