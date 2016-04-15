"""
This module contains classes to interface with SRS lock-in amplifiers.
"""
import serial


class LockinError(Exception):
    pass


class SR830(object):

    termination = '\n'

    # TODO: figure out the acceptable formats for floats
    float_format = ':.6f'

    def __init__(self, serial_device, baud_rate=19200, timeout=1):
        self.serial = serial.Serial(serial_device, baudrate=baud_rate, timeout=timeout, rtscts=True)
        self.name = "lockin"

    def send(self, message):
        self.serial.write(message + self.termination)

    def receive(self):
        return self.serial.readline().strip()

    def send_and_receive(self, message):
        self.send(message)
        return self.receive()

    @property
    def state(self):
        return dict(rms_voltage=self.R, time_constant=self.time_constant, sensitivity=self.sensitivity)
    # The commands are listed in the same order as in the manual.

    # Reference and phase commands

    @property
    def phase(self):
        """
        This is the phase in degrees, represented by a float. It implements the PHAS (?) command.
        """
        return float(self.send_and_receive('PHAS?'))

    @phase.setter
    def phase(self, phase):
        self.send(('PHAS {' + self.float_format + '}').format(phase))

    @property
    def reference_source(self):
        """
        This is the reference source, represented by an int. It implements the FMOD (?) command.
        """
        return int(self.send_and_receive('FMOD?'))

    @reference_source.setter
    def reference_source(self, source):
        self.send('FMOD {:d}'.format(source))

    @property
    def reference_frequency(self):
        """
        This is the reference frequency in Hertz, represented by a float. It implements the FREQ (?) command.
        """
        return float(self.send_and_receive('FREQ?'))

    @reference_frequency.setter
    def reference_frequency(self, frequency):
        self.send(('FREQ {' + self.float_format + '}').format(frequency))

    # RSLP

    # HARM

    # SLVL

    # ISRC

    # IGND

    # ICPL

    # ILIN

    # Gain and time constant commands

    @property
    def sensitivity(self):
        """
        This is the sensitivity, represented by an int. See the manual. It implements the SENS (?) command.
        """
        return int(self.send_and_receive('SENS?'))

    @sensitivity.setter
    def sensitivity(self, integer):
        self.send('SENS {:d}'.format(integer))

    # RMOD

    @property
    def time_constant(self):
        """
        This is the output time constant, represented by an int. See the manual. It implements the OFLT (?) command.
        """
        return int(self.send_and_receive('OFLT?'))

    @time_constant.setter
    def time_constant(self, integer):
        self.send('OFLT {:d}'.format(integer))

    # OFSL

    # SYNC

    # Display and output commands

    # DDEF

    # FPOP

    # OEXP

    # AOFF

    # Aux input and output commands

    # OAUX

    # AUXV

    # Setup commands

    # OUTX

    # OVRM

    # KLCK

    # ALRM

    # SSET

    # RSET

    # Auto functions

    def auto_gain(self):
        self.send('AGAN')

    def auto_reserve(self):
        self.send('ARSV')

    def auto_phase(self):
        self.send('APHS')

    def auto_offset_X(self):
        self.send('AOFF 1')

    def auto_offset_Y(self):
        self.send('AOFF 2')

    def auto_offset_R(self):
        self.send('AOFF 3')

    # Data storage commands

    @property
    def sample_rate(self):
        """
        This is the sample rate, represented by an int. See the manual. It implements the SRAT command.
        """
        return int(self.send_and_receive('SRAT?'))

    @sample_rate.setter
    def sample_rate(self, integer):
        self.send('SRAT {:d}'.format(integer))

    # SEND

    # TRIG

    # TSTR

    # STRT

    # PAUS

    # REST

    # Data transfer commands

    # OUTP

    @property
    def X(self):
        return float(self.send_and_receive('OUTP? 1'))

    @property
    def Y(self):
        return float(self.send_and_receive('OUTP? 2'))

    @property
    def R(self):
        return float(self.send_and_receive('OUTP? 3'))

    @property
    def theta(self):
        return float(self.send_and_receive('OUTP? 4'))

    # OUTR

    # SNAP
    def snap(self, *parameters):
        message = 'SNAP? ' + ','.join([str(int(p)) for p in parameters])
        response = self.send_and_receive(message)
        return [float(s) for s in response.split(',')]

    # OAUX

    @property
    def aux1(self):
        return float(self.send_and_receive('OAUX? 1'))

    @property
    def aux2(self):
        return float(self.send_and_receive('OAUX? 2'))

    @property
    def aux3(self):
        return float(self.send_and_receive('OAUX? 3'))

    @property
    def aux4(self):
        return float(self.send_and_receive('OAUX? 4'))

    # SPTS

    @property
    def n_stored_points(self):
        return int(self.send_and_receive('SPTS?'))

    # TRCA

    # TRCB

    # TRCL

    # FAST

    # STRD

    # Interface commands

    def reset(self):
        """
        Reset the lock-in to its default configuration.

        This method implements the *RST command.
        """
        self.send('*RST')

    @property
    def identification(self):
        """
        This property implements the *IDN command.

        :return: a four-element tuple containing identification information.
        """
        return tuple(self.send_and_receive('*IDN?').split(','))

    @property
    def local(self):
        """
        This property implements the LOCL command.
        """
        return int(self.send_and_receive('LOCL?'))

    @local.setter
    def local(self, integer):
        self.send('LOCL {:d}'.format(integer))

    # OVRM

    def trigger(self):
        """
        This method implements the TRIG command.
        """
        self.send('TRIG')

    # Status reporting commands

    def clear_status(self):
        """
        This method implements the *CLS command.
        """
        self.send('*CLS')

    # *ESE

    # *ESR

    @property
    def input_queue_overflow(self):
        return bool(int(self.send_and_receive('*ESR? 0')))

    @property
    def output_queue_overflow(self):
        return bool(int(self.send_and_receive('*ESR? 2')))

    @property
    def execution_or_parameter_error(self):
        return bool(int(self.send_and_receive('*ESR? 4')))

    @property
    def illegal_command(self):
        return bool(int(self.send_and_receive('*ESR? 5')))

    @property
    def key_pressed(self):
        return bool(int(self.send_and_receive('*ESR? 6')))

    @property
    def power_on(self):
        return bool(int(self.send_and_receive('*ESR? 7')))

    # *SRE

    # STB

    @property
    def no_scan_in_progress(self):
        return bool(int(self.send_and_receive('*STB? 0')))

    @property
    def no_command_in_progress(self):
        return bool(int(self.send_and_receive('*STB? 1')))

    @property
    def any_error_status(self):
        return bool(int(self.send_and_receive('*STB? 2')))

    @property
    def any_lockin_status(self):
        return bool(int(self.send_and_receive('*STB? 3')))

    @property
    def interface_output_buffer_nonempty(self):
        return bool(int(self.send_and_receive('*STB? 4')))

    @property
    def any_standard_status(self):
        return bool(int(self.send_and_receive('*STB? 5')))

    @property
    def service_request(self):
        return bool(int(self.send_and_receive('*STB? 6')))

    # *PSC

    # ERRE

    # ERRS

    @property
    def battery_error(self):
        return bool(int(self.send_and_receive('ERRS? 1')))

    @property
    def ram_error(self):
        return bool(int(self.send_and_receive('ERRS? 2')))

    @property
    def rom_error(self):
        return bool(int(self.send_and_receive('ERRS? 4')))

    @property
    def gpib_error(self):
        return bool(int(self.send_and_receive('ERRS? 5')))

    @property
    def dsp_error(self):
        return bool(int(self.send_and_receive('ERRS? 6')))

    @property
    def math_error(self):
        return bool(int(self.send_and_receive('ERRS? 7')))

    # LIAE

    # LIAS

    @property
    def input_overload(self):
        return bool(int(self.send_and_receive('LIAS? 0')))

    @property
    def filter_overload(self):
        return bool(int(self.send_and_receive('LIAS? 1')))

    @property
    def output_overload(self):
        return bool(int(self.send_and_receive('LIAS? 2')))

    @property
    def reference_unlock(self):
        return bool(int(self.send_and_receive('LIAS? 3')))

    @property
    def reference_unlock(self):
        return bool(int(self.send_and_receive('LIAS? 3')))

    @property
    def frequency_range_switch(self):
        return bool(int(self.send_and_receive('LIAS? 4')))

    @property
    def time_constant_changed(self):
        return bool(int(self.send_and_receive('LIAS? 5')))

    @property
    def triggered(self):
        return bool(int(self.send_and_receive('LIAS? 6')))

Lockin = SR830