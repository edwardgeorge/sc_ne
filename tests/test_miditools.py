from osc_ne import miditools

def test_nibbles():
    assert miditools.nibbles(0xAE) == (0x0A, 0x0E)
    assert miditools.nibbles('\x5C') == (0x05, 0x0C)

def test_byte():
    assert miditools.byte(0xFF) == 255
    assert miditools.byte('\xFF') == 255

def test_byte14():
    assert miditools.byte14(0x01, 0x02) == int('100000001', 2)

def test__iterfmt():
    data = [(None, 'b'), (4, 'x'), (3, 's'), (2, 'b'), (0, 'i'), (0, 's'), ]
    res = list(miditools._iterfmt(data))
    expected = ['b', 's', 'b', 'b', 's']
    assert res == expected, 'expected %r got %r' % (expected, res)

def test__checkvals():
    assert miditools._checkvals(127, 'c') == 127
    assert miditools._checkvals('foo', 's') == 'foo'
    res = miditools._checkvals(int('01111111' '00000001', 2), 'H')
    assert res == int('11111111', 2), res
    res = miditools._checkvals(int('01101101' '01100001', 2), 'H')
    assert res == int('11000011101101', 2), res
    res = miditools._checkvals(int('01101101' '01100001' '00001011'
        '00000000', 2), 'i')
    assert res == int('101111000011101101', 2), res

def test_note():
    assert miditools.note(60) == ('C', 4)
    assert miditools.note(69) == ('A', 4)

def test_note_to_frequency():
    assert miditools.note_to_frequency(69) == 440.0
    assert miditools.note_to_frequency(69 - 12) == 220.0

def test_unpack():
    # check special case
    assert miditools.unpack(None, 'foo') == ['foo']

    assert miditools.unpack('', '') == []
    assert miditools.unpack('>4B', '\x01\x02\x03\x04') == [1, 2, 3, 4]
