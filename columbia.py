"""
This module should contain up-to-date values for Columbia ROACH hardware.

Note that this file is under version control so it is shared by all deploys. If a piece of hardware has multiple common
settings, it's better to create multiple, descriptive names for these settings here instead of overwriting with the one
currently in use. The values in this file shouldn't have to change often.
"""

SIM900_SERIAL = '/dev/serial/by-id/usb-FTDI_USB_to_Serial_Cable_FTGQM0GY-if00-port0'

# TODO: replace this with the by-id value.
LOCKIN_SERIAL = '/dev/ttyUSB2'

# TODO: add the other IP if we're commonly using both.
HITTITE_IP = '192.168.001.070'
