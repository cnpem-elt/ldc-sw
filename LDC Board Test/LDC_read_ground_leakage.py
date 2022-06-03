import matplotlib.pyplot as plt
import numpy as np
import time
import pydrs

drs = pydrs.SerialDRS()
drs.connect('COM10')


def read_ground_leakage(duration=1, iib_address=69):

    list_samples = []
    t = []

    fs = 10
    dt = 1/fs

    print('\n Reading samples...\n')
    for i in range(int(fs*duration)):
        list_samples.append(drs.read_bsmp_variable(iib_address, 'float'))
        t.append(i*dt)

        time.sleep(1/fs)

    np_samples = np.array(list_samples)

    print("Mean: {:.3e} A".format(np_samples.mean()))
    print("Max: {:.3e} A".format(np_samples.max()))
    print("Min: {:.3e} A".format(np_samples.min()))
    print(
        "Peak to peak: {:.3e} A\n".format(np_samples.max() - np_samples.min())
         )

    plt.plot(t, list_samples)
    plt.grid()
    plt.xlabel('Time [s]')
    plt.ylabel('Ground leakage [A]')
    plt.show()
