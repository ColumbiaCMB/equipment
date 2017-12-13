"""
Jackson Labs Fury
"""
import serial


class Fury(object):

    termination = '\r'
    name = "fury"
    baud_rate = 115200

    def __init__(self, serial_device, timeout=1):
        self.serial = serial.Serial(serial_device, baudrate=self.baud_rate, timeout=timeout, rtscts=True)

    def send(self, message):
        self.serial.write(message + self.termination)

    def receive(self):
        return self.serial.readline().strip()
        #return self.read_until_terminator()

    def read_until_terminator(self):
        characters = []
        while True:
            character = self.serial.read()
            if not character:  # self.serial has timed out.
                print("Serial port timed out while reading.")
                break
            elif character == self.termination:
                break
            else:
                characters.append(character)
        return ''.join(characters).rstrip()  # Some commands seem to return both a space and carriage return.

    def send_and_receive(self, message):
        self.send(message)
        return self.receive()
