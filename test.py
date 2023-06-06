import matplotlib.pyplot as pp
from pycbc import types, fft, waveform



hp, hc = waveform.get_td_waveform(approximant='TaylorF2',
                            mass1=10,
                            mass2=10,
                            spin1z=0.9,
                            delta_t=1.0/4096,
                            f_lower=40)

sptilde, sctilde = waveform.get_fd_waveform(approximant="TaylorF2Ecc",
                             mass1=10, mass2=10, delta_f=1.0/4, f_lower=40, eccentricity = 0.2)

# FFT it to the time-domain
tlen = int(1.0 / hp.delta_t / sptilde.delta_f)
sptilde.resize(tlen/2 + 1)
sp = types.TimeSeries(types.zeros(tlen), delta_t=hp.delta_t)
fft.ifft(sptilde, sp)

pp.plot(sp.sample_times, sp, label="TaylorF2Ecc")
pp.plot(hp.sample_times, hp, label='TaylorF2')

pp.ylabel('Strain')
pp.xlabel('Time (s)')
pp.legend()
pp.xlim(-2, 0.2)
pp.savefig("TF2Eccspin-IFFT.png")

