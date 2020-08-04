## Python Polyphonic MIDI Synthesizer

[Python3](https://www.python.org/) script that simulates a [modular synthesizer](https://en.wikipedia.org/wiki/Modular_synthesizer).  Requires a separate [MIDI](https://en.wikipedia.org/wiki/MIDI) input device.  Generates samples based on waveforms and processes them through modules.  Allows control of the modules through MIDI messages.

#### Oscillators
Generates a waveform based on the following types:
 - sawtooth
 - triangle
 - square
 - sine

You can select which waveform is generated using MIDI program change.

#### Modules

Modules are used to process the waveform signal.  These are loaded from the settings *(see below)* then the signal is passed through each in order loaded for processing.  You can then set up bindings to control module parameters using MIDI controls.

#### Included Modules

*None!* :p  Someone needs to read up on dsp...

 - Currently a test module *mod.test* for testing MIDI control bindings.

#### Requirements

Requires the following packages to be installed:
- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- [sounddevice](https://pypi.org/project/sounddevice/)
- [rtmidi](https://pypi.org/project/python-rtmidi/)

-----

## Configuration

Settings can be found in the file *settings.json*.  One will be created automatically the first time the script is ran.

#### Sample rate
You can set the sample rate here.  Defaults to 44100Hz.
```
'sample_rate': 44100,
```

#### Keyboard events
The MIDI note on/off messages.  Defaults to the following:
```
'note_on': 144,
'note_off': 128,
```

#### Loading modules
Load modules to process the signal.  The signal will be filtered through each module in order added.
```
'modules': [ 'mod.test' ],
```

#### MIDI control bindings
Bind MIDI controls to modules or general settings.

__Format:__ binding_name, midi_msg[0], midi_msg[1]
```
'bindings': [
    #  Default bindings
    [ 'master_volume', 176, 29 ],

    #  Module bindings
    #  Binding names should have the format class_name.member_name
    [ 'test_module.set_a_value', 176, 118 ]
],
```

#### Saving data
Modules will store their data values here on shutdown, then restore them on next run.
```
'module_data': []
```

-----

## Modules

To make a module, create a Python file in the *mod* folder.  Define the module as a class, then define the following functions.

- __process function__ - Define what happens with the signal.
```
def process(self, signal):
    #  Do something with the signal
    return signal
```

- __save_data function__ - Return an array of binding names and the variable they are associated with.
```
def save_data(self):
    return [
        [ 'example.control_a', self.value_a ],
        [ 'example.control_b', self.value_b ]
    ]
```

For each control in the module, create a seperate function to set its value.  Then to create bindings to these controls, use the format __class_name.function_name__.

### Example mod.test.py
```
##  PPMS Synth Module for testing the patchboard.
class test_module:
    ##  Store test_value
    __test_value = 0

    ## Test process, simply print the test_value.
    #  @param self Object pointer
    #  @param signal Signal data to modify
    #  @return Modified signal data
    def process(self, signal):
        print("Test value:", self.__test_value)
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
```
