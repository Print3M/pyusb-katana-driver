import usb.core
import usb.util
from usb.core import Device
import sys
from src.consts import *
from src.usb_audio import *


class KatanaAudioControlDriver:
    def __init__(self):
        self.dev = self.__get_device()
        self.__setup_device()

    def __get_device(self):
        dev = usb.core.find(idProduct=ID_PRODUCT, idVendor=ID_VENDOR)

        if type(dev) != Device:
            print("Error: no device has been found!")
            sys.exit(1)

        return dev

    def __setup_device(self):
        # Detach AudioControl interface
        if self.dev.is_kernel_driver_active(AUDIO_CONTROL_IFACE):
            self.dev.detach_kernel_driver(AUDIO_CONTROL_IFACE)

    def set_volume(self, level: int):
        """
        Send two CONTROL transfers (2 channels) to set volume level.

        5.2.2.4.1. Set Feature Unit Control Request
        5.2.2.4.3.2. Volume Control
        """
        raw_data = VOLUME_LEVELS[level].to_bytes(2, "little")

        self.dev.ctrl_transfer(
            bmRequestType=AUDIO_CONTROL_SET,
            bRequest=SET_CUR,
            wValue=get_wValue(ControlSelector.VOLUME, channel=1),
            wIndex=get_wIndex(entity=1, endpoint=0),
            data_or_wLength=raw_data,
        )
        self.dev.ctrl_transfer(
            bmRequestType=AUDIO_CONTROL_SET,
            bRequest=SET_CUR,
            wValue=get_wValue(ControlSelector.VOLUME, channel=2),
            wIndex=get_wIndex(entity=1, endpoint=0),
            data_or_wLength=raw_data,
        )

    def get_volume(self):
        """
        5.2.2.4.3.2. Volume Control
        """
        result = self.dev.ctrl_transfer(
            bmRequestType=AUDIO_CONTROL_GET,
            bRequest=GET_CUR,
            wValue=get_wValue(ControlSelector.VOLUME, channel=1),
            wIndex=get_wIndex(entity=1, endpoint=0),
            data_or_wLength=2,
        )
        value = (result[1] << 8) | result[0]

        return Volume.value_to_level(value)

    def get_mute(self):
        """
        5.2.2.4.3.1. Mute Control
        """
        result = self.dev.ctrl_transfer(
            bmRequestType=AUDIO_CONTROL_GET,
            bRequest=GET_CUR,
            wValue=get_wValue(ControlSelector.MUTE, channel=1),
            wIndex=get_wIndex(entity=1, endpoint=0),
            data_or_wLength=1,
        )

        return bool(result[0])


if __name__ == "__main__":
    dev = KatanaAudioControlDriver()
    print(dev.get_volume())
    dev.set_volume(13)
    print(dev.get_volume())

    exit()
