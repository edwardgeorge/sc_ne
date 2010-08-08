MIDI_NOTE_OFF = 0x08
MIDI_NOTE_ON = 0x09
MIDI_AFTERTOUCH = 0x0A
MIDI_CONTROLCHANGE = 0x0B
MIDI_PROGRAMCHANGE = 0x0C
MIDI_CHANNELPRESSURE = 0x0D
MIDI_PITCHWHEEL = 0x0E

CHANNEL_VOICE_HANDLERS = {
    MIDI_NOTE_OFF: 'NOTE_OFF',
    MIDI_NOTE_ON: 'NOTE_ON',
    MIDI_AFTERTOUCH: 'AFTERTOUCH',
    MIDI_CONTROLCHANGE: 'CC',
    MIDI_PROGRAMCHANGE: 'PROGRAM',
    MIDI_PITCHWHEEL: 'PITCH_WHEEL',
}
CONTROLLERS = {
    # MSBs
    0x00: 'BANK_SELECT_MSB',
    0x01: 'MODULATION_WHEEL_MSB',
    0x02: 'BREATH_MSB',
    # 0x03 undefined
    0x04: 'FOOT_PEDAL_MSB',
    0x05: 'PORTAMENTO_TIME_MSB',
    0x06: 'DATA_ENTRY_SLIDER',
    0x07: 'CHANNEL_VOLUME_MSB',
    0x08: 'BALANCE_MSB',
    # 0x09 undefined
    0x0A: 'PAN_MSB',
    0x0B: 'EXPRESSION_MSB',
    0x0C: 'EFFECT_1_MSB',
    0x0D: 'EFFECT_2_MSB',
    # 0x0E undefined
    # 0x0F undefined
    0x10: 'GENERAL_PURPOSE_1_MSB',
    0x11: 'GENERAL_PURPOSE_2_MSB',
    0x12: 'GENERAL_PURPOSE_3_MSB',
    0x13: 'GENERAL_PURPOSE_4_MSB',
    # 0x14 undefined
    # ...
    # 0x1F undefined
    0x20: 'BANK_SELECT_LSB',

    # LSBs
    0x21: 'MODULATION_WHEEL_LSB',
    0x22: 'BREATH_LSB',
    # 0x23 undefined. lsb for 0x03
    0x24: 'FOOT_PEDAL_LSB',
    0x25: 'PORTAMENTO_TIME_LSB',
    0x26: 'DATA_ENTRY_SLIDER',
    0x27: 'CHANNEL_VOLUME_LSB',
    0x28: 'BALANCE_LSB',
    # 0x29 undefined. lsb for 0x09
    0x2A: 'PAN_LSB',
    0x2B: 'EXPRESSION_LSB',
    0x2C: 'EFFECT_1_LSB',
    0x2D: 'EFFECT_2_LSB',
    # 0x2E undefined. lsb for 0x0E
    # 0x2F undefined. lsb for 0x0F
    0x30: 'GENERAL_PURPOSE_1_LSB',
    0x31: 'GENERAL_PURPOSE_2_LSB',
    0x32: 'GENERAL_PURPOSE_3_LSB',
    0x33: 'GENERAL_PURPOSE_4_LSB',
    # 0x34 undefined. lsb for 0x14
    # ...
    # 0x3F undefined. lsb for 0x1F

    # switches
    0x40: 'DAMPER_PEDAL',  # 0-63 off, 64-127 on
    0x41: 'PORTAMENTO_PEDAL',
    0x42: 'SOSTENUTO_PEDAL',  # sustain pedal
    0x43: 'SOFT_PEDAL',
    0x44: 'LEGATO_PEDAL',
    0x45: 'HOLD_2_PEDAL',

    # sound control
    0x46: 'SOUND_CONTROL_1',  # default: sound variation
    0x47: 'SOUND_CONTROL_2',  # default: sound timbre
    0x48: 'SOUND_CONTROL_3',  # default: release time
    0x49: 'SOUND_CONTROL_4',  # default: attack time
    0x4A: 'SOUND_CONTROL_5',  # default: brightness
    0x4B: 'SOUND_CONTROL_6',  # default: decay time (mma rp-021)
    0x4C: 'SOUND_CONTROL_7',  # default: vibrato rate (mma rp-021)
    0x4D: 'SOUND_CONTROL_8',  # default: vibrato depth (mma rp-021)
    0x4E: 'SOUND_CONTROL_9',  # default: vibrato delay (mma rp-021)
    0x4F: 'SOUND_CONTROL_10',  # default: undefined (mma rp-021)

    0x50: 'GENERAL_PURPOSE_5',
    0x51: 'GENERAL_PURPOSE_6',
    0x52: 'GENERAL_PURPOSE_7',
    0x53: 'GENERAL_PURPOSE_8',
    0x54: 'PORTAMENTO_CONTROL',
    # 0x55 undefined
    # ...
    # 0x5A undefined

    # effects
    0x5B: 'EFFECTS_1_DEPTH',  # default: reverb send level (mma rp-023)
    0x5C: 'EFFECTS_2_DEPTH',  # (tremolo depth)
    0x5D: 'EFFECTS_3_DEPTH',  # default: chorus send level (mma rp-023)
    0x5E: 'EFFECTS_4_DEPTH',  # (celeste[detune] depth)
    0x5F: 'EFFECTS_5_DEPTH',  # (phaser depth)

    0x60: 'DATA_INCREMENT',  # DATA ENTRY +1 (mma rp-018)
    0x61: 'DATA_DECREMENT',  # DATA ENTRY -1 (mma rp-018)
    0x62: 'NRPN_LSB',  # Non-Registered Param Number (Param for Data Entry)
    0x63: 'NRPN_MSB',
    0x64: 'RPN_LSB',  # Registered Param Number (for Data Entry)
    0x65: 'RPN_MSB',
    # 0x66 undefined
    # ...
    # 0x77 undefined

    # channel mode messages
    0x78: 'ALL_SOUND_OFF',  # value isn't used and defaults to 0
    0x79: 'RESET_ALL_CONTROLLERS',  # value is default 0 (mma rp-015)
    0x7A: 'LOCAL_CONTROL',  # switch for keyboard device. 0 off, 127 on.
    0x7B: 'ALL_NOTES_OFF',  # value not used, defaults to 0
    0x7C: 'OMNI_MODE_OFF',  # no value. all notes turned off.
    0x7D: 'OMNI_MODE_ON',  # no value. all notes turned off.
    0x7E: 'MONO_MODE_ON',  # value is how many channels to respond to (0 = num voices). all notes off.
    0x7F: 'MONO_MODE_OFF',  # no value. all notes off.
}
REGISTERED_PARAMETER_NUMBERS = {
    # to imput from: http://www.midi.org/techspecs/midimessages.php
}
SYSTEM_COMMON_HANDLERS = {
    # 0xF0 SYSTEM EXCLUSIVE. handled internally.
    0xF1: 'MTC_QUARTER_FRAME',
    0xF2: 'SONG_POSITION',
    0xF3: 'SONG_SELECT',
    # 0xF4 undefined
    # 0xF5 undefined
    0xF6: 'TUNE_REQUEST',
    # 0xF7
}
SYSTEM_REALTIME_HANDLERS = {
    0xF8: 'MIDI_CLOCK',
    0xF9: 'MIDI_TICK',
    0xFA: 'MIDI_START',
    0xFB: 'MIDI_CONTINUE',
    0xFC: 'MIDI_STOP',
    # 0xFD undefined
    0xFE: 'ACTIVE_SENSE',
    0xFF: 'RESET',
}
# 0x7E non-realtime, 0x7F realtime
# from http://www.midi.org/techspecs/midimessages.php
UNIVERSAL_SYSEX_NONREALTIME_HANDLERS = {
    # 0x00 unused
    # 0x01 - 0x03 sample dump
    # 0x04 midi time code
    # 0x05 sample dump extensions
    (0x06, 0x01): 'IDENTITY_REQUEST',
     (0x06, 0x02): 'IDENTITY_REPLY',
    # 0x07 file dump
    # 0x08 midi tuning standard
    # 0x09 GM ENABLE/DISABLE
    # 0x0A downloadable sounds
    # 0x0B file reference
    # 0x7B - 0x7F End of File, Wait, Cancel, NAK, ACK
}
UNIVERSAL_SYSEX_REALTIME_HANDLERS = {
    # 0x00 unused
    # 0x01 midi time code
    # 0x02 midi show control
    # 0x03 notation information
    (0x04, 0x01): 'MASTER_VOLUME',
     (0x04, 0x02): 'MASTER_BALANCE',
     (0x04, 0x03): 'MASTER_FINE_TUNING',
     (0x04, 0x04): 'MASTER_COURSE_TUNING',
     (0x04, 0x05): 'GLOBAL_PARAMETER_CONTROL',
    # 0x05 real-time MTC cueing
    # 0x06 midi machine control commands
    # 0x07 midi machine control responses
    # 0x08 midi tuning standard
    # 0x09 controller destination setting
    # 0x0A key-based instrument control
    # 0x0B scalable polyphony midi mip message
    # 0x0C mobile phone control message
}
