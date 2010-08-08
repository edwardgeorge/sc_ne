from osc_ne import miditools

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
        try:
            handler = getattr(self, handler_name)
        except AttributeError, e:
            # shld log here
            pass
        else:
            return handler(chan, *bytes)

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
        pass

    def handle_systemcommon(self, data):
        handler_name = self.SYSTEM_COMMON_HANDLERS.get(data[0])
        if handler_name:
            try:
                handler = getattr(self, handler_name)
            except AttributeError, e:
                # shld log here
                pass
            else:
                return handler(data[1:])

    def handle_systemrealtime(self, data):
        handler_name = self.SYSTEM_REALTIME_HANDLERS.get(data[0])
        if handler_name:
            try:
                handler = getattr(self, handler_name)
            except AttributeError, e:
                # shld log here
                pass
            else:
                return handler(data[1:])

    # fallbacks
    def handle_channel_fallback(self, mtyp, type_name, chan, bytes):
        pass

    def handle_systemcommon_fallback(self, name, data):
        pass

    def handle_systemrealtime_fallback(self, name, data):
        pass
