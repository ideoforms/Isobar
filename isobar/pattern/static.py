from . import Pattern

import threading
import copy

class PStaticGlobal(Pattern):
    """ PStaticGlobal: Static global value identified by a string, with OSC listener.
    TODO: Rename to PStaticDict, remove global support?
    """
    dict = {}
    listening = False

    def __init__(self, name, value=None):
        self.name = name
        if value is not None:
            PStaticGlobal.set(name, value)

    def __next__(self):
        name = Pattern.value(self.name)
        value = PStaticGlobal.dict[name]
        return Pattern.value(value)

    # BROKEN: not sure why
    @classmethod
    def _get(self, key):
        value = PStaticGlobal.dict[key]
        return Pattern.value(value)

    @classmethod
    def set(self, key, value):
        PStaticGlobal.dict[key] = value

    @classmethod
    def listen(self, prefix="/global", port=9900):
        if not PStaticGlobal.listening:
            # TODO: Fix
            server = OSC.OSCServer(("localhost", port))
            server.addMsgHandler(prefix, self.recv)
            self.thread = threading.Thread(target=server.serve_forever)
            self.thread.setDaemon(True)
            self.thread.start()

            PStaticGlobal.listening = True

        self.prefix = prefix

    @classmethod
    def recv(self, addr, tags, data, client_address):
        key = data[0]
        value = data[1]
        PStaticGlobal.set(key, value)

class Globals:
    @classmethod
    def get(cls, key):
        if key not in PGlobals.dict:
            raise ValueError("Global variable does not exist: %s" % key)
        value = PGlobals.dict[key]
        return Pattern.value(value)

    @classmethod
    def set(cls, key, value):
        PGlobals.dict[key] = value

class PGlobals (Pattern):
    """ PGlobals: Static global value identified by a string.
    """
    dict = {}

    def __init__(self, name):
        self.name = name

    def __next__(self):
        name = Pattern.value(self.name)
        value = Globals.get(name)
        return Pattern.value(value)

class PStaticSequence(Pattern):
    def __init__(self, sequence, duration):
        #------------------------------------------------------------------------
        # take a copy of the list to avoid changing the original
        #------------------------------------------------------------------------
        self.sequence = copy.copy(sequence)
        self.duration = duration
        self.start = None

    def __next__(self):
        timeline = self.timeline
        if self.start is None:
            self.start = round(timeline.current_time, 5)

        now = round(timeline.current_time, 5)
        if now - self.start >= self.duration:
            self.sequence.pop(0)
            self.start = now
            if len(self.sequence) == 0:
                raise StopIteration
        return self.sequence[0]

class PStaticPattern(Pattern):
    def __init__(self, pattern, element_duration):
        self.pattern = pattern
        self.value = None
        self.element_duration = element_duration
        self.current_element_start_time = None
        self.current_element_duration = None

    def __next__(self):
        timeline = self.timeline
        current_time = round(timeline.current_time, 5)
        if self.current_element_start_time is None or \
                current_time - self.current_element_start_time >= self.current_element_duration:

            self.value = Pattern.value(self.pattern)
            self.current_element_start_time = round(timeline.current_time, 5)
            self.current_element_duration = Pattern.value(self.element_duration)

        return self.value

class PStaticOSCReceiver(Pattern):
    listening = False

    def __init__(self, default=0, address="/value", port=9900):
        if not PStaticOSCReceiver.initialised:
            server = OSC.OSCServer(("localhost", port))
            server.addMsgHandler(prefix, self.recv)
            self.thread = threading.Thread(target=server.serve_forever)
            self.thread.setDaemon(True)
            self.thread.start()

            PStaticGlobal.listening = True

            osc_server = OSC.OSCServer(("0.0.0.0", port))
            osc_server.serve_forever()

        self.value = default
        self.address = address
        osc.bind(self.recv, address)

    def recv(self, msg, source=None):
        address = msg[0]
        signature = msg[1][1:]
        print("(%s) %s" % (address, signature))
        self.value = msg[2]

    def __next__(self):
        return self.value

class PStaticCurrentTime(Pattern):
    """ PStaticCurrentTime: Returns the position (in beats) of the current timeline. """

    def __init__(self, timeline=None):
        self.given_timeline = timeline

    def __next__(self):
        beats = self.get_beats()
        return round(beats, 5)

    def get_beats(self):
        #------------------------------------------------------------------------
        # using the specified timeline (if given) or the currently-embedded
        # timeline (otherwise), return the current position in current_time.
        #------------------------------------------------------------------------
        timeline = self.given_timeline if self.given_timeline else self.timeline
        if timeline:
            return timeline.current_time

        return 0
