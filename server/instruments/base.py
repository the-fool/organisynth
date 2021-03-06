import mido

import logging


class BaseInstrument:
    def __init__(self, output_name, channel=0):
        self.outport = mido.open_output(output_name)
        self.channel = channel
        logging.info(
            "Instrument: {} on channel {}".format(output_name, channel))

    @staticmethod
    def midify(x):
        if not isinstance(x, int):
            x = int(x)

        if x < 0:
            x = 0
        if x > 127:
            x = 127
        return x

    def note_on(self, note, velocity=127):
        velocity = BaseInstrument.midify(velocity)
        self._out_msg('note_on', note=note, velocity=velocity)

    def note_off(self, note):
        note = BaseInstrument.midify(note)
        self._out_msg('note_off', note=note)

    def _control(self, control, value):
        print('Control change', control, value)
        control = self.midify(control)
        value = self.midify(value)
        self._out_msg('control_change', control=control, value=value)

    def _out_msg(self, kind, **kwargs):
        m = mido.Message(kind, channel=self.channel, **kwargs)
        self.outport.send(m)

    def program_change(self, program):
        print(program)
        m = mido.Message('program_change', program=program, channel=self.channel)
        self.outport.send(m)
