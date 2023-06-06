import matplotlib.pyplot as plt
import numpy as np
from pycbc.waveform import get_fd_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower

f_low = 40
sample_rate = 4

spin = np.linspace(0, 1, 100)
ecc = np.linspace(0, 0.2, 100)

X, Y = np.meshgrid(ecc, spin)

def match_waveform(ecc, spin):

    # Generate the two waveforms to compare
    hp, hc = get_fd_waveform(approximant="TaylorF2",
                            mass1=10,
                            mass2=10,
                            spin1z=spin,
                            spin2Z=0,
                            f_lower=f_low,
                            delta_f=1.0/sample_rate)

    sp, sc = get_fd_waveform(approximant="TaylorF2Ecc",
                            mass1=10,
                            mass2=10,
                            spin1z=spin,
                            spin2Z=0,
                            f_lower=f_low,
                            delta_f=1.0/sample_rate,
                            eccentricity=ecc)

    # Resize the waveforms to the same length
    flen = max(len(sp), len(hp))
    sp.resize(flen)
    hp.resize(flen)

    # Generate the aLIGO ZDHP PSD
    delta_f = 1.0 / sample_rate
    psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)

    # Note: This takes a while the first time as an FFT plan is generated
    # subsequent calls are much faster.
    m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)
    return m


f2 = np.vectorize(match_waveform)
Z = f2(X, Y)

MM_c1 = 1 - 1/(10**2)
MM_c2 = 1 - 1/(32.4**2)

plt.imshow(Z, extent=[0, 0.2, 0, 1], origin='lower', aspect='auto')
plt.colorbar()

contours = plt.contour(X, Y, Z, levels = [0.97, MM_c1, MM_c2], colors='black')
plt.clabel(contours, inline=True, fontsize=10)

plt.xlabel("Eccentricity")
plt.ylabel("Spin")
plt.show()