import usb.core
import usb.util
from usb.core import Device
import sys

# Fixed values for different volume levels. Katana uses weird logarithmic scale
# I couldn't determine so the sniffed values are fixed.
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

DETACHED_IFACES = [0]

ID_VENDOR = 0x041E  # Creative Technology Ltd
ID_PRODUCT = 0x3247  # Sound BlasterX Katana


def get_device():
    dev = usb.core.find(idProduct=ID_PRODUCT, idVendor=ID_VENDOR)

    if type(dev) != Device:
        print("Error: no device has been found!")
        sys.exit(1)

    return dev


def setup_device(dev: Device):
    """
    Detaching all drivers is the most reliable solution.
    """

    # for iface in DETACHED_IFACES:
        # if dev.is_kernel_driver_active(iface):
            # dev.detach_kernel_driver(iface)

    # Iterate over the interfaces and detach all active ones
    for iface in dev.get_active_configuration().interfaces():
        if dev.is_kernel_driver_active(iface.bInterfaceNumber):
            dev.detach_kernel_driver(iface.bInterfaceNumber)


def set_volume(dev: Device, level: int):
    """
    Send two CONTROL transfers to set volume level.
    """
    raw_data = VOLUME_LEVELS[level].to_bytes(2, "little")

    print("[+] Start...")

    dev.ctrl_transfer(
        bmRequestType=0x21,
        bRequest=1,
        wValue=0x0201,
        wIndex=256,
        data_or_wLength=raw_data,
    )
    # dev.read(0x84, 64, 1000)

    print("[+] 1st CONTROL sent")

    dev.ctrl_transfer(
        bmRequestType=0x21,
        bRequest=1,
        wValue=0x0202,
        wIndex=256,
        data_or_wLength=raw_data,
    )
    # dev.read(0x84, 64, 1000)


    print("[+] 2nd CONTROL sent")


if __name__ == "__main__":
    dev = get_device()
    # setup_device(dev)
    set_volume(dev, 5)

    exit()
