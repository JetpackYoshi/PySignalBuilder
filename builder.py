# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 21:18:49 2019

@author: Yoshin
"""

import matplotlib.pyplot as plt
from bisect import bisect
from scipy import interpolate
import numpy as np


class Node:
    def __init__(self, time, left_piece=None, right_piece=None, nType='normal'):
        if left_piece is not None:
            self.setLeft(left_piece)
        else:
            self._left = None

        if right_piece is not None:
            self.setRight(right_piece)
        else:
            self._right = None

        self.setnType(nType)
        self.setTime(time)

    def setnType(self, nType):
        self._nType = nType

    def nType(self):
        return self._nType

    def setTime(self, time):
        self._time = time

    def time(self):
        return self._time

    def setLeft(self, left_piece):
        self._left = left_piece

    def setRight(self, right_piece):
        self._right = right_piece

    def left(self):
        return self._left

    def right(self):
        return self._right


class Piece:
    fType = None
    def __init__(self, start_node=None, end_node=None, fType='constant'):
        self._funcs = {
                'constant': Constant(),
                'ramp': Ramp(),
                'sinusoid': Sinusoid(),
                'square': None
                }
        
        self.setfType(fType)
        self.setStart(start_node)
        self.setEnd(end_node)
        
    def addFunc(self, key, func):
        self._funcs[key] = func
        
    def getFunc(self, fType = None):
        if fType is not None:
            return self._funcs[fType]
        else:
            return self._funcs[self._fType]
        
    def setfType(self, fType):
        self._fType = fType

    def setStart(self, start_node):
        self._startNode = start_node

        if self._startNode is not None:
            self._startNode.setRight(self)

    def setEnd(self, end_node):
        self._endNode = end_node

        if self._endNode is not None:
            self._endNode.setLeft(self)

    def valid(self, x):
        return (x >= self._startNode.time()) & (x<self._endNode.time())


class Sinusoid:
    def __init__(self, amplitude=1, frequency=1, vertical_shift=0, phase_shift=0):
        self._amplitude = amplitude
        self._frequency = frequency
        self._vShift = vertical_shift
        self._phaseShift = phase_shift

    def setAmplitude(self, amplitude):
        self._amplitude = amplitude

    def setFrequency(self, frequency):
        self._frequency = frequency

    def setVShift(self, vertical_shift):
        self._vShift = vertical_shift

    def setPhase(self, phase_shift):
        self._phaseShift = phase_shift

    def exec_(self, x):
        y = self._amplitude * np.sin((2 * np.pi * self._frequency) * (x - self._phaseShift)) + self._vShift
        return y

class Square:
    pass


class Ramp:
    def __init__(self, startVal=0, endVal=1, rate=1, vShift=0, mode='rate'):
        self._startVal = startVal
        self._endVal = endVal
        self._slope = rate
        self._vShift = vShift
        self._mode = mode
    
    def setMode(self, mode):
        self._mode = mode
    
    def exec_(self, x):
        if self._mode is 'rate':
            return self._slope*x + self._vShift

class Constant:
    def __init__(self, value=0):
        self._value = value
        
    def setValue(self, value):
        self._value = value
        
    def exec_(self, x):
        return self._value
    
def genPiecew(t,pieces):
    fun = np.piecewise(t,[piece.valid(t) for piece in pieces],[piece.getFunc().exec_ for piece in pieces])
    return fun
    


if __name__ == '__main__':
    start_time = 0
    end_time = 8
    freq = 500
    num_samples = (end_time-start_time)*freq
    t = np.linspace(start_time, end_time, num=num_samples)
    y = np.zeros(num_samples)
    
    n1 = Node(0, nType='Start')
    n2 = Node(2)
    n3 = Node(4)
    n4 = Node(6, nType='End')

    p1 = Piece(n1, n2, fType='ramp')
    p2 = Piece(n2, n3)
    p2.getFunc().setValue(4)
    p3 = Piece(n3, n4, 'sinusoid')
    p3.getFunc().setFrequency(5)
    p3.getFunc().setAmplitude(0.5)
    
    Y = genPiecew(t,[p1,p2,p3])
    
    plt.plot(t,Y)
    plt.xlim([start_time,end_time])
    #plt.axvspan(0, 7.5, color='green', alpha=0.2)
    plt.show()