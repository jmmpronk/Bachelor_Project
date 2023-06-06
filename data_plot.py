import numpy as np
import matplotlib.pyplot as plt

master = np.loadtxt('master_time.dat')

eccspin = np.loadtxt('spin_time.dat')

time = master[:, 0]

master_waveform = master[:, 1]

eccspin_waveform = eccspin[:, 1]

plt.plot(time, master_waveform, label="without terms")
plt.plot(time, eccspin_waveform, label="with terms")
plt.legend()
plt.savefig("TF2Ecc-comparison")