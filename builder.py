# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 21:18:49 2019

@author: Yoshin
"""

import matplotlib.pyplot as plt
from bisect import bisect
from scipy import interpolate, signal
import numpy as np
from collections import deque, OrderedDict
import itertools
from functions import *


class Node:
    _time = None
    _left = None
    _right = None
    _nType = 'normal'

    def __init__(self, time=None, left_piece=None, right_piece=None, nType='normal'):
        if left_piece is not None:
            self.setLeft(left_piece)
        else:
            self._left = None

        if right_piece is not None:
            self.setRight(right_piece)
        else:
            self._right = None

        self.nType = nType
        self.time = time

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @property
    def nType(self):
        return self._nType

    @nType.setter
    def nType(self, nType):
        self._nType = nType

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, left_piece):
        self._left = left_piece
        
        if self._left is not None:
            assert type(left_piece) is Piece, "Invalid Type. Must be object of type 'Piece'"
            self._left._end = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, right_piece):
        self._right = right_piece
        if self._right is not None:
            assert type(right_piece) is Piece, "Invalid Type. Must be object of type 'Piece'"
            self._right._start = self


class Piece:
    fType = None
    _fType = 'constant'
    _start = None
    _end = None

    def __init__(self, start_node=None, end_node=None, fType='constant'):
        self._funcs = {
            'constant': Constant(),
            'ramp': Ramp(),
            'sinusoid': Sinusoid(),
            'square': Square()
        }

        self.fType = fType
        self.start = start_node
        self.end = end_node

    def addFunc(self, key, func):
        self._funcs[key] = func

    def getFunc(self, fType=None):
        if fType is not None:
            return self._funcs[fType]
        else:
            return self._funcs[self._fType]

    @property
    def func(self):
        return self._funcs[self._fType]

    @property
    def fType(self):
        return self._fType

    @fType.setter
    def fType(self, fType):
        self._fType = fType

    @property
    def start(self):
        return self._startNode

    @start.setter
    def start(self, start_node):
        self._startNode = start_node

        if self._startNode is not None:
            assert type(start_node) is Node, "Invalid Type. Must be object of type 'Node'"
            self._startNode._right = self

    @property
    def end(self):
        return self._endNode

    @end.setter
    def end(self, end_node):
        self._endNode = end_node

        if self._endNode is not None:
            assert type(end_node) is Node, "Invalid Type. Must be object of type 'Node'"
            self._endNode._left = self

    def valid(self, x):
        return (x >= self._startNode.time) & (x <= self._endNode.time)


class SignalBuilder:
    _startNode = Node(nType='start')
    _endNode = Node(nType='end')
    _nodes = [_startNode, _endNode]
    _pieces = [Piece(_startNode, _endNode)]
    _sampleFrequency = None

    def __init__(self):
        pass
    
    @property
    def sampleFrequency(self):
        return self._sampleFrequency
    
    @sampleFrequency.setter
    def sampleFrequency(self, frequency):
        self._sampleFrequency = frequency

    @property
    def signalStart(self):
        return self._startNode.time

    @signalStart.setter
    def signalStart(self, t):
        # assert t < self._nodes[1].time(), "Invalid Time"
        self.setNodeTime(0, t)

    @property
    def signalEnd(self):
        return self._endNode.time

    @signalEnd.setter
    def signalEnd(self, t):
        # assert t > self._nodes[-2].time(), "Invalid Time"
        self.setNodeTime(len(self._nodes) - 1, t)

    def setNodeTime(self, index, t):
        myNode = self._nodes[index]

        left = None
        right = None

        for node in self._nodes[:index][::-1]:
            if node.time is not None:
                left = node

        for node in self._nodes[index + 1:]:
            if node.time is not None:
                right = node

        if left is not None:
            assert t > left.time, "Invalid Time"
        if right is not None:
            assert t < right.time, "Invalid Time"

        myNode.time = t

    @property
    def nodes(self):
        return self._nodes

    @property
    def pieces(self):
        return self._pieces

    def insertNode(self, index, t=None):
        assert 0 < index < len(self._nodes), "Invalid Node Index"
        newNode = Node(time=t)
        newPiece = Piece()
        newPiece.start = newNode

        self._nodes.insert(index, newNode)
        self._pieces.insert(index, newPiece)

        self._pieces[index - 1].end = newNode
        newPiece.end = self._nodes[index + 1]

    def deleteNode(self, index, right=True):
        delNode = self._nodes[index]

        if right:
            delPiece = delNode.right()
            oldPiece = delNode.left()
            oldNode = delPiece.getEnd()
        else:
            delPiece = delNode.left()

    def trace(self, report=False):
        obj = self._startNode
        trace = []
        while 1:

            if type(obj) is Node:
                trace.append(obj)
                if obj.nType is 'end':
                    break
                obj = obj.right
            if type(obj) is Piece:
                trace.append(obj)
                obj = obj.end

        return trace

    def checkNodeTimes(self, verbose=False):
        invalid = []
        for item in self.trace():
            if type(item) is Node:
                if item.time is None:
                    invalid.append(item)

        return invalid

    def report(self):
        for item in self.trace():
            if type(item) is Node:
                if item.nType is 'start':
                    print("Start Node:")
                elif item.nType is 'end':
                    print("End Node:")
                else:
                    print("Node:")
                print("    {}".format(item))
                print("    time: {}".format(item.time))
                print("----\n")

            if type(item) is Piece:
                print("Piece:")
                print("    {}".format(item))
                print("    Type: {}".format(item.fType))
                print("----\n")

    def genPiecew(self):
        print(self._endNode.time)
        num_samples = (self._endNode.time - self._startNode.time) * self._sampleFrequency
        t = np.linspace(self._startNode.time, self._endNode.time, num=num_samples)

        condlist = [piece.valid(t) for piece in self._pieces]
        funclist = [piece.getFunc().exec_ for piece in self._pieces]

        node_locations = [node.time for node in self._nodes]

        return t, np.piecewise(t, condlist, funclist), node_locations

    def chainConfig(self, start_node):
        obj = start_node
        nodes = []
        pieces = []
        while 1:

            if type(obj) is Node:
                nodes.append(obj)
                if obj.nType is 'end':
                    break
                obj = obj.right()
            if type(obj) is Piece:
                pieces.append(obj)
                obj = obj.getEnd()

        self._nodes = nodes
        self._pieces = pieces

    def listConfig(self, nodes, pieces):
        pass


def genPiecew(t, pieces):
    fun = np.piecewise(t, [piece.valid(t) for piece in pieces], [piece.getFunc().exec_ for piece in pieces])
    return fun


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
