from . import Minilogue, Reaper

MIDI_OUTPUTS = [
    'MIDI4x4:MIDI4x4 MIDI 1 20:0', 'MIDI4x4:MIDI4x4 MIDI 2 20:1',
    'MIDI4x4:MIDI4x4 MIDI 3 20:2', 'MIDI4x4:MIDI4x4 MIDI 4 20:3'
]

instrument_dict = {
    'minilogue_1': Minilogue(MIDI_OUTPUTS[0]),
    'minilogue_2': Minilogue(MIDI_OUTPUTS[1]),
    'reaper': Reaper(MIDI_OUTPUTS[2], channel=1),
    'synth_fast': Reaper(MIDI_OUTPUTS[2], channel=2),
    'synth_slow': Reaper(MIDI_OUTPUTS[2], channel=3)
}

instruments = [
    instrument_dict['synth_fast'],
    instrument_dict['synth_slow'],
    instrument_dict['reaper']
]
