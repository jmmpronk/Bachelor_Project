import matplotlib.pyplot as pp
import numpy as np
from pycbc import types, fft, waveform

sptilde, sctilde = waveform.get_fd_waveform(approximant="TaylorF2Ecc",
                            mass1=10,
                            mass2=10,
                            spin1z = 1,
                            spin2z = 1,
                            f_lower=40,
                            delta_f=1.0/4,
                            eccentricity=0.2)


print(sctilde)

f=open("CHECK_check.dat","w")

f.write(str(sctilde))

f.close()