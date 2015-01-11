from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# This data is transcribed in a very sloppy way from the load curve
# pdf.  Improve. Points in L1 (L2) correspond to points in T1 (T2),
# but the 1st and 2nd stage arrays have transposed shapes.
L1 = np.array([[ 0.0, 20.0, 30.0, 37.0],
               [ 0.0, 20.0, 30.0, 37.0],
               [ 0.0, 20.0, 30.0, 37.0],
               [ 0.0, 20.0, 30.0, 37.0],
               [ 0.0, 20.0, 30.0, 37.0]])

T1 = np.array([[29.5, 44.0, 54.5, 64.5],
               [30.0, 45.0, 55.0, 64.5],
               [30.5, 45.5, 56.0, 65.0],
               [31.0, 46.0, 56.5, 65.0],
               [31.5, 46.5, 57.0, 65.5]])

L2 = np.array([[0.00, 0.3, 0.5, 0.7, 1.00],
               [0.00, 0.3, 0.5, 0.7, 1.00],
               [0.00, 0.3, 0.5, 0.7, 1.00],
               [0.00, 0.3, 0.5, 0.7, 1.00]])

T2 = np.array([[2.25, 3.50, 4.20, 4.70, 5.25],
               [2.35, 3.40, 3.80, 4.30, 4.80],
               [2.40, 3.30, 3.75, 4.20, 4.75],
               [2.45, 3.25, 3.70, 4.15, 4.70]])

interp_L1 = interp2d(T1, T2.T, L1)
interp_L2 = interp2d(T1.T, T2, L2)
interp_T1 = interp2d(L1, L2.T, T1)
interp_T2 = interp2d(L1.T, L2, T2)

def temp_to_load(t1, t2):
    return interp_t1(t1), interp_t2(t2)

def capacity_curve():
    fig = plt.figure()
    for l1 in range(T1.shape[0]):
        plt.plot(T1[l1, :], T2[:, l1], linestyle='solid', marker='.', color='b')
    for l2 in range(T2.shape[0]):
        plt.plot(T1[:, l2], T2[l2, :], linestyle='solid', marker='.', color='b')
    plt.xlabel('First stage temperature [K]')
    plt.ylabel('Second stage temperature [K]')
    plt.title('PT407 capacity curve')
    return fig
