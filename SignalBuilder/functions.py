# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 22:33:35 2019

@author: Yoshin
"""

from scipy import interpolate, signal
import numpy as np

# func_dict = {
#     'constant': Constant(),
#     'ramp': Ramp(),
#     'sinusoid': Sinusoid(),
#     'square': Square()
#     }

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
        if self._mode == 'rate':
            m = self._slope
        elif self._mode == 'ps':
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
        
class Function2:
    _timeRange = [0, 0]
    _properties = {'amplitude':1,
                   'frequency':1,
                   'vShift':0,
                   'phaseShift':0,
                   'duty':0.5}
    
    def __init__(self):
        self.__dict = self._properties
        print(self.amplitude)
    
    def setTimeRange(start,end):
        self._timeRange = [start, end]
        
        
    def __getattr__(self, name):
        try:
            return self.__dict[name]
        except KeyError:
            msg = "'{0}' object has no attribute '{1}'"
            raise AttributeError(msg.format(type(self).__name__, name))
    
    def exec_(self, x):
        raise Exception ("Not Implemented")
        
class square(Function):
    def __init__(self,amplitude=1, frequency=1, vertical_shift=0, phase_shift=0, duty_cycle=0.5):
        self._amplitude = amplitude
        self._frequency = frequency
        self._vShift = vertical_shift
        self._phaseShift = phase_shift
        self._duty = duty_cycle
        
    @property
    def amplitude(self):
        return self._amplitude
    
class Square(Function):
    def __init__(self,amplitude=1, frequency=1, vertical_shift=0, phase_shift=0, duty_cycle=0.5):
        self._amplitude = amplitude
        self._frequency = frequency
        self._vShift = vertical_shift
        self._phaseShift = phase_shift
        self._duty = duty_cycle
        
    def setAmplitude(self, amplitude):
        self._amplitude = amplitude

    def setFrequency(self, frequency):
        self._frequency = frequency

    def setVShift(self, vertical_shift):
        self._vShift = vertical_shift

    def setPhase(self, phase_shift):
        self._phaseShift = phase_shift
        
    def setDutyCycle(self, duty):
        self._duty = duty
        
    def exec_(self, x):
        return self._amplitude*signal.square(2 * np.pi * self._frequency * (x - self._phaseShift), duty=self._duty) + self._vShift