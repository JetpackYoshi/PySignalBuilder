# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 22:33:35 2019

@author: Yoshin
"""

from scipy import interpolate, signal
import numpy as np

class Descriptor(object):
    
    def __init__(self, label):
        self.label = label
        
    def __get__(self, instance, owner):
        #print '__get__', instance, owner
        return instance.__dict__.get(self.label)
    
    def __set__(self, instance, value):
        #print '__set__'
        instance.__dict__[self.label] = value

        
class DescriptorOwner(type):
    def __new__(cls, name, bases, attrs):
        # find all descriptors, auto-set their labels
        for n, v in attrs.items():
            if isinstance(v, Descriptor):
                v.label = n
        return super(DescriptorOwner, cls).__new__(cls, name, bases, attrs)
    
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
    #__metaclass__ = DescriptorOwner
    amplitude = property()
    frequency = property()
    vShift = property()
    phaseShift = property()
    duty = property()

    def __init__(self,amplitude=1, frequency=1, vertical_shift=0, phase_shift=0, duty_cycle=0.5):
        self.amplitude = amplitude
        self.frequency = frequency
        self.vShift = vertical_shift
        self.phaseShift = phase_shift
        self.duty = duty_cycle
        
    def exec_(self, x):
        return self.amplitude*signal.square(2 * np.pi * self.frequency * (x - self.phaseShift), duty=self.duty) + self.vShift
    
    
class Square(Function):
    
    
    def __init__(self,amplitude=1, frequency=1, vertical_shift=0, phase_shift=0, duty_cycle=0.5):
        self.amplitude = amplitude
        self.frequency = frequency
        self.vShift = vertical_shift
        self.phaseShift = phase_shift
        self.duty = duty_cycle
        
    def setAmplitude(self, amplitude):
        self.__amplitude = amplitude

    def setFrequency(self, frequency):
        self.__frequency = frequency

    def setVShift(self, vertical_shift):
        self.__vShift = vertical_shift

    def setPhase(self, phase_shift):
        self.__phaseShift = phase_shift
        
    def setDutyCycle(self, duty):
        self.__duty = duty
        
    def exec_(self, x):
        return self.__amplitude*signal.square(2 * np.pi * self.__frequency * (x - self.__phaseShift), duty=self.__duty) + self.__vShift
    
    amplitude = property(fset=setAmplitude)
    frequency = property(fset=setFrequency)
    vShift = property(fset=setVShift)
    phaseShift = property(fset=setPhase)
    duty = property(fset=setDutyCycle)
    
