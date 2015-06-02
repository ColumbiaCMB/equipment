from __future__ import division
import time
import serial

class TemperatureMonitor218(object):

    # From manual table 6-1
    baud_rate = 9600
    data_bits = serial.SEVENBITS
    start_bits = 1  # Not sure what this is
    stop_bits = serial.STOPBITS_ONE  # This is the Serial default
    parity = serial.PARITY_ODD
    # flow control: None; this is the Serial default
    # handshaking: None; this is the Serial default

    # From page 50 of the  manual.
    #
    # When issuing commands the user program alone should:
    # -Properly format and transmit the command including terminators as one string
    # -Guarantee that no other communication is started for 50 ms after the last character is transmitted
    # -Not initiate communication more than 20 times/s
    #
    # When issuing queries or queries and commands together, the user program should:
    # -Properly format and transmit the query including the terminator as one string
    # -Prepare to receive a response immediately
    # -Receive the entire response from the instrument including the terminator
    # -Guarantee that no other communication is started during the response or for 50 ms after it completes
    # -Not initiate communication more than 20 times/s

    # The following delay ensures that the above conditions are satisfied, so the class uses this by default.
    communication_delay = 50e-3

    # The serial timeout
    timeout = 1

    # The serial termination character
    termination = '\n'

    def __init__(self, serial_device):
        self.serial_port = serial.Serial(port=serial_device, baudrate=self.baud_rate, bytesize=self.data_bits,
                                         parity=self.parity, timeout=self.timeout)
        self.serial_port.flushInput()
        self.serial_port.flushOutput()

    def send(self, message):
        self.serial_port.write(message + self.termination)
        time.sleep(self.communication_delay)

    def receive(self):
        return self.serial_port.readline().strip()

    def send_and_receive(self, message):
        self.serial_port.write(message + self.termination)
        message = self.receive()
        time.sleep(self.communication_delay)
        return message

    def clear_interface(self):
        self.send('*CLS')

    @property
    def enabled_status_bits(self):
        return int(self.send_and_receive('*ESE?'))

    @enabled_status_bits.setter
    def enabled_status_bits(self, status):
        self.send('*ESE {:d}'.format(status))

    @property
    def event_status_integer(self):
        return int(self.send_and_receive('*ESR?'))

    # Add handling of individual bits

    @property
    def identification(self):
        manufacturer, instrument_number, serial_number, firmware_version = self.send_and_receive('*IDN?').split(',')
        return manufacturer, instrument_number, serial_number, float(firmware_version)

    # test
    @property
    def operation_complete_enabled(self):
        return bool(self.send_and_receive('OPC?'))

    @operation_complete_enabled.setter
    def operation_complete_enabled(self, boolean):
        self.send('OPC {}'.format(int(boolean)))

    def reset(self):
        self.send('*RST')

    @property
    def service_request_integer(self):
        return int(self.send_and_receive('*SRE?'))

    @service_request_integer.setter
    def service_request_integer(self, integer):
        self.send('*SRE {:d}'.format(integer))

    @property
    def status(self):
        return int(self.send_and_receive('*STB?'))

    @property
    def startup_self_test_failed(self):
        return bool(self.send_and_receive('*TST?'))

    # WAI

    # ALARM
    # ALARM?
    # ALARMST?
    # ALMB
    # ALMB?
    # ALMRST

    # ANALOG
    # ANALOG?

    @property
    def analog_output_percentage(self):
        return float(self.send_and_receive('AOUT?'))

    @property
    def baud(self):
        return int(self.send_and_receive('BAUD?'))

    @baud.setter
    def baud(self, baud_rate):
        self.send('BAUD {:d}'.format(baud_rate))

    @property
    def celsius_all(self):
        return [float(reading) for reading in self.send_and_receive('CRDG? 0').split(',')]

    @property
    def celsius_1(self):
        return self.celsius_all[1-1]

    @property
    def celsius_2(self):
        return self.celsius_all[2-1]

    @property
    def celsius_3(self):
        return self.celsius_all[3-1]

    @property
    def celsius_4(self):
        return self.celsius_all[4-1]

    @property
    def celsius_5(self):
        return self.celsius_all[5-1]

    @property
    def celsius_6(self):
        return self.celsius_all[6-1]

    @property
    def celsius_7(self):
        return self.celsius_all[7-1]

    @property
    def celsius_8(self):
        return self.celsius_all[8-1]

    def delete_curve(self, curve):
        self.send('CRVDEL {:d}'.format(curve))

    # CRVHDR
    # CRVHDR
    # CRVPT
    # CRVPT?
