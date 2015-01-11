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

    # From manual
    communication_delay = 30e-3

    # The serial timeout
    timeout = 1

    # The serial termination character
    termination = '\n'

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
        self.send(message)
        return self.receive()

    def process_last_query(self):
        return self.send_and_receive('?')

    @property
    def identification(self):
        return self.send_and_receive('*IDN?')

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
        self.send('AUTO? {}'.format(int(boolean)))

    # beep
    # beep?

    # brigt
    # brigt?

    def factory_defaults(self):
        self.send('DFLT 99')

    # keyst?

    # lock
    # lock?

    # mxhold
    # mxhold?

    # opst?

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

    # Rename
    @property
    def measurement_mode(self):
        return self.send_and_receive('RDGMODE?')

    @measurement_mode.setter
    def measurement_mode(self, mode_filter_band):
        self.send('RDGMODE {}, {}, {}'.format(*mode_filter_band))

    @property
    def DC_or_RMS(self):
        pass

    @property
    def DC_filter_on(self):
        mode, filter, band = self.measurement_mode
        return bool(mode)

    @DC_filter_on.setter
    def DC_filter_on(self, boolean):
        mode, filter, band = self.measurement_mode
        self.measurement_mode = mode, int(filter), band

    @property
    def RMS_bandwidth(self):
        pass


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
        self.send('UNIT {}'.format(int(self.unit_to_int.get(str(units).capitalize(), units))))

    def clear_zero_probe(self):
        self.send('ZCLEAR')

    def zero_probe(self):
        self.send('ZPROBE')



