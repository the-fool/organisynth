from server.observable import observable_factory
import json

BASE_DO = 60

ionian = [0, 2, 4, 5, 7, 9, 11]


# OO implementation
class ColorMonoSequencer:
    """
    Responsible for interfacing with a remote client

    It has 2 public methods:

    1) A metronome callback
      - on metronome ticks, it sends a message with a note & beat index out to clients

    2) A WebSocket callback
      - on websocket messages from the client, it updates the notes

    It exposes a list of notes (real_notes) with the sequencer,
    which in turn is responsible for translating notes into midi messages
    """

    def __init__(self,
                 base_do=BASE_DO,
                 pitchIndices=[0, 0, 0, 0],
                 scale=ionian,
                 rhythm=[-1] * 16):
        self.pitchIndices = pitchIndices
        self.base_do = base_do
        self.scale = scale
        self.length = len(rhythm)
        self.rhythm = rhythm
        self.real_notes = [0] * len(rhythm)
        self.update_notes()
        self.obs, self.emit = observable_factory(self.msg_maker())

    def msg_maker(self):
        return json.dumps({
            'action': 'state',
            'payload': {
                'rhythm': self.rhythm,
                'pitches': self.pitchIndices
            }
        })

    @property
    def notes(self):
        return self.real_notes

    def update_notes(self):
        for i, n in enumerate(self.rhythm):
            # 0 and -1 are special cases (not mapped)
            if n > 0:
                pitchIndex = self.pitchIndices[n - 1]
                scaleIndex = pitchIndex % 7
                scaleMultiplier = pitchIndex // 7
                pitch = self.scale[scaleIndex] + self.base_do + (
                    12 * scaleMultiplier)
            else:
                pitch = n

            self.real_notes[i] = pitch

    async def metro_cb(self, ts):
        rhythm_index = ts % self.length
        note_index = self.rhythm[rhythm_index]
        msg = json.dumps({
            'action': 'beat',
            'payload': {
                'rhythm_index': rhythm_index,
                'note_index': note_index
            }
        })
        await self.emit(msg)

    async def ws_consumer(self, kind, payload, uuid):

        if kind == 'pitch':
            index = payload['index']
            value = payload['value']
            self.pitchIndices[index] = value

        elif kind == 'rhythm':
            index = payload['index']
            value = payload['value']
            self.rhythm[index] = value
        elif kind == 'state':
            # this one is OK -- it just passes through so as to receive the state
            pass
        else:
            # unknown
            return

        self.update_notes()
        await self.emit(self.msg_maker())
