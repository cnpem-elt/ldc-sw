# coding utf-8
# LDC Board Test


import matplotlib.pyplot as plt
import numpy as np
import pydrs
import pyvisa as visa
import time
from datetime import datetime

# PyDRS Communication with IIB
drs = pydrs.SerialDRS()
drs.connect('COM2')


# SCPI Commands
class SCPI:
    def __init__(self, instrument_id):
        self.rm = visa.ResourceManager()
        self.instrument = self.rm.open_resource(instrument_id)
        print('SCPI Commands enabled!\nInstrument connected successfully!')

    def set_voltage(self, voltage):
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'VOLTage')
        self.instrument.write(':SOURce1:CURRent:LEVel:IMMediate:AMPLitude %G' % voltage)
        print("The source voltage is set to %.3fV" % voltage)
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        print("Output Voltage: %.3fV" % voltage_value[0])

    def set_current(self, current):
        self.instrument.write(':SOURce1:FUNCtion:MODE %s' % 'CURRent')
        self.instrument.write(':SOURce1:CURRent:LEVel:IMMediate:AMPLitude %G' % current)
        print("The source current is set to %.3fA" % current)
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        print("Output Current: %.3fA" % current_value[0])

    def enable_output(self):
        self.instrument.write(':OUTPut1:STATe %d' % 1)
        print("Output enabled successfully!")

    def disable_output(self):
        self.instrument.write(':OUTPut1:STATe %d' % 0)
        print("Output disabled successfully!")

    def measure_all(self):
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        print("Output Voltage: %.3fV\nOutput Current: %.3fA" % (voltage_value[0], current_value[0]))

    def measure_current(self):
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        print("Output Current: %.3fA" % current_value[0])

    def measure_voltage(self):
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        print("Output Voltage: %.3fV" % voltage_value[0])


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
            current_value = scpi.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
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
        print("Graphic file named '{}' saved successfully!")


# LDC Functions module start
ldc = LDC()


# Accuracy Test Properties and Functions
class AccuracyTest:
    def __init__(self):
        self.total_mean = []
        self.total_error = []
        self.total_std = []
        self.total_current = []
        self.test_time = []
        print("Accuracy Test module activated!")

    def start(self, step, minimum, maximum):
        span = maximum - minimum
        total_steps = round(span / step) + 1
        print("Starting test...")
        scpi.enable_output()
        for i in range(int(total_steps)):
            print("Setting current value...")
            current = minimum + (i * step)
            scpi.set_current(current)
            print("Waiting for acquisition...\n")
            print("Values for {0:.3f} mA".format(i * step * 1000))
            print('--' * 20)
            ldc.read_ground_leakage(10)
            print('--' * 20)
            if (i * step) < span:
                print("Acquisition completed! Moving for next step...\n")
            elif (i * step) == span:
                print("Accuracy Test completed!")
        scpi.disable_output()
