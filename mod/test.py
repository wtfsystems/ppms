#
#  Python Polyphonic MIDI Synthesizer
#
#  Filename:  test.py
#  By:  Matthew Evans
#  See LICENSE.md for copyright information.
#

from .parts import synthmod

##  PPMS Synth Module for testing the patchboard.
class test_module(synthmod):
    ##  Store test_value
    __test_value = 0

    ## Test process, simply print the test_value.
    #  @param self Object pointer
    #  @param signal Signal data to modify
    #  @return Modified signal data
    def process(self, note, signal):
        if self.__test_value > self.MIDI_MIN:
            if self.__test_value == self.MIDI_MAX:
                print("Text value at max: ", self.__test_value)
            else:
                print("Test value: ", self.__test_value)
        return signal

    ##  Build an array of save data for the module.
    #  Bindings should have the format class_name.member_name.
    #  @param self Object pointer
    #  @return Module data to save
    def save_data(self):
        return [
            [ 'test_module.set_a_value', self.__test_value ]
        ]

    ## Set test value.
    #  @param self Object pointer
    #  @param val New value to set
    def set_a_value(self, val):
        self.__test_value = val
