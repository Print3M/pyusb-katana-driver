"""
USB Audio Specification:
    5. Requests

Supported requests (5.2.):
    If an audio function does not support a certain request, it must indicate
    this by stalling the control pipe when that request is issued to the
    function. If SET request is supported, the associated GET request must also
    be supported (not the other way around).
"""

import enum

# Table A-9: Audio Class-Specific Request Codes
SET_CUR = 0x01
GET_CUR = 0x81

# Table 5-1: Set Request Values
AUDIO_CONTROL_SET = 0b00100001

# Table 5-2: Get Request Values
AUDIO_CONTROL_GET = 0b10100001


class ControlSelector(enum.IntEnum):
    """
    Feature Unit Control Selectors
    """

    MUTE = 0x01
    VOLUME = 0x02


def get_wValue(cs: ControlSelector, channel: int):
    return (cs.value << 8) | channel


def get_wIndex(entity: int, endpoint: int):
    return (entity << 8) | endpoint
