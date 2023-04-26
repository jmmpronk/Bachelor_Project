from pycbc.waveform import get_fd_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower

f_low = 30
sample_rate = 4

for i in range(0, 20):
    ecc = i/100
# Generate the two waveforms to compare
    hp, hc = get_fd_waveform(approximant="TaylorF2",
                            mass1=10,
                            mass2=10,
                            f_lower=f_low,
                            delta_f=1.0/sample_rate)

    sp, sc = get_fd_waveform(approximant="TaylorF2Ecc",
                            mass1=10,
                            mass2=10,
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
    print('The match is: {:.4f}'.format(m))
