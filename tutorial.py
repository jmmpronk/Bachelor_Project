import matplotlib.pyplot as pp
from pycbc.waveform import get_td_waveform_from_fd


for apx in ['TaylorF2', 'TaylorF2Ecc']:
    hp, hc = get_td_waveform_from_fd(approximant=apx,
                                 mass1=10,
                                 mass2=10,
                                 spin1z=0.9,
                                 delta_t=1.0/4096,
                                 f_lower=40)

    pp.plot(hp.sample_times, hp, label=apx)

pp.ylabel('Strain')
pp.xlabel('Time (s)')
pp.legend()
pp.show()