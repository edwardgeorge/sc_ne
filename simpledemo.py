import logging
import sys
import time

from osc_ne import coremidi
from osc_ne import midi

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

handler = midi.MidiHandler()
callback = lambda data, userdata: handler.handle_message(data)

coremidi.go(callback, {})

while True:
    time.sleep(60)

