import serial
import warnings
import numpy as np

class Keithley2400(object):
    termination = '\r'
    name = "sourcemeter"

    def __init__(self, serial_device, baud_rate=9600, timeout=1):
        self.serial = serial.Serial(serial_device, baudrate=baud_rate, timeout=timeout, rtscts=True)

    def send(self, message):
        self.serial.write(message + self.termination)

    def receive(self):
        #return self.serial.readline().strip()
        return self.read_until_terminator()

    def read_until_terminator(self):
        characters = []
        while True:
            character = self.serial.read()
            if not character:  # self.serial has timed out.
                warnings.warn("Serial port timed out while reading.")
                break
            elif character == self.termination:
                break
            else:
                characters.append(character)
        return ''.join(characters).rstrip()  # Some commands seem to return both a space and carriage return.

    def send_and_receive(self, message):
        self.send(message)
        return self.receive()

    def identify(self):
        return self.send_and_receive("*IDN?")

    def set_output(self,on=False):
        self.send(":OUTPUT:STATE %d" % int(on))

    def enable_output(self):
        self.set_output(True)
    def disable_output(self):
        self.set_output(False)

    def measure_current(self):
        return float(self.send_and_receive(":MEASURE:CURRENT?"))

    def measure_voltage(self):
        values = [float(x) for x in self.send_and_receive(":MEASURE:VOLTAGE?").split(',')]
        return values[0],values[1]

    def set_current_source(self,compliance=3.1, max_current=20e-3):
        self.set_output(False)
        self.send(":SOURCE:FUNC:MODE CURRENT")
        self.send(":SOURCE:CURRENT:MODE FIX")
        self.send(":SENSE:VOLT:PROT:LEV %f" % compliance)
        self.send(":SOURCE:CURRENT:RANGE %f" % max_current)
        self.set_current_amplitude(0.0)

    def set_current_amplitude(self,current):
        self.send(":SOURCE:CURRENT %f" % current)

    def get_current_amplitude(self):
        return float(self.send_and_receive(":SOURCE:CURRENT?"))

    @property
    def state(self):
        volts,current = self.measure_voltage()
        return dict(voltage=volts,current=current)

SourceMeter = Keithley2400