# -*- coding: utf-8 -*- 

import numpy as np
from matplotlib import pyplot as plt

from intervalo import *
from difauto import *

# Funciones de prueba usadas por LauraMA
def identidad(x) :
    return x

def cte2(x) :
    return Intervalo(2)
    
def g(x) :
    return x*x - 1
    
def h(x) :
    return x*x*x - 3*x*x + 2*x

# Función de prueba para mis tests j(x)
# x = 1
# x = 2
# x = 1/2(3 - sqrt(3))
# x = 1/2(3 + sqrt(3))

def j(x) :
    return x*(x*(x*(2*x - 12) + 25) - 21) + 6 

def f(x):
    return 3.5*x*(1-x)

def f_n(x) :
    n = 2
    if n > 1:
        return f(f(x))
    else :
        return f(x)

def f_real(x):
    return x - f(f(f(f(x))))

def f_deriv(x) :
    return f_real(DifAuto(x,1)).deriv

def met_biseccion(x, f, n) :
    """
    Este método, a diferencia de otros más elegantes, no hace uso de un valor de tolerancia, sino más bien se le da
    una cantidad finita de pasos para dividir el Intervalo. Esto conlleva a que pueden darse dos micro_intervalos consecutivos que
    contengan el mismo cero. Para esto fue necesario analizar si el cero anterior enlistado está a una distancia menor o igual a
    la del epsilon producto del step. 
    """
    # x - intervalo
    # f - función
    # n - steps
    
    epsilon = float(x.hi - x.lo)/n
    current_x = x.lo
    posibles_ceros = []
    
    for i in range(1, n) :
        micro_intervalo = Intervalo(current_x, current_x + epsilon)
        current_x += epsilon
        
        this_y = f(micro_intervalo)
        if i == 1 :
            y_final = this_y
        else:
            y_final = Intervalo.hull(y_final, this_y)
        if 0 in this_y and (this_y.lo * this_y.hi < 0) :
            if posibles_ceros == [] :
                posibles_ceros.append(micro_intervalo)
            elif micro_intervalo.lo - posibles_ceros[-1].hi <= epsilon :
                posibles_ceros[-1].hi = micro_intervalo.hi
            else :
                posibles_ceros.append(micro_intervalo)
            
    return posibles_ceros


