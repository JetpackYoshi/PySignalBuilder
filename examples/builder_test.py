from SignalBuilder import SignalBuilder
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    start_time = 0
    end_time = 10
    freq = 500
    num_samples = (end_time - start_time) * freq
    t = np.linspace(start_time, end_time, num=num_samples)
    y = np.zeros(num_samples)

    #    n1 = Node(0, nType='Start')
    #    n2 = Node(2)
    #    n3 = Node(4)
    #    n4 = Node(6, nType='End')
    #
    #    p1 = Piece(n1, n2, fType='ramp')
    #    p1.getFunc().setStartVal(1)
    #    p2 = Piece(n2, n3)
    #    p2.getFunc().setValue(4)
    #    p3 = Piece(n3, n4, 'sinusoid')
    #    p3.getFunc().setFrequency(5)
    #    p3.getFunc().setAmplitude(0.5)
    #
    #    Y = genPiecew(t,[p1,p2,p3])
    #
    #    S = SignalBuilder()
    #
    #    plt.plot(t,Y)
    #    plt.xlim([start_time,end_time])
    #    #plt.axvspan(0, 7.5, color='green', alpha=0.2)
    #    plt.show()

    S = SignalBuilder()
    S.sampleFrequency = 50
    S.signalStart = 0
    S.signalEnd = 10
    S.report()

    S.insertNode(1, 2)
    S.insertNode(2, 4)
    S.insertNode(3, 6)
    S.insertNode(4, 8)

    pieces = S.pieces
    pieces[1].getFunc().setValue(2)
    pieces[3].getFunc().setValue(-2.5)
    pieces[2].fType = 'square'
    pieces[2].getFunc().setAmplitude(0.5)
    pieces[2].getFunc().setDutyCycle(0.7)
    pieces[4].fType = 'ramp'
    pieces[4].getFunc().setTimeRange([8, 10])

    t, Y, nodes = S.genPiecew()
    plt.plot(t, Y, '-', t, Y, '.')
    for xc in nodes:
        plt.axvline(x=xc, linewidth=0.5, linestyle='--')
    plt.show()

    S.deleteNode(4, False)

    t, Y, nodes = S.genPiecew()
    plt.plot(t, Y, '-', t, Y, '.')
    for xc in nodes:
        plt.axvline(x=xc, linewidth=0.5, linestyle='--')
    plt.show()