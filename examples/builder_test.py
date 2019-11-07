from SignalBuilder import SignalBuilder

S = SignalBuilder()
start_time = 0
end_time = 10
S.signalStart = start_time
S.signalEnd = end_time

S.report()

S.insertNode(1, 1.5)
S.insertNode(2, 3.5)
S.insertNode(3, 6)
S.insertNode(4, 8)

pieces = S.pieces
pieces[1].func.setValue(2)
pieces[3].func.setValue(-2.5)
pieces[2].fType = 'square'
pieces[2].func.setAmplitude(0.5)
pieces[2].func.setDutyCycle(0.7)
pieces[3].fType = 'sinusoid'
pieces[3].func.setAmplitude(0.25)
pieces[3].func.setVShift(1)
pieces[4].fType = 'ramp'
pieces[4].getFunc().setTimeRange([8, 10])
S.report()

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

freq = 50
S.sampleFrequency = freq

num_samples = (end_time - start_time) * freq
t = np.linspace(start_time, end_time, num=num_samples)
y = np.zeros(num_samples)

# Plot
t, Y, nodes = S.genPiecew()
plt.plot(t, Y, '-', color='k')
for xc in nodes:
    plt.axvline(x=xc, linewidth=0.5, linestyle='--', color='m')
plt.show()

# Move a Node
S.setNodeTime(1, 2)

t, Y, nodes = S.genPiecew()
plt.plot(t, Y, '-', color='k')
for xc in nodes:
    plt.axvline(x=xc, linewidth=0.5, linestyle='--', color='m')
plt.show()

# Delete a Node
S.deleteNode(4)

t, Y, nodes = S.genPiecew()
plt.plot(t, Y, '-', color='k')
for xc in nodes:
    plt.axvline(x=xc, linewidth=0.5, linestyle='--', color='m')
plt.show()