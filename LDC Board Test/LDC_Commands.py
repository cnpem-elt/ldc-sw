# coding utf-8
# LDC Commands

import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime


# LDC Functions
class LDC:
    def __init__(self):
        import pydrs
        from SCPI_Commands import SCPI

        # PyDRS Communication with IIB
        self.drs = pydrs.SerialDRS()
        self.drs.connect('COM2')

        # SCPI Communication module start
        instrument = input("Insert instrument id: ")
        self.scpi = SCPI(instrument)

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
            current_value = self.scpi.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
            self.samples.append((self.drs.read_bsmp_variable(53, 'float'))*1000)
            self.time_samples.append(round(x * self.period, 2))
            self.error.append(current_value[0] - self.samples[x])
            time.sleep(self.period)
            np_samples = np.array(self.samples)
            np_error = np.array(self.error)
        self.test_time = datetime.today()
        self.mean = np_samples.mean()
        self.maximum = np_samples.max()
        self.minimum = np_samples.min()
        self.ppc = (np_samples.max() - np_samples.min())
        self.mean_error = abs(np_error.mean())
        self.std_dev = np_samples.std()

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
        return "CSV file named '{}' saved successfully!".format(name)

    def plot_graphic(self):
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=30)
        ax.plot(self.time_samples, self.samples)
        plt.xlabel('Time [s]')
        plt.ylabel('Leakage Current [mA]')
        plt.title('Leakage Current')
        return plt.show()

    def save_graphic(self):
        test_name = self.test_time.strftime('%d_%m_%Y-%H_%M_%S')
        name = test_name + '.jpg'
        fig, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.locator_params(axis='y', tight=True, nbins=15)
        ax.locator_params(axis='x', tight=True, nbins=30)
        ax.plot(self.time_samples, self.samples)
        plt.xlabel('Time [s]')
        plt.ylabel('Leakage Current [mA]')
        plt.title('Leakage Current')
        plt.savefig(name)
        return "Graphic file named '{}' saved successfully!".format(name)
