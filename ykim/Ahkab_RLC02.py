import numpy as np
import math
import ahkab
from ahkab import ahkab, circuit, time_functions

mycircuit = circuit.Circuit(title="Butterworth Example circuit", filename=None)

gnd = mycircuit.get_ground_node()



mycircuit.add_resistor("R1", n1="%s", n2="n2", value=100 % ('n1'))
mycircuit.add_inductor("L1", n1="n2", n2="n3", value=0)
mycircuit.add_capacitor("C1", n1="n3", n2=gnd, value=1.5e-10)



voltage_step = time_functions.pulse(v1=0, v2=1, td=0.1e-6, tr=1e-12, pw=0.5e-6, tf=1e-12, per=1.0e-6)
mycircuit.add_vsource("V1", n1="n1", n2=gnd, dc_value=5, ac_value=1, function=voltage_step)


print mycircuit

# op_analysis = ahkab.new_op()
ac_analysis = ahkab.new_ac(start=1e6, stop=1e10, points=1e2)
tran_analysis = ahkab.new_tran(tstart=0, tstop=1e-6, tstep=0.01e-6, x0=None)

# r = ahkab.run(mycircuit, an_list=[op_analysis, ac_analysis, tran_analysis])
r = ahkab.run(mycircuit, an_list=[ac_analysis, tran_analysis])


import pylab

fig = pylab.figure()
pylab.title(mycircuit.title + " - TRAN Simulation")
pylab.plot(r['tran']['T']*1e6, r['tran']['VN1'], label="Input voltage")
pylab.hold(True)
pylab.plot(r['tran']['T']*1e6, r['tran']['VN3'], label="output voltage")
pylab.legend()
pylab.hold(False)
pylab.grid(True)
# pylab.ylim([0,2.0])
# pylab.xlim([0,16])
pylab.ylabel('Step response')
pylab.xlabel('Time [us]')
fig.savefig('tran_plot.png')



fig = pylab.figure(figsize=(6,9))

pylab.subplot(311)
pylab.semilogx(r['ac']['f'], np.abs(r['ac']['Vn3']), 'o-')
pylab.ylabel('abs(V(n3)) [V]')
pylab.title(mycircuit.title + " - AC Simulation")
pylab.grid(which ='both')

pylab.subplot(312)
pylab.semilogx(r['ac']['f'], 10*np.log(np.abs(r['ac']['Vn3'])/np.abs(r['ac']['Vn1'])), 'o-')
pylab.ylabel('Gain [dB]')
# pylab.ylim(-80, 40)
pylab.grid(which ='both')

pylab.subplot(313)
pylab.grid(True)
pylab.semilogx(r['ac']['f'], np.angle(r['ac']['Vn3']), 'o-')
pylab.xlabel('Frequency [Hz]')
pylab.ylabel('arg(V(n3)) [rad]')
pylab.grid(which ='both')

fig.savefig('ac_plot.png')
pylab.show()
