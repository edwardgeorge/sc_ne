NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_0 = (0, -1) # Note 60 is Middle C (4), so 0 is C-1


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
    note = note - 69 # A above middle C = 0. note(69) = ('A', 5)
    return (a_tuning * 2.0 ** (note/12.0))

def stringtobytes(s):
    return map(byte, s)

def byte14(b1, b2):
    """decodes the 14bit integer value from two bytes."""
    b1, b2 = byte(b1), byte(b2)
    return (b1 & 63) | ((b2 & 63) << 7)

def byte14i(b):
    """decodes 14bit integer from 16bit integer."""
    return byte14(b >> 8 & 127, b & 127)

def nibbles(b):
    """returns the high, low nibbles from a byte."""
    b = byte(b)
    return (b & 240) >> 4, b & 15
