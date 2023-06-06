import numpy as np
import matplotlib.pyplot as plt
from pycbc.waveform import get_fd_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower

f_low = 40
sample_rate = 4

def match_waveform(ecc, M_tot):
    M_1 = M_tot / 2
    M_2 = M_tot / 2

    spin = 0

    # Generate the two waveforms to compare
    hp, hc = get_fd_waveform(
        approximant="TaylorF2",
        mass1=M_1,
        mass2=M_2,
        spin1z=spin,
        spin2Z=spin,
        f_lower=f_low,
        delta_f=1.0 / sample_rate,
    )

    sp, sc = get_fd_waveform(
        approximant="TaylorF2Ecc",
        mass1=M_1,
        mass2=M_2,
        spin1z=spin,
        spin2Z=spin,
        f_lower=f_low,
        delta_f=1.0 / sample_rate,
        eccentricity=ecc,
    )

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



X = np.random.rand(100) * 0.2
Y = np.random.rand(100) * 90 + 10

f2 = np.vectorize(match_waveform)
Z = f2(X, Y)
