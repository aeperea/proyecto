# -*- coding: utf-8 -*- 

import numpy as np
from difauto import *

def met_newton(f, x0, steps=10000, tolerance=0.000001):
    
    i = 1
    while i < steps :
        x1 = x0 - f(x0)/f(DifAuto(x0,1)).deriv
        t = np.abs(x1 - x0)
        if t < tolerance:
            break
        x0 = x1
        i += 1
    return x0