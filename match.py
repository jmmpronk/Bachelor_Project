import matplotlib.pyplot as pp
from pycbc.waveform import get_fd_waveform
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower

f_low = 40
sample_rate = 4

eccentricity = []
wave_match = []

N = 100
for i in range(0, N+1):
    ecc = (i/N) * 0.2
    # Generate the two waveforms to compare
    hp, hc = get_fd_waveform(approximant="TaylorF2Ecc",
                            mass1=10,
                            mass2=10,
                            spin1z = 1,
                            spin2z = 1,
                            f_lower=f_low,
                            delta_f=1.0/sample_rate,
                            eccentricity=ecc,
                            EccSpin=0)

    sp, sc = get_fd_waveform(approximant="TaylorF2Ecc",
                            mass1=10,
                            mass2=10,
                            spin1z = 1,
                            spin2z = 1,
                            f_lower=f_low,
                            delta_f=1.0/sample_rate,
                            eccentricity=ecc,
                            EccSpin=1)

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
    print('The match is: {:f}'.format(m))

    eccentricity.append(ecc)
    wave_match.append(m)

pp.plot(eccentricity, wave_match)

pp.xlabel("eccentricity")
pp.ylabel("match")
pp.xlim(0, 0.2)
pp.savefig("TF2Ecc-match.png")