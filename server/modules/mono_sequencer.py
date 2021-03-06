import logging


class MonoSequencer:
    def __init__(self, get_notes, instruments=[], time_multiplier=1, octave_multiplier=0):
        """
        Notes are a mutable, public list of notes
        cbs are a list of objects that implement the BaseInstrument interface,
          -- namely, they have a note_on, note_off methods
        """
        self.get_notes = get_notes
        self.octave_multiplier = octave_multiplier
        self.off_note = 0
        self.instruments = instruments

        # if a time_multiplier is 1, then we hit on every beat
        # else, if the multiplier increases the amount of time each step takes
        # eg, with multiplier at 4, each step will be 4 times as long
        self.time_multiplier = time_multiplier

    async def on_beat(self, ts):
        notes = self.get_notes()
        if len(notes) == 0:
            return

        if len(self.instruments) == 0:
            return

        if ts % self.time_multiplier != 0:
            return

        step = int((ts // self.time_multiplier) % len(notes))

        note = notes[step] + self.octave_multiplier * 12

        logging.info('Mono seq trigger step {}, note {}'.format(step, note))
        # when note is == 0, hold
        # when note is < 0, rest

        # we either have a note, or a rest -- do note off!
        if note is not 0 and self.off_note is not 0:
            for instrument in self.instruments:
                instrument.note_off(self.off_note)
                self.off_note = 0

        # we have a note -- play it!
        if note > 0:
            self.off_note = note
            for instrument in self.instruments:
                instrument.note_on(note)
