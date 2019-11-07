# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 21:18:49 2019

@author: Yoshin
"""

from SignalBuilder.functions import *
import numpy as np

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
        assert index != 0 and index != len(self._nodes)-1, "Cannot Delete Start or End Node"
        delNode = self._nodes[index]

        if right:
            delPiece = delNode.right
            oldPiece = delNode.left
            oldNode = delPiece.end
            
            # Link together remaining unlinked node and piece
            oldPiece.end = oldNode
              
        else:
            delPiece = delNode.left
            oldPiece = delNode.right
            oldNode = delPiece.start
            
            # Link together remaining unlinked node and piece
            oldPiece.start = oldNode
        
        self._nodes.remove(delNode)
        self._pieces.remove(delPiece)
        

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