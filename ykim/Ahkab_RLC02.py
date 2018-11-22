import numpy as np
import math
import ahkab
from ahkab import ahkab, circuit, time_functions

mycircuit = circuit.Circuit(title="TWMZM equivalent circuit", filename=None)

gnd = mycircuit.get_ground_node()

n = 6
for i in range(1, n+1):

    #Transmission line (Passive segment)
    mycircuit.add_resistor("Rl%s" %(i), n1="n%s" %(4*i-3), n2="n%s" %(4*i-2), value=1.65)
    mycircuit.add_inductor("Ll%s" %(i), n1="n%s" %(4*i-2), n2="n%s" %(4*i-1), value=1.27e-10)
    mycircuit.add_capacitor("Cl%s" %(i), n1="n%s" %(4*i-1), n2=gnd, value=2.24e-14)
    mycircuit.add_resistor("Gl%s" %(i), n1="n%s" %(4*i-1), n2=gnd, value=8e3)

    Rs = 60.05#60.05
    Cj = 82e-15#82e-15

    #Phase shifter (Active segment)
    mycircuit.add_resistor("Rs%s" % (i), n1="n%s" %(4*i-1), n2="n%s" %(4*i+1), value=Rs)
    mycircuit.add_capacitor("Cj%s" % (i), n1="n%s" %(4*i+1), n2=gnd, value=Cj)
    mycircuit.add_resistor("Rsub%s" % (i), n1="n%s" %(4*i-1), n2="n%s" %(4*i), value=20.28)
    mycircuit.add_capacitor("Cox%s" % (i), n1="n%s" %(4*i), n2=gnd, value=4.09e-14)

mycircuit.add_resistor("Rt", n1="n%s" %(4*i+1), n2=gnd, value=25.0)



# voltage_step = time_functions.pulse(v1=0, v2=1, td=500e-9, tr=1e-12, pw=1, tf=1e-12, per=2)
voltage_step = time_functions.pulse(v1=0, v2=0.1, td=0.1e-6, tr=1e-12, pw=0.5e-6, tf=1e-12, per=1.0e-6)
mycircuit.add_vsource("V1", n1="n1", n2=gnd, dc_value=0, ac_value=0.05, function=voltage_step)

print mycircuit

# op_analysis = ahkab.new_op()
ac_analysis = ahkab.new_ac(start=1e7, stop=1e10, points=1e2)
# tran_analysis = ahkab.new_tran(tstart=0, tstop=14e-6, tstep=0.1e-6, x0=None)

# r = ahkab.run(mycircuit, an_list=[op_analysis, ac_analysis, tran_analysis])
r = ahkab.run(mycircuit, an_list=[ac_analysis])


import pylab
#
# fig = pylab.figure()
# pylab.title(mycircuit.title + " - TRAN Simulation")
# pylab.plot(r['tran']['T']*1e6, r['tran']['VN1'], label="Input voltage")
# pylab.hold(True)
# pylab.plot(r['tran']['T']*1e6, r['tran']['VN3'], label="output voltage")
# pylab.legend()
# pylab.hold(False)
# pylab.grid(True)
# pylab.ylim([0,2.0])
# pylab.xlim([0,16])
# pylab.ylabel('Step response')
# pylab.xlabel('Time [us]')
# fig.savefig('tran_plot.png')



fig = pylab.figure(figsize=(8,9))

# node = '3'
node = str(4*n+1)

pylab.subplot(311)
pylab.title(mycircuit.title + " - AC Simulation")
pylab.semilogx(r['ac']['f'], 10*np.log(np.abs(r['ac']['Vn'+node])/np.abs(r['ac']['Vn1'])), 'o-')
pylab.ylabel('Gain(V(n'+node+') [dB]')
# pylab.ylim(-25, 0)
pylab.grid(which ='both')

pylab.subplot(312)
pylab.semilogx(r['ac']['f'], np.abs(r['ac']['Vn'+node]), 'o-')
pylab.ylabel('abs(V(n'+node+')) [V]')
pylab.grid(which ='both')

pylab.subplot(313)
pylab.grid(True)
pylab.semilogx(r['ac']['f'], np.angle(r['ac']['Vn'+node]), 'o-')
pylab.xlabel('Frequency [Hz]')
pylab.ylabel('arg(V(n'+node+')) [rad]')
pylab.grid(which ='both')

fig.savefig('ac_plot.png')
pylab.show()
