import logging
from osc_ne import miditools

class NoMethodError(Exception):
    pass


def delegateto(obj, methods, raise_error=True):
    mlist = methods[:]
    while mlist:
        method, args, kwargs = mlist.pop(0)
        try:
            m = getattr(obj, method)
        except AttributeError, e:
            if not mlist and raise_error:
                raise NoMethodError()
        else:
            return m(*args, **kwargs)

class MidiHandler(object):
    from osc_ne.midispec import *
    def __init__(self, delegate):
        self.delegate = delegate or self

    def handle_message(self, bytestr):
        b = miditools.stringtobytes(bytestr)
        if 0x80 <= b[0] <= 0xEF:
            mtyp, chan = miditools.nibbles(b[0])
            return self.handle_channelmessage(mtyp, chan, b[1:])
        elif 0xF0 <= b[0] <= 0xFF:
            return self.handle_systemmessage(b)
        else:
            return ValueError()

    def handle_channelmessage(self, mtyp, chan, bytes):
        handler_name = self.CHANNEL_VOICE_HANDLERS[mtyp]
        delegateto(self.delegate, [
            (handler_name, [chan] + bytes, {}),
            ('channel_fallback', (mtyp, handler_name, chan, bytes), {})),
            ], raise_error=False)

    def handle_systemmessage(self, data):
        handler_name = None
        if data[0] == 0xF0:
            # sysex message
            return self.handle_sysex(data)
        elif 0xF1 <= data[0] <= 0xF7:
            # system common
            return self.handle_systemcommon(data)
        elif 0xF7 <= data[0] <= 0xFF:
            # system realtime
            return self.handle_systemrealtime(data)
        else:
            # should not happen
            raise Exception()

    def handle_sysex(self, data):
        handlers = [('sysex', (data,), {})]
        if data[0] == 0x7E:
            # universal non-realtime
            raise NotImplementedError()
        elif data[0] == 0x7F:
            # universal realtime
            raise NotImplementedError()
        else:
            delegateto(self.delegate, handlers, raise_error=False)

    def handle_systemcommon(self, data):
        handler_name = self.SYSTEM_COMMON_HANDLERS.get(data[0], 'SYSTEM_COMMON_UNDEFINED')
        handlers = [(handler_name, (data,), {}),
                    ('systemcommon_fallback', (handler_name, data), {}),
                    ('system_fallback', (handler_name, data), {})]
        delegateto(self.delegate, handlers, raise_error=False)

    def handle_systemrealtime(self, data):
        handler_name = self.SYSTEM_REALTIME_HANDLERS.get(data[0], 'SYSTEM_REALTIME_UNDEFINED')
        handlers = [(handler_name, (data,), {}),
                    ('systemrealtime_fallback', (handler_name, data), {}),
                    ('system_fallback', (handler_name, data), {})]
        delegateto(self.delegate, handlers, raise_error=False)

    # delegate methods
    def sysex(self, data):
        logger = logging.getLogger('osc_ne.midi.MidiHandler.sysex')
        logger.info('received sysex: %r' % data)

    def system_fallback(self, name, data):
        logger = logging.getLogger('osc_ne.midi.MidiHandler.system_fallback')
        logger.info('received system message %s: %r' % (name, data))

    def channel_fallback(self, typ, name, channel, bytes):
        logger = logging.getLogger('osc_ne.midi.MidiHandler.channel_fallback')
        logger.info('received chanel voice message %s on channel %d: %r' % (name, channel, data))

