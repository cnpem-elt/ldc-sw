# coding utf-8
# LDC Board Test

import matplotlib.pyplot as plt
import numpy as np
import pydrs
import pyvisa as visa
import time

# PyDRS Communication with IIB for leakage current measurement
drs = pydrs.SerialDRS()
drs.connect('COM2')

# Reads Ground Leakage Current
def read_ground_leakage(duration):
    samples = []
    error = []
    total_mean = []
    total_error = []
    total_std = []
    total_current = []
    t = []
    frequency = 10
    period = 1 / frequency
    temp_values = instr.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
    current1 = temp_values[0]
    total_current.append(current1)
    for x in range(int(frequency * duration)):
        samples.append(drs.read_bsmp_variable(53, 'float'))
        t.append(x * period)
        error.append(current1 - samples[x])
        time.sleep(period)
    np_samples = np.array(samples)
    np_error = np.array(error)
    print("Mean: {0:.3f} mA".format(np_samples.mean() * 1000))
    print("Maximum: {0:.3f} mA".format(np_samples.max() * 1000))
    print("Minimum: {0:.3f} mA".format(np_samples.min() * 1000))
    print("Peak to peak: {0:.3f} mA".format((np_samples.max() - np_samples.min()) * 1000))
    print("Mean Error: {0:.3f} mA".format(abs((np_error.mean()) * 1000)))
    print("Standard Deviation: {0:.3f} mA".format(np_samples.std() * 1000))
    total_mean.append(np_samples.mean())
    total_error.append(np_error.mean())
    total_std.append(np_samples.std())
    # leakage Current Graph
    plt.plot(t, samples)
    plt.xlabel('Time [s]')
    plt.ylabel('Leakage Current [A]')
    plt.title('Leakage Current')
    plt.savefig('leakage.png')


# SCPI Commands for instrument basic communication
# -------------------------------------------------------------------------------
def get_instruments():
    rm = visa.ResourceManager()
    instruments = list(rm.list_resources())
    for i in range(len(instruments)):
        print('Instrument %s: %s' % (i + 1, instruments[i]))


def connect(equipment_id):
    rm = visa.ResourceManager()
    global instr
    instr = rm.open_resource(equipment_id)
    print('Instrument connected successfully!')


def set_voltage(voltage):
    instr.write(':SOURce1:FUNCtion:MODE %s' % 'VOLTage')
    instr.write(':SOURce1:VOLTage:LEVel:IMMediate:AMPLitude %G' % voltage)
    temp_values = instr.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
    voltage1 = temp_values[0]
    print("The supply voltage is set to %.3fV" % voltage)
    voltage_values = instr.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
    voltage1 = voltage_values[0]
    print("Output Voltage: %.3fV" % voltage1)


def set_current(current):
    instr.write(':SOURce1:FUNCtion:MODE %s' % 'CURRent')
    instr.write(':SOURce1:CURRent:LEVel:IMMediate:AMPLitude %G' % current)
    temp_values = instr.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
    current1 = temp_values[0]
    print("The source current is set to %.3fA" % current)
    current_values = instr.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
    current1 = current_values[0]
    print("Output Current: %.3fA" % current1)


def enable_output():
    instr.write(':OUTPut1:STATe %d' % 1)
    print("Output enabled successfully!")


def disable_output():
    instr.write(':OUTPut1:STATe %d' % 0)
    print("Output disabled successfully!")


def measure():
    print("Which values do you want?\n(0)Voltage\n(1)Current\n(2)Both\n")
    value = int(input("Insert value: "))
    if value == 0:
        voltage_values = instr.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        voltage = voltage_values[0]
        print("Output Voltage: %.3fV" % voltage)
    elif value == 1:
        current_values = instr.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        current = current_values[0]
        print("Output Current: %.3fA" % current)
    elif value == 2:
        voltage_values = instr.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        voltage = voltage_values[0]
        current_values = instr.query_ascii_values(':MEASure:CURRent:DC? (%s)' % '@1')
        current = current_values[0]
        print("Output Voltage: %.3fV\nOutput Current: %.3fA" % (voltage, current))


# -------------------------------------------------------------------------------
def accuracy_test(step, min, max, duration):
    span = max - min
    total_steps = round(span / step) + 1
    equipment = input("Insert equipment adress: ")
    connect(equipment)
    print("Starting test...")
    enable_output()
    for i in range(int(total_steps)):
        print("Setting Current Value...")
        setted_current = min + (i * step)
        set_current(setted_current)
        voltage_values = instr.query_ascii_values(':MEASure:VOLTage:DC? (%s)' % '@1')
        voltage = voltage_values[0]
        print("Output Voltage: %.3fV" % voltage)
        print("Waiting for acquisition...")
        read_ground_leakage(duration)
        if (i * step) < span:
            print("Acquisition completed! Moving for next step...\n")
    disable_output()
    print("Accuracy Test completed!")
