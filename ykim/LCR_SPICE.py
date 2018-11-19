from scipy import signal
import numpy as np
import matplotlib.pyplot as plt



R = 10
C = 1e-9
L = 1e-5


num = [1]
den = [L * C, R * C, 1]
sys = signal.TransferFunction(num, den)


#
# num = [1]
# den = [L*L*C*C, 2*R*L*C*C, R*R*C*C+2*L*C, 2*R*C,1]
# sys = signal.TransferFunction(num, den)



w, mag, phase = sys.bode()
f = w / (2 * np.pi)
t, s = signal.step(sys, N = 500)


plt.figure(1)
plt.suptitle('LCR Frequency characteristics')

plt.subplot(211)
plt.semilogx(f, mag)
plt.grid(which ='both')
plt.ylim(-80, 40)
plt.ylabel('Gain [dB]')

plt.subplot(212)
plt.semilogx(f, phase)
plt.grid(which='both')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [deg.]')

plt.figure(2, figsize = (6, 3.8))
plt.suptitle('Response on step')
plt.plot(t * 1e+6, s)
plt.grid(which= 'both')
plt.xlabel('Time[usec]')
plt.ylabel('Amplitude')

plt.show()

