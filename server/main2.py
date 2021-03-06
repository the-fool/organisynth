import asyncio
import sys
import threading

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib as GObject

from .util import scale

from .microbit import MyMicrobit

from .web_servers import ws_server_factory

from .web_socket_clients import Clocker, MetronomeChanger,\
    ColorMonoSequencer as CMS,\
    CubeOfPatchChanger,\
    DrummerChanger,\
    FxManager

from .modules import Metronome,\
    MonoSequencer,\
    ScaleCube,\
    PatchCube,\
    Drummer

from .instruments.four_by_four import instruments
from .table import LedTCPServer

import logging

MBIT_VOZUZ = 'DE:ED:5C:B4:E3:73'
MBIT_GUPAZ = 'D5:38:B0:2D:BF:B6'
DONGLE_ADDR = '5C:F3:70:81:F3:66'

starting_bpm = 120

loop = asyncio.get_event_loop()

BLE = True
LED = True
SLIDEY = False


def parse_argv():
    global BLE
    global LED
    global SLIDEY
    argv = sys.argv
    for arg in argv:
        if arg == '--no-ble':
            # no ble
            BLE = False
        elif arg == '--no-table':
            LED = False
        elif arg == '--no-slidey':
            SLIDEY = False
        elif arg == '--slidey':
            SLIDEY = True


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    parse_argv()

    scale_cube = ScaleCube()

    patch_cube_1 = PatchCube(instruments=instruments[:1])
    patch_changer_1 = CubeOfPatchChanger(patch_cube_1)

    patch_cube_2 = PatchCube(instruments=instruments[1:2])
    patch_changer_2 = CubeOfPatchChanger(patch_cube_2)

    fx_cbs = make_fx_cbs()

    reaper_fx = FxManager(fx_cbs['reaper'])

    # make COLOR_MONO_SEQUENCER
    cms1 = CMS(scale_cube, identifier='slow')
    cms2 = CMS(scale_cube, identifier='fast')

    # make MONO_SEQUENCER

    # fast
    mono_seq_1 = MonoSequencer(
        cms2.get_notes, 
        instruments=[instruments[0]])

    # slow
    mono_seq_2 = MonoSequencer(
        cms1.get_notes,
        instruments=[instruments[1]], 
        time_multiplier=16, 
        octave_multiplier=-1)

    # make CLOCKER
    clocker = Clocker()

    # make DRUMMER
    drummer = Drummer(midi_devs=[instruments[2]])
    drummer_changer = DrummerChanger(drummer=drummer)

    if LED:
        table_server = LedTCPServer(
            loop=loop,
            scale_cube=scale_cube,
            patch_cube=patch_cube_1,
            color_seqs=[cms2, cms1])
    # Set up metronome
    metronome_cbs = [
        clocker.metronome_cb, 
        mono_seq_1.on_beat, 
        mono_seq_2.on_beat,
        drummer.on_beat
    ]

    if LED:
        metronome_cbs.append(table_server.metro_cb)

    metronome = Metronome(metronome_cbs, starting_bpm)

    metro_changer = MetronomeChanger(
        init_bpm=starting_bpm, on_change_cb=metronome.set_bpm)

    # hash of {path: (consumer, producer)}
    ws_behaviors = {
        'clocker': (None, clocker.obs),
        # 'particles': (particles_ws_consumer, None),
        'metronome_changer': (metro_changer.ws_consumer, metro_changer.obs),
        # 'scale': (scale_changer.ws_consumer, scale_changer.obs),
        'patch_1': (patch_changer_1.ws_consumer, patch_changer_1.obs),
        'patch_2': (patch_changer_2.ws_consumer, patch_changer_2.obs),
        'cms1': (cms1.ws_consumer, cms1.obs),
        'cms2': (cms2.ws_consumer, cms2.obs),
        'drummer': (drummer_changer.ws_consumer, drummer_changer.obs),
        'fx_reaper': (reaper_fx.ws_consumer, reaper_fx.obs),
    }

    ws_server_coro = ws_server_factory(behaviors=ws_behaviors)

    coros = [
        patch_changer_1.coro(), patch_changer_2.coro(),
        ws_server_coro,
        metronome.run()
    ]

    if LED:
        coros.extend(table_server.coros)

    # Set Up mbits
    if BLE:
        gupaz_cb = make_gupaz_uart_cb(patch_cube_1, loop)
        vozuz_cb = make_vozuz_uart_cb(patch_cube_2, loop)
        setup_mbits(vozuz_cb, gupaz_cb)

        # and run the dbus loop
        t = threading.Thread(target=run_dbus_loop)
        t.start()

    loop.run_until_complete(asyncio.gather(*coros))

    loop.close()


def run_dbus_loop():
    """
    Start the dbus loop
    """
    DBusGMainLoop(set_as_default=True)
    loop = GObject.MainLoop()
    loop.run()


def microbit_init(address):
    # Do the microbit things:
    try:
        logging.info('Attempting to connect to {}'.format(address))
        mbit = MyMicrobit(device_addr=address, adapter_addr=DONGLE_ADDR)

        logging.info('Successfully connected to {}!'.format(address))
    except:
        logging.error('Failed to find mbit {}'.format(address))
        return None
    if not mbit.connect():
        logging.error('Failed to connect to {}'.format(address))
        return None
    return mbit


def setup_mbits(vozuz_uart_cb, gupaz_uart_cb):
    gupaz = microbit_init(MBIT_GUPAZ)
    vozuz = microbit_init(MBIT_VOZUZ)
    gupaz.subscribe_uart(gupaz_uart_cb)
    vozuz.subscribe_uart(vozuz_uart_cb)


def make_gupaz_uart_cb(patch_cube, loop):
    def cb(l, data, x):
        try:
            (kind, payload) = [int(chr(c)) for c in data['Value']]
            if kind == 0:
                logging.info('Power Cube of Patch 1: DISCONNECTED')
            elif kind == 1:
                logging.info(
                    'Power Cube of Patch 1: CONNECTED at {}'.format(payload))
                asyncio.ensure_future(patch_cube.set_patch(payload), loop=loop)

            print(kind, payload)
        except Exception as e:
            print(e)
            print('error', data)

    return cb


def make_vozuz_uart_cb(patch_cube, loop):
    def cb(l, data, x):
        try:
            (kind, payload) = [int(chr(c)) for c in data['Value']]
            if kind == 0:
                logging.info('Power Cube of Patch 2: DISCONNECTED')
            elif kind == 1:
                logging.info(
                    'Power Cube of Patch 2: CONNECTED at {}'.format(payload))

                asyncio.ensure_future(patch_cube.set_patch(payload), loop=loop)
            print(kind, payload)
        except Exception as e:
            print(e)
            print('error', data)

    return cb


def make_fx_cbs():
    if len(instruments) < 3:
        # no instruments connected
        return

    reaper = instruments[2]

    def scale_it(cb, maximum=127):
        def scaled(x):
            cb(scale(x, 0, 1, 0, maximum))

        return scaled

    def make_mini_cbs(i):
        mini = instruments[i]

        return {
            'cutoff': scale_it(mini.cutoff),
            'attack': scale_it(mini.eg_attack),
            'release': scale_it(mini.amp_release),
            'decay': scale_it(mini.amp_decay),
            'volume': scale_it(getattr(reaper, 'mini_{}_vol'.format(i + 1)), maximum=80),
            'reverb': scale_it(getattr(reaper, 'mini_{}_verb'.format(i + 1))),
            'distortion': scale_it(getattr(reaper, 'mini_{}_dist'.format(i + 1)))
        }

    reaper_cbs = {
        'reverb': scale_it(reaper.reverb),
        'distortion': scale_it(reaper.distortion),
        'special1': scale_it(reaper.special_1),
        'special2': scale_it(reaper.special_2)
    }

    return {
        'reaper': reaper_cbs
    }
