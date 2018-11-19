from .base import BaseInstrument


class Reaper(BaseInstrument):
    MINI_1_VOL = 9
    MINI_1_VERB = 10
    MINI_1_DIST = 11

    MINI_2_VOL = 15
    MINI_2_VERB = 12
    MINI_2_DIST = 13

    AMP_ATTACK = 16
    AMP_DECAY = 17
    AMP_RELEASE = 14
    EG_ATTACK = 20
    EG_DECAY = 21
    VOICE_MODE = 27
    CUTOFF = 43
    RESONANCE = 44
    LFO_RATE = 24
    LFO_INT = 26

    REVERB = 14
    DISTORTION = 18
    
    SPECIAL_1 = 19
    SPECIAL_2 = 20

    VCO_1_LEVEL = 39
    VCO_2_LEVEL = 40
    
    def __init__(self, output_name, channel=0, base_prog=79, base_bank=1, *args, **kwargs):
        super(Reaper, self).__init__(output_name, channel=channel, *args, **kwargs)
        self.base_prog = base_prog

    def mini_1_vol(self, value):
        self._control(self.MINI_1_VOL, int(value))

    def mini_2_vol(self, value):
        self._control(self.MINI_2_VOL, int(value))

    def mini_1_dist(self, value):
        self._control(self.MINI_1_DIST, value)

    def mini_2_dist(self, value):
        self._control(self.MINI_2_DIST, value)

    def special_1(self, value):
        self._control(self.SPECIAL_1, value)
    
    def special_2(self, value):
        self._control(self.SPECIAL_2, value)
    
    def mini_1_verb(self, value):
        self._control(self.MINI_1_VERB, value)

    def mini_2_verb(self, value):
        self._control(self.MINI_2_VERB, value)

    def reverb(self, value):
        self._control(self.REVERB, value)
    
    def distortion(self, value):
        self._control(self.DISTORTION, value)

    def program_change(self, program):
        super(Reaper, self).program_change(self.base_prog + program)

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
