import matplotlib.pyplot as plt
import numpy as np
import time
import pydrs

drs = pydrs.SerialDRS()
drs.connect('COM2')
def read_ground_leakage(duration = 1):

    list_samples = []
    t = []

    fs = 10
    dt = 1/fs

    print('\n Lendo amostras...\n')
    for i in range(int(fs*duration)):

        list_samples.append(drs.read_bsmp_variable(53,'float'))
        t.append(i*dt)

        time.sleep(1/fs)


    np_samples = np.array(list_samples)

    print("Media: {:.3e} A".format(np_samples.mean()))
    print("Max: {:.3e} A".format(np_samples.max()))
    print("Min: {:.3e} A".format(np_samples.min()))
    print("Pico a pico: {:.3e} A\n".format(np_samples.max() - np_samples.min()))

    plt.plot(t, list_samples)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Ground leakage [A]')
    plt.show()
