import os
import numpy as np
import pandas as pd


class ZBD(object):

    # This is -15 dBm, or about 32 uW, which is the maximum power that keeps the output compression under 0.5 dB.
    maximum_linear_power = 1e-3 * 10**(-15 / 10)

    def __init__(self):
        this_directory = os.path.dirname(__file__)
        self.frequency_data_Hz = np.load(os.path.join(this_directory, 'frequency_data_Hz.npy'))
        self.responsivity_data_V_per_W = np.load(os.path.join(this_directory, 'responsivity_data_V_per_W.npy'))

    def responsivity(self, frequency):
        return np.interp(frequency, self.frequency_data_Hz, self.responsivity_data_V_per_W)

    def maximum_linear_voltage(self, frequency):
        return self.maximum_linear_power * self.responsivity(frequency)


def excel_to_npy():
    xlsx_filename = '13067-columbia-wr6.5zbd-datapoints.xlsx'
    this_directory = os.path.dirname(__file__)
    data = pd.ExcelFile(os.path.join(this_directory, xlsx_filename)).parse('Sheet1')
    frequency_data_Hz = 1e9 * np.array(data['Freq (GHz)'])
    responsivity_data_V_per_W = np.array(data['Responsivity (V/W)'])
    np.save(os.path.join(this_directory, 'frequency_data_Hz.npy'), frequency_data_Hz)
    np.save(os.path.join(this_directory, 'responsivity_data_V_per_W.npy'), responsivity_data_V_per_W)
