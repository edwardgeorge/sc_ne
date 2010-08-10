import re
import struct

__all__ = ['note', 'byte', 'note_to_frequency', 'stringtobytes', 'byte14',
    'byte14i', 'nibbles', 'unpack']

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_0 = (0, -1)  # Note 60 is Middle C (4), so 0 is C-1


def note(b):
    """MIDI Number to NOTE

    >>> note(60)
    ('C', 4)

    """
    n, o = NOTE_0
    n = n + b
    return NOTES[n % 12], o + (n // 12)

def byte(b):
    """return the integer value of a byte."""
    if isinstance(b, basestring):
        if len(b) == 1:
            return ord(b)
        raise ValueError()
    elif isinstance(b, int):
        if 0 <= b < 256:
            return b
        raise ValueError()
    raise TypeError()

def note_to_frequency(note, a_tuning=440):
    """Converts midi note (integer) to a frequency value in Hz."""
    note = note - 69  # A above middle C = 0. note(69) = ('A', 5)
    return (a_tuning * 2.0 ** (note / 12.0))

def stringtobytes(s):
    return map(byte, s)

def byte14(lsb, msb):
    """decodes the 14bit integer value from two bytes."""
    lsb, msb = byte(lsb), byte(msb)
    return (lsb & 127) | ((msb & 127) << 7)

def byte14i(b):
    """decodes 14bit integer from 16bit integer. significant bits inverted"""
    return byte14(b & 127, b >> 8 & 127)

def nibbles(b):
    """returns the high, low nibbles from a byte."""
    b = byte(b)
    return (b & 240) >> 4, b & 15

# utility funcs for unpack
def _iterfmt(res):
    for c, v in res:
        if v == 'x':
            continue
        elif c == 0 and v != 's':
            continue
        elif v == 's':
            yield v
        else:
            for i in range(int(c) if c else 1):
                yield v

def _checkvals(val, fmt):
    if isinstance(val, int):
        size = struct.calcsize('>' + fmt)
        if size > 1:
            tmp = 0
            for i in range(size):
                tmp = (tmp << 7) | (val & 127)
                val = val >> 8
            val = tmp
    return val

def unpack(fmt, string):
    # special case: if fmt is None just return string
    if fmt is None:
        return [string]
    if fmt and fmt[0] in ('@', '<', '>', '!', '='):
        if fmt[0] != '>':
            raise ValueError('unsupported byte ordering')
        fmt = fmt[1:]
    regex = re.compile('([0-9]+)?([xcbB?hHiIlLqQfdsp]{1})')
    filtered = list(_iterfmt(regex.findall(fmt)))
    results = struct.unpack('>' + fmt, string)
    assert len(filtered) == len(results), 'something terrible happened!'
    return map(_checkvals, results, filtered)

