"""
Figure out which model of oscilloscope we have.
"""

import numpy as np

def load_csv(filename):
    with open(filename) as f:
        header = [f.readline()]
        while header[-1].split(',')[0] != 'TIME':
            header.append(f.readline())
        columns = header[-1].rstrip().split(',')
    data = np.loadtxt(filename, skiprows=len(header), delimiter=',',
                    dtype=[(column, np.float) for column in columns]).view(np.recarray)
    return data, header
