# Fixed values for different volume levels. Katana uses weird logarithmic scale
# I couldn't determine so the sniffed values are fixed. Item's index means its
# volume level.
VOLUME_LEVELS = [
    0xC000,
    0xC7BD,
    0xD0A8,
    0xD869,
    0xDC00,
    0xDEE7,
    0xE157,
    0xE370,
    0xE548,
    0xE6ED,
    0xE869,
    0xE9C3,
    0xEB01,
    0xEC27,
    0xED38,
    0xEE37,
    0xEF26,
    0xF008,
    0xF0DD,
    0xF1A7,
    0xF268,
    0xF31F,
    0xF3CE,
    0xF475,
    0xF515,
    0xF5B0,
    0xF644,
    0xF6D3,
    0xF75C,
    0xF7E1,
    0xF862,
    0xF8DF,
    0xF957,
    0xF9CC,
    0xFA3E,
    0xFAAC,
    0xFB18,
    0xFB80,
    0xFBE6,
    0xFC49,
    0xFCAA,
    0xFD08,
    0xFD64,
    0xFDBE,
    0xFE16,
    0xFE6C,
    0xFEC0,
    0xFF12,
    0xFF63,
    0xFFB2,
    0x0000,
]


class Volume:
    @staticmethod
    def level_to_value(level: int):
        return VOLUME_LEVELS[level]

    @staticmethod
    def value_to_level(value: int):
        return VOLUME_LEVELS.index(value)


# Interface to detach
AUDIO_CONTROL_IFACE = 0

# Creative Technology Ltd
ID_VENDOR = 0x041E

# Sound BlasterX Katana
ID_PRODUCT = 0x3247
