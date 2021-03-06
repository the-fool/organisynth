from .base import BaseInstrument


class Minilogue(BaseInstrument):
    AMP_ATTACK = 16
    AMP_DECAY = 17
    AMP_RELEASE = 19
    AMP_DECAY = 17
    EG_ATTACK = 20
    EG_DECAY = 21
    VOICE_MODE = 27
    CUTOFF = 43
    RESONANCE = 44
    LFO_RATE = 24
    LFO_INT = 26

    VCO_1_LEVEL = 39
    VCO_2_LEVEL = 40

    def __init__(self, output_name, base_prog=79, base_bank=1, *args, **kwargs):
        super(Minilogue, self).__init__(output_name, *args, **kwargs)
        self._control(0, 0)
        self._control(32, 1)
        self.base_prog = base_prog

    def program_change(self, program):
        super(Minilogue, self).program_change(self.base_prog + program)

    def level(self, value):
        self._control(self.VCO_2_LEVEL, value)
        self._control(self.VCO_1_LEVEL, value)

    def amp_release(self, value):
        self._control(self.AMP_RELEASE, value)

    def amp_attack(self, value):
        self._control(self.AMP_ATTACK, value)

    def amp_decay(self, value):
        self._control(self.AMP_DECAY, value)

    def eg_attack(self, value):
        self._control(self.EG_ATTACK, value)

    def eg_decay(self, value):
        self._control(self.EG_DECAY, value)

    def cutoff(self, value):
        self._control(self.CUTOFF, value)

    def resonance(self, value):
        self._control(self.RESONANCE, value)

    def beat_on(self, note, step=0):
        self.note_on(note=note)

    def beat_off(self, note, step=0):
        self.note_off(note=note)

    def voice_mode(self, val):
        self._control(self.VOICE_MODE, val)
