# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 21:18:49 2019

@author: Yoshin
"""

import matplotlib.pyplot as plt
from bisect import bisect
from scipy import interpolate
import numpy as np
from collections import deque, OrderedDict
import itertools

class Node:
    def __init__(self, time=None, left_piece=None, right_piece=None, nType='normal'):
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
        
    def getfType(self):
        return self._fType

    def setStart(self, start_node):
        self._startNode = start_node

        if self._startNode is not None:
            self._startNode.setRight(self)
            
    def getStart(self):
        return self._startNode
    

    def setEnd(self, end_node):
        self._endNode = end_node

        if self._endNode is not None:
            self._endNode.setLeft(self)
            
    def getEnd(self):
        return self._endNode

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
    def __init__(self, startVal=0, rate=1, endVal=1, mode='rate'):
        self._startVal = startVal
        self._endVal = endVal
        self._slope = rate
        self._mode = mode
        self._timeRange = [0,0]
    
    def setMode(self, mode):
        self._mode = mode
    
    def setStartVal(self, val):
        self._startVal = val
        
    def setEndVal(self, val):
        self._endVal = val
        
    def setRate(self, rate):
        self._slope = rate
        
    def setTimeRange(self, time_range):
        self._timeRange = time_range
    
    def exec_(self, x):
        if self._mode is 'rate':
            m = self._slope
        elif self._mode is 'ps':
            m = (self._endVal - self._startVal)/(self._timeRange[1] - self._timeRange[0])
        
        return m*(x - self._timeRange[0]) + self._startVal

class Constant:
    def __init__(self, value=0):
        self._value = value
        
    def setValue(self, value):
        self._value = value
        
    def exec_(self, x):
        return self._value
    
class Function:
    _timeRange = [0, 0]
    
    def setTimeRange(start,end):
        self._timeRange = [start, end]
    
    def exec_(self, x):
        raise Exception ("Not Implemented")
    
class SignalBuilder:
    _startNode = Node(nType='start')
    _endNode = Node(nType='end')
    _nodes = [_startNode,_endNode]
    _pieces = [Piece(_startNode, _endNode)]
    _sampleFrequency = None
    
    def __init__(self):
        pass
    
    def setSampleFrequency(self, frequency):
        self._sampleFrequency = frequency
        
    def setSignalStart(self, t):
        #assert t < self._nodes[1].time(), "Invalid Time"
        self.setNodeTime(0, t)
        
    def setSignalEnd(self, t):
        #assert t > self._nodes[-2].time(), "Invalid Time"
        self.setNodeTime(len(self._nodes)-1, t)
        
    def setNodeTime(self, index, t):
        myNode = self._nodes[index]
        
        left = None
        right = None
        
        for node in self._nodes[:index][::-1]:
            if node.time() is not None:
                left = node
                
        for node in self._nodes[index+1:]:
            if node.time() is not None:
                right = node
        
        if left is not None:
            assert t > left.time(), "Invalid Time"
        if right is not None:
            assert t < right.time(), "Invalid Time"
            
        myNode.setTime(t)
        
    def getNodes(self):
        return self._nodes
    
    def getPieces(self):
        return self._pieces
        
    def insertNode(self, index, t=None):
        assert 0 < index < len(self._nodes), "Invalid Node Index"
        newNode = Node(time=t)
        newPiece = Piece()
        newPiece.setStart(newNode)
        
        self._nodes.insert(index, newNode)
        self._pieces.insert(index, newPiece)
        
        self._pieces[index-1].setEnd(newNode)
        newPiece.setEnd(self._nodes[index+1])
        
        
    def deleteNode(self, index):
        pass
        
    def trace(self, report=False):
        obj = self._startNode
        trace = []
        while 1:
            
            if type(obj) is Node:
                trace.append(obj)
                if obj.nType() is 'end':
                    break  
                obj = obj.right()
            if type(obj) is Piece:
                trace.append(obj)
                obj = obj.getEnd()
        
        return trace
    
    def checkNodeValidity(self):
        invalid = []
        for item in self.trace():
            if type(item) is Node:
                if item.time() is None:
                    invalid.append(item)
                    
        return invalid
    
    def report(self):
        for item in self.trace():
            if type(item) is Node:
                if item.nType() is 'start':
                    print("Start Node:")
                elif item.nType() is 'end':    
                    print("End Node:")
                else:
                    print("Node:")
                print("    {}".format(item))
                print("    time: {}".format(item.time()))
                print("----\n")
                
            if type(item) is Piece:
                print("Piece:")
                print("    {}".format(item))
                print("    Type: {}".format(item.getfType()))
                print("----\n")
                
    def genPiecew(self):
        print(self._endNode.time())
        num_samples = (self._endNode.time()-self._startNode.time())*self._sampleFrequency
        t = np.linspace(self._startNode.time(), self._endNode.time(), num=num_samples)
        
        condlist = [piece.valid(t) for piece in self._pieces]
        funclist = [piece.getFunc().exec_ for piece in self._pieces]
        
        node_locations = [node.time() for node in self._nodes]
        
        return t, np.piecewise(t, condlist, funclist), node_locations
                
                
               
    
def genPiecew(t,pieces):
    fun = np.piecewise(t,[piece.valid(t) for piece in pieces],[piece.getFunc().exec_ for piece in pieces])
    return fun
    


if __name__ == '__main__':
    start_time = 0
    end_time = 10
    freq = 500
    num_samples = (end_time-start_time)*freq
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
    S.setSampleFrequency(20)
    S.setSignalStart(0)
    S.setSignalEnd(10)
    S.report()
    
    S.insertNode(1, 2)
    S.insertNode(2, 4)
    S.insertNode(3, 6)
    S.insertNode(4, 8)
    
    pieces = S.getPieces()
    pieces[1].getFunc().setValue(2)
    pieces[3].getFunc().setValue(-2.5)
    pieces[2].setfType('sinusoid')
    pieces[2].getFunc().setAmplitude(0.5)
    pieces[4].setfType('ramp')
    pieces[4].getFunc().setTimeRange([8,10])
    
    t, Y, nodes = S.genPiecew()
    plt.plot(t,Y)
    for xc in nodes:
        plt.axvline(x=xc, linewidth=0.5, linestyle='--')
    plt.show()
   