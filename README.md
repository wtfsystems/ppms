# Python Polyphonic MIDI Synthesizer

### Warning
 - Speaker warning
 - Experimental, WIP, math

### About

[Python](https://www.python.org/) script that simulates a basic [modular synthesizer](https://en.wikipedia.org/wiki/Modular_synthesizer).  Requires a separate [MIDI](https://en.wikipedia.org/wiki/MIDI) input device, however a [virtual](https://vmpk.sourceforge.io/) one may be used on supported platforms.  Generates samples based on [waveforms](https://en.wikipedia.org/wiki/Waveform) and processes them through modules.  Allows control of the modules through MIDI messages.

### Package Requirements

Requires the following Python packages to be installed:
- [numpy](https://numpy.org/)
- [scipy](https://www.scipy.org/)
- [sounddevice](https://pypi.org/project/sounddevice/)
- [python-rtmidi](https://pypi.org/project/python-rtmidi/)

###  How to Use

-----

## Parts

The file __parts.py__ contains a series of classes used to implement the functionality of a synthesizer.

### Algorithms
Algorithms for use throughout __ppms__.  Implemented in the __ppms_algs__ class.

### Oscillators
Generates waveforms based on the following types:
 - sawtooth /|
 - triangle /\
 - square |_|
 - sine ~

These are implemented in the __oscillator__ class.  You can select which waveform is generated using MIDI program change.

### Patchboard

Loads modules listed in settings and stores for processing.  Implemented in the __patchboard__ class.  When a note is played, the data is passed through each loaded module in order.

### Synth Modules

Processes the note data.  This allows implementation of effect processors.  An abstract base class __synthmod__ is used to create a new module.  See the section on *Modules* for more information.

### Mod Wheel

An abstract base class __mod_control__ that *Synth Module* classes can extend to allow reading from a mod wheel on a keyboard.

-----

## Modules

Modules are used to process the waveform signal.  These are loaded from the settings (*see below*) then the signal is passed through each in the order they were loaded.  You can then set up bindings to control module parameters using MIDI controls.

#### Included Modules

| File | Description |
| ---- | ----------- |
| __mod.test__ | For testing MIDI control bindings. |
| __mod.reverb__ | Adds reverberation effect. |
| __mod.bpass__ | Provides a high-pass and low-pass filter. |

-----

## Configuration

Settings can be found in the file *settings.json*.  One will be created automatically the first time the script is ran.

#### Sample rate
You can set the sample rate here.  Defaults to 44100Hz.  Value is a float.
```
"sample_rate": 44100.0,
```

#### Keyboard events
The MIDI note on/off messages.  Defaults to the following:
```
"sawtooth_on": 144,
"sawtooth_off": 128,
"triangle_on": 145,
"triangle_off": 129,
"square_on": 146,
"square_off": 130,
"sine_on": 147,
"sine_off": 131,
```

The load preset message is defined as:
```
"preset_msg": 192,
```

#### Impact weight
Set the impact weight.  This is used for factoring keyboard velocity.
```
"impact_weight": 20000,
```

#### Preset directory
Folder to load preset files from.
```
"preset_folder": "presets",
```

#### Loading modules
Load modules to process the signal.  The signal will be filtered through each module in order added.
```
"modules": [ "mod.test", "mod.another" ],
```

#### Loading presets
List preset files in order here.  These files must be located in the folder as indicated by the __preset_folder__ setting.
```
"presets": [ "example1.json", "example2.json" ],
```

Run with *--build_presets* to generate a list from the presets folder.

#### MIDI control bindings
Bind MIDI controls to modules or general settings.

__Format:__ binding_name, midi_msg[0], midi_msg[1]
```
"bindings": [
    #  Default bindings
    [ "master_volume", 176, 29 ],
    [ "pitch_wheel", 224, 0 ],
    [ "mod_wheel", 176, 1 ],

    #  Module bindings
    #  Binding names should have the format class_name.member_name
    [ "test_module.set_a_value", 176, 118 ]
],
```

#### Saving data
Modules will store their setting data here on shutdown, then restore them on next run.
```
"module_data": []
```

-----

## Modules
To make a module, create a Python file in the *mod* folder.  Define the module as a class and extend __synthmod__ from __parts.py__.  At minimum the __process__ function needs to be defined.  The class can then be composed as following:

- __process function__ - Define what happens with the signal.
```
def process(self, note, signal):
    #  Do something with the signal
    return signal
```

- __save_data function__ - Return an array of binding names and the variable they are associated with.
```
def save_data(self):
    return [
        [ "example.control_a", self.value_a ],
        [ "example.control_b", self.value_b ]
    ]
```

For each control in the module, create a seperate function to set its value.  Then to create bindings to these controls, use the format __class_name.function_name__.

### Example mod.test.py
```
from .parts import synthmod

##  PPMS Synth Module for testing the patchboard.
class test_module(synthmod):
    ##  Store test_value
    __test_value = 0

    ## Test process, simply print the test_value.
    #  @param self Object pointer
    #  @param note The note frequency being played
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
```

-----

## Presets

Preset files are used to store module parameters and can be loaded during runtime.  When the MIDI message to load a preset is received, it selects the corresponding preset file and sets the active parameters.

For setting the preset folder and MIDI message, see __Configuration__ above.

### Example preset.json
```
[
    [ "envelope.set_attack", 100 ],
    [ "envelope.set_decay", 27 ],
    [ "envelope.set_sustain", 46 ],
    [ "envelope.set_release", 90 ],
    [ "band_pass.set_high_pass", 12 ],
    [ "band_pass.set_low_pass", 42 ],
    [ "reverberation.set_reverb", 38 ]
]
```
