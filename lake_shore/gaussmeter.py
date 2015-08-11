from __future__ import division
import time
import serial


class Gaussmeter425(object):

    # From manual table 6-1
    baud_rate = 57600
    data_bits = serial.SEVENBITS
    start_bits = 1  # Not sure what this is
    stop_bits = serial.STOPBITS_ONE  # This is the Serial default
    parity = serial.PARITY_ODD
    # flow control: None; this is the Serial default
    # handshaking: None; this is the Serial default

    # From page 50 of the  manual.
    #
    # When issuing commands the user program alone should:
    # -Properly format and transmit the command including the terminator as one string
    # -Guarantee that no other communication is started for 30 ms after the last character is transmitted
    # -Not initiate communication more than 30 times/s
    #
    # When issuing queries or queries and commands together, the user program should:
    # -Properly format and transmit the query including the terminator as one string
    # -Prepare to receive a response immediately
    # -Receive the entire response from the instrument including the terminator
    # -Guarantee that no other communication is started during the response or for 30 ms after it completes
    # -Not initiate communication more than 30 times/s

    # The following delay ensures that the above conditions are satisfied, so the class uses this by default.
    communication_delay = 1 / 30  # 33.3 ms

    # The code was tested with no class send delay and the following loop:
    # if new_field_reading:
    #     get field
    # else:
    #     record a missed request
    # sleep(short_communication_delay)
    #
    # With the delay below there was always a new field point ready and the gaussmeter responded slowly enough to
    # lower the communication rate to just under 30 Hz. The upshot is that this delay may be safe to use if the
    # calling code has a significant external delay or tests for new field readings before requesting them,
    # or if it just doesn't care about duplicate field points. It's not guaranteed to work in general.
    short_communication_delay = 10e-3

    # The serial timeout
    timeout = 1

    # The serial termination character
    termination = '\n'

    # Measurement modes
    mode_to_int = {'DC': 1,
                   'RMS': 2}
    int_to_mode = {1: 'DC',
                   2: 'RMS'}

    # AC filter bandwidths
    bandwidth_to_int = {'wide': 1,
                        'narrow': 2}
    int_to_bandwidth = {1: 'wide',
                        2: 'narrow'}

    # Field units
    unit_to_int = {'Gauss': 1,
                   'Tesla': 2,
                   'Oersted': 3,
                   'Ampere/meter': 4}
    int_to_unit = {1: 'Gauss',
                   2: 'Tesla',
                   3: 'Oersted',
                   4: 'Ampere/meter'}

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

    def process_last_query(self):
        return self.send_and_receive('?')

    @property
    def identification(self):
        manufacturer, instrument_number, serial_number, firmware_version = self.send_and_receive('*IDN?').split(',')
        return manufacturer, instrument_number, serial_number, float(firmware_version)

    def reset(self):
        self.send('*RST')

    # alarm
    # alarm?
    # alarmst?

    @property
    def auto_range(self):
        return bool(self.send_and_receive('AUTO?'))

    @auto_range.setter
    def auto_range(self, boolean):
        self.send('AUTO {}'.format(int(boolean)))

    # beep
    # beep?

    # brigt
    # brigt?

    def factory_defaults(self):
        self.send('DFLT 99')

    @property
    def last_key_pressed(self):
        return int(self.send_and_receive('KEYST?'))

    @property
    def keyboard_lock(self):
        return bool(self.send_and_receive('LOCK?'))

    @keyboard_lock.setter
    def keyboard_lock(self, boolean):
        self.send('LOCK {}'.format(int(boolean)))

    @property
    def maximum_hold(self):
        return bool(self.send_and_receive('MXHOLD?'))

    @maximum_hold.setter
    def maximum_hold(self, boolean):
        self.send('MXHOLD {}'.format(int(boolean)))

    def reset_maximum_field(self):
        self.send('MXRST')

    @property
    def integer_status(self):
        return int(self.send_and_receive('OPST?'))

    @property
    def boolean_status(self):
        binary = format(self.integer_status, '08b')
        return [bool(int(b)) for b in reversed(binary)]

    @property
    def no_probe(self):
        return self.boolean_status[0]

    @property
    def field_overload(self):
        return self.boolean_status[1]

    @property
    def new_field_reading(self):
        return self.boolean_status[2]

    @property
    def alarm_condition(self):
        return self.boolean_status[3]

    @property
    def invalid_probe(self):
        return self.boolean_status[4]

    # Bit 5 is apparently not used

    @property
    def calibration_error(self):
        return self.boolean_status[6]

    @property
    def zero_probe_done(self):
        return self.boolean_status[7]

    @property
    def probe_field_compensation(self):
        return bool(self.send_and_receive('PRBFCOMP?'))

    @probe_field_compensation.setter
    def probe_field_compensation(self, boolean):
        self.send('PRBFCOMP {}'.format(int(boolean)))

    @property
    def probe_sensitivity(self):
        return float(self.send_and_receive('PRBSENS?'))

    @property
    def field_range(self):
        return int(self.send_and_receive('RANGE?'))

    @field_range.setter
    def field_range(self, range_):
        if not int(range_) in range(1, 5):
            raise ValueError("Valid ranges are 1-4")
        self.send('RANGE {}'.format(range_))

    @property
    def field(self):
        return float(self.send_and_receive('RDGFIELD?'))

    @property
    def measurement_mode(self):
        mode, filter, bandwidth = self.send_and_receive('RDGMODE?').split(',')
        return int(mode), int(filter), int(bandwidth)

    @measurement_mode.setter
    def measurement_mode(self, mode_filter_bandwidth):
        self.send('RDGMODE {}, {}, {}'.format(*mode_filter_bandwidth))

    @property
    def DC_or_RMS(self):
        mode, filter, bandwidth = self.measurement_mode
        return self.int_to_mode[mode]

    @DC_or_RMS.setter
    def DC_or_RMS(self, dc_or_rms):
        mode, filter, bandwidth = self.measurement_mode
        try:
            new_mode = self.mode_to_int[dc_or_rms.upper()]
        except AttributeError:
            new_mode = int(dc_or_rms)
        self.measurement_mode = new_mode, filter, bandwidth

    @property
    def DC_filter(self):
        mode, filter, band = self.measurement_mode
        return bool(filter)

    @DC_filter.setter
    def DC_filter(self, boolean):
        mode, filter, bandwidth = self.measurement_mode
        self.measurement_mode = mode, int(boolean), bandwidth

    @property
    def AC_bandwidth(self):
        mode, filter, bandwidth = self.measurement_mode
        return self.int_to_bandwidth[bandwidth]

    @AC_bandwidth.setter
    def AC_bandwidth(self, narrow_or_wide):
        mode, filter, bandwidth = self.measurement_mode
        try:
            new_bandwidth = self.bandwidth_to_int[narrow_or_wide.lower()]
        except AttributeError:
            new_bandwidth = int(narrow_or_wide)
        self.measurement_mode = mode, filter, new_bandwidth

    @property
    def minimum_and_maximum_field(self):
        minimum, maximum = self.send_and_receive('RDGMNMX?').split(',')
        return float(minimum), float(maximum)

    @property
    def maximum_field(self):
        return float(self.send_and_receive('RDGMX?'))

    @property
    def relative_field(self):
        return float(self.send_and_receive('RDGREL?'))

    @property
    def relative_mode(self):
        return bool(self.send_and_receive('REL?'))

    @relative_mode.setter
    def relative_mode(self, boolean):
        self.send('REL {}'.format(int(boolean)))

    # relay
    # relay?
    # relayst?

    @property
    def relative_setpoint(self):
        return float(self.send_and_receive('RELSP?'))

    # Check format
    @relative_setpoint.setter
    def relative_setpoint(self, setpoint):
        self.send('RELSP {:.3E}'.format(setpoint))

    @property
    def probe_type(self):
        return int(self.send_and_receive('TYPE?'))

    @property
    def field_units(self):
        return self.int_to_unit[int(self.send_and_receive('UNIT?'))]

    # test
    @field_units.setter
    def field_units(self, units):
        self.send('UNIT {}'.format(self.unit_to_int.get(str(units).capitalize(), units)))

    def clear_zero_probe(self):
        self.send('ZCLEAR')

    def zero_probe(self):
        self.send('ZPROBE')



