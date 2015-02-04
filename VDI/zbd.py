import os
import numpy as np
import pandas as pd

class ZBD(object):

    xlsx_filename = '13067-columbia-wr6.5zbd-datapoints.xlsx'

    def __init__(self):
        data = pd.ExcelFile(os.path.join(os.path.dirname(__file__), self.xlsx_filename)).parse('Sheet1')
        self.frequency_data_Hz = 1e9 * np.array(data['Freq (GHz)'])
        self.responsivity_data_V_per_W = np.array(data['Responsivity (V/W)'])

    def responsivity(self, frequency):
        return np.interp(frequency, self.frequency_data_Hz, self.responsivity_data_V_per_W)
