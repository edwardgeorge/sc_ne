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
        status = miditools.byte(bytestr[0])
        if 0x80 <= status <= 0xEF:
            mtyp, chan = miditools.nibbles(status)
            return self.handle_channelmessage(mtyp, chan, bytestr[1:])
        elif 0xF0 <= status <= 0xFF:
            return self.handle_systemmessage(status, bytestr[1:])
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

    def handle_controlchange(self, chan, data):
        cc, val = miditools.stringtobytes(data)
        cc_name = midispec.CONTROLLERS.get(cc)
        return self._call(
            (cc_name, chan, val),
            ('control_change', cc, cc_name, chan, val))

    def handle_systemmessage(self, status, data):
        try:
            if status == 0xF0:
                return self.handle_sysex(data)
            elif 0xF1 <= status <= 0xF7:
                return self.handle_systemcommon(status, data)
            elif 0xF7 <= status <= 0xFF:
                return self.handle_systemrealtime(status, data)
        except NotImplementedError, e:
            self._call(('system_message', status, data))

    def handle_sysex(self, data):
        if data[-1] != '\xF7':
            # aborted
            return
        data = data[:-1]
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

    def handle_systemcommon(self, status, data):
        handler_name = midispec.SYSTEM_COMMON_HANDLERS.get(status)
        return self._call(
            (handler_name, data),
            ('system_common', status, handler_name, data))
            #('system_message', status, handler_name, data))

    def handle_systemrealtime(self, status, data):
        handler_name = midispec.SYSTEM_REALTIME_HANDLERS.get(status)
        return self._call(
            (handler_name, data),
            ('system_realtime', status, handler_name, data))
            #('system_message', status, handler_name, data))

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
