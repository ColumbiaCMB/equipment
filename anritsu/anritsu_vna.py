from __future__ import division

from os.path import splitext
import numpy as np

class Sweep(object):

    def __init__(self, filename, header_rows=42):
        if splitext(filename)[-1] == '.csv':
            with open(filename, 'r') as csv:
                f_phase, self.phase, f_mag, self.mag = np.loadtxt(csv,
                                                        delimiter=',',
                                                        skiprows=header_rows,
                                                        usecols=(1, 2, 3, 4),
                                                        unpack=True)
            if not np.all(f_phase == f_mag):
                raise ValueError("Frequencies for phase and magnitude points do not match.")
            if not f_phase.size == self.phase.size == self.mag.size:
                raise ValueError("Numbers of points do not match.")
            self.f = f_phase
            self.S21 = 10**(self.mag / 20) * np.exp(1j * np.radians(self.phase))

