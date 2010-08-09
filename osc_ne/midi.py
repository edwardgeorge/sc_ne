import functools
import logging

from osc_ne import midispec
from osc_ne import miditools

def silence_unimplemented(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotImplementedError, e:
            pass
    return decorated

class MidiHandler(object):
    def __init__(self, delegate=None):
        self.delegate = delegate or self

    def _call(self, *methods):
        for mdata in methods[:]:
            method, args = mdata[0], mdata[1:]
            if method is None:
                continue
            try:
                m = getattr(self.delegate, method)
            except AttributeError, e:
                pass
            else:
                return m(*args)
        raise NotImplementedError()

    @silence_unimplemented
    def handle_message(self, bytestr):
        b = miditools.stringtobytes(bytestr)
        if 0x80 <= b[0] <= 0xEF:
            mtyp, chan = miditools.nibbles(b[0])
            return self.handle_channelmessage(mtyp, chan, b[1:])
        elif 0xF0 <= b[0] <= 0xFF:
            return self.handle_systemmessage(b)
        else:
            return ValueError()

    def handle_channelmessage(self, mtyp, chan, data):
        # should probably get controller name here for CC stuff
        if mtyp == MIDI_CONTROLCHANGE:
            try:
                return self.handle_controlchange(chan, data)
            except NotImplementedError, e:
                pass
        handler_name = midispec.CHANNEL_VOICE_HANDLERS[mtyp]
        return self._call(
            (handler_name, chan, data),
            ('channel_voice', mtyp, handler_name, chan, data))

    def handle_controlchange(self, chan, bytes):
        cc, val = bytes
        cc_name = midispec.CONTROLLERS.get(cc)
        return self._call(
            (cc_name, chan, val),
            ('control_change', cc, cc_name, chan, val))

    def handle_systemmessage(self, data):
        handler_name = None
        try:
            if data[0] == 0xF0:
                return self.handle_sysex(data)
            elif 0xF1 <= data[0] <= 0xF7:
                return self.handle_systemcommon(data)
            elif 0xF7 <= data[0] <= 0xFF:
                return self.handle_systemrealtime(data)
        except NotImplementedError, e:
            self._call(('system_message', data[0], data[1:]))

    def handle_sysex(self, data):
        handlers = [('sysex', (data,), {})]
        if data[0] == 0x7E:
            # universal non-realtime
            raise NotImplementedError()
        elif data[0] == 0x7F:
            # universal realtime
            raise NotImplementedError()
        else:
            return self._call(
                ('sysex', data))

    def handle_systemcommon(self, data):
        handler_name = midispec.SYSTEM_COMMON_HANDLERS.get(data[0])
        return self._call(
            (handler_name, data[1:]),
            ('system_common', data[0], handler_name, data[1:]))
            #('system_message', data[0], handler_name, data[1:]))

    def handle_systemrealtime(self, data):
        handler_name = midispec.SYSTEM_REALTIME_HANDLERS.get(data[0])
        return self._call(
            (handler_name, data[1:]),
            ('system_realtime', data[0], handler_name, data[1:]))
            #('system_message', data[0], handler_name, data[1:]))

    # delegate methods
    def sysex(self, data):
        logger = logging.getLogger('osc_ne.midi.MidiHandler.sysex')
        logger.info('received sysex: %r' % data)

    def system_message(self, name, data):
        logger = logging.getLogger('osc_ne.midi.MidiHandler.system_fallback')
        logger.info('received system message %s: %r' % (name, data))

    def channel_voice(self, typ, name, channel, bytes):
        logger = logging.getLogger('osc_ne.midi.MidiHandler.channel_fallback')
        logger.info('received chanel voice message %s on channel %d: %r' % (name, channel, data))

    def control_change(self, cc, name, channel, val):
        logger = logging.getLogger('osc_ne.midi.MidiHandler.control_change')
        logger.info('received cc message %s %r on channel %s: %s' %
            (cc, name, channel, val))
