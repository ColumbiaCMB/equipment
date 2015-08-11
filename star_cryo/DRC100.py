from __future__ import division

from datetime import datetime
import numpy as np

class LogFile(object):

    def __init__(self, filename, start=datetime(2013, 1, 1)):
        self.start = start
        with open(filename) as f:
            self.data = np.genfromtxt(f, names=True, delimiter=',', converters={0: self.convert_timestamp})

    def convert_timestamp(self, timestamp):
        dt = datetime.strptime('{}000'.format(timestamp), '%m/%d/%Y %H:%M:%S.%f')
        return (dt - self.start).total_seconds()
