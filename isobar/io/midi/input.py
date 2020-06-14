import mido

import os
import time
import queue
import logging
from ...note import Note
from ...exceptions import DeviceNotFoundException

log = logging.getLogger(__name__)

MIDI_CLOCK_TICKS_PER_BEAT = 24

class MidiIn:
    def __init__(self, device_name=None, clock_target=None, virtual=False):
        if device_name is None:
            device_name = os.getenv("ISOBAR_DEFAULT_MIDI_IN")
        try:
            self.midi = mido.open_input(device_name, callback=self.callback, virtual=virtual)
        except (RuntimeError, SystemError, OSError):
            raise DeviceNotFoundException("Could not find MIDI device")

        self.clock_target = clock_target
        self.queue = queue.Queue()
        self.estimated_tempo = None
        self.last_clock_time = None
        log.info("Opened MIDI input: %s" % self.midi.name)

    @property
    def device_name(self):
        return self.midi.name

    def callback(self, message):
        """
        Callback for mido
        Args:
            message (mido.Message): The message
        """
        log.debug(" - MIDI message received: %s" % message)

        if message.type == 'clock':
            if self.last_clock_time is not None:
                dt = time.time() - self.last_clock_time
                tick_estimate = (120/48) * 1.0/dt
                if self.estimated_tempo is None:
                    self.estimated_tempo = tick_estimate
                else:
                    smoothing = 0.95
                    self.estimated_tempo = (smoothing * self.estimated_tempo) + ((1.0 - smoothing) * tick_estimate)
                self.last_clock_time = time.time()
            else:
                self.last_clock_time = time.time()

            if self.clock_target is not None:
                self.clock_target.tick()

        elif message.type == 'start':
            log.info(" - MIDI: Received start message")
            if self.clock_target is not None:
                self.clock_target.start()

        elif message.type == 'stop':
            log.info(" - MIDI: Received stop message")
            if self.clock_target is not None:
                self.clock_target.stop()

        elif message.type == 'songpos':
            log.info(" - MIDI: Received songpos message")
            if message.pos == 0:
                if self.clock_target is not None:
                    self.clock_target.reset()
            else:
                log.warning("MIDI song position message received, but MIDI input cannot seek to arbitrary position")

        elif message.type == 'note_on' or message.type == 'control':
            self.queue.put(message)

    def run(self):
        """
        Run indefinitely.
        """
        while True:
            time.sleep(0.1)

    def get_tempo(self):
        return self.estimated_tempo

    def set_tempo(self, tempo):
        raise RuntimeError("Cannot set the tempo of an external clock")

    tempo = property(get_tempo, set_tempo)

    @property
    def ticks_per_beat(self):
        return MIDI_CLOCK_TICKS_PER_BEAT

    def receive(self):
        return self.queue.get()

    def poll(self):
        """
        Non-blocking poll for MIDI messages.
        Returns:
            Note: The note received, or None.
        """
        rv = None
        try:
            rv = self.queue.get_nowait()
        except queue.Empty:
            pass
        return rv

    def close(self):
        del self.midi
