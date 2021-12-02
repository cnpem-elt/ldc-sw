# coding utf-8
# LDC Board Test


import csv
import matplotlib.pyplot as plt
import numpy as np
import pydrs
import pyvisa as visa
import time

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

    def measure(self):
        voltage_value = self.instrument.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        current_value = self.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        print("Output Voltage: %.3fV\nOutput Current: %.3fA" % (voltage_value[0], current_value[0]))


# SCPI Communication module start
instrument = input("Insert instrument id: ")
scpi = SCPI(instrument)


def read_ground_leakage(duration, save_img, save_csv):
    frequency = 10
    period = 1 / frequency
    samples = []
    time_samples = []
    error = []
    for x in range(int(frequency * duration)):
        current_value = scpi.instrument.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        samples.append(drs.read_bsmp_variable(53, 'float'))
        time_samples.append(str(round(x * period, 2)))
        error.append(current_value[0] - samples[x])
        time.sleep(period)
    np_samples = np.array(samples)
    np_error = np.array(error)
    print("Mean: {0:.3f} mA".format(np_samples.mean() * 1000))
    print("Maximum: {0:.3f} mA".format(np_samples.max() * 1000))
    print("Minimum: {0:.3f} mA".format(np_samples.min() * 1000))
    print("Peak to peak: {0:.3f} mA".format((np_samples.max() - np_samples.min()) * 1000))
    print("Mean Error: {0:.3f} mA".format(abs((np_error.mean()) * 1000)))
    print("Standard Deviation: {0:.3f} mA\n".format(np_samples.std() * 1000))
    plt.plot(time_samples, samples)
    plt.xlabel('Time [s]')
    plt.ylabel('Leakage Current [A]')
    plt.title('Leakage Current')
    if save_img == 1:
        plt.savefig('leakage.png')
        print("Graphic saved successfully!")
        print("Ground Leakage Measure Finished!")
    elif save_img == 0:
        plt.show()
        print("Ground Leakage measure finished!")
    else:
        print("Invalid input!\nInsert 1 for saving the graphics or insert 0 for printing it.")
    if save_csv == 1:
        data = [['Leakage Current'], ['Time']]
        column0 = data[0]
        column1 = data[1]
        for row in range(len(samples)):
            column0.append(samples[row])
            column1.append(time_samples[row])
        with open('samples.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print("Samples saved to csv file.")
    elif save_csv == 0:
        print("Samples will not be saved to a csv file.")
    else:
        print("Invalid input!\nInsert 1 for saving the samples or insert 0 to skip.")


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
            print('--'*20)
            read_ground_leakage(10, 0, 0)
            print('--' * 20)
            if (i * step) < span:
                print("Acquisition completed! Moving for next step...\n")
            elif (i * step) == span:
                print("Accuracy Test completed!")
        scpi.disable_output()
