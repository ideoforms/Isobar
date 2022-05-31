from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading
import time

from isobar.pattern.static import Globals
from isobar.constants import DEFAULT_TICKS_PER_BEAT

class NetworkGlobalsReceiver:
    """
    Simple interface to receive Globals over a network.

    TODO: Integrate with NetworkClockReceiver
    """
    def __init__(self, port=8193):
        dispatcher = Dispatcher()
        dispatcher.map("/globals/set", self.on_globals_set)

        server = BlockingOSCUDPServer(("0.0.0.0", port), dispatcher)
        self.thread = threading.Thread(target=server.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while True:
            time.sleep(0.1)

    def on_globals_set(self, address, *args):
        key = args[0]
        value = args[1]
        Globals.set(key, value)

if __name__ == "__main__":
    receiver = NetworkGlobalsReceiver()
    Globals.set("test", 0.0)
    while True:
        time.sleep(1.0)
        print(Globals.get("test"))