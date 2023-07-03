# User-space Creative Katana X Blaster volume driver

Hobby project to write a user-space USB Audio Control driver to control the volume of my sound-bar - Sound BlasterX Katana. I based this on the sniffed USB traffic (using Wireshark) from the official Windows driver.

I implemented a small part of USB Audio specification just to control the volume.

The default Linux driver ("snd-usb-audio") seems not to be able to handle the volume change (host -> device) communication. As far as I understand this communication, the transmitted volume values actually, is not standard (acorrding to the "USB Device Class Definition for Audio Devices" specification). I tried to reverse engineer the algorithm to generate subsequent values but I wasn't able to do this (a strange logarithmic function). The plan B was to simply sniff all necessary values from the official Windows driver. To be honest I suspect that these values are hardcoded into the official driver as well. After hours of learning USB Audio communication... it finally worked! The volume changing programatically works but...

## A problem I cannot solve yet

An Audio Streaming data is transmitted with the Interface 1. An Audio Control data is transmitted with the Interface 0. So why, when I detach the Interface 0 from the kernel, the sound is gone? There must be something off with the default "snd-usb-audio" driver. Maybe it does something nasty when it's detached. The flow of an ISOCHRONOUS transmission (the actual sound data) is also interrupted so it's not only the case of messed Interface 0 settings. These two interfaces should operate independently but they don't. I don't see any suspicious traffic from the host to the device during the detachment so propably the default driver messes something in the kernel settings.

### A possible solution

The possible solution might be to implement the driver on the Linux Kernel Module level and skip the "detachment" part. The kernel-level driver should be configured to attach to Katana's Interface 0 automatically and do not allow the default "snd-usb-audio" be attached to the Audio Control interface at all.

## Sources

* [Universal Serial Bus Device Class Definition for Audio Devices - Specification](https://www.usb.org/sites/default/files/audio10.pdf)
