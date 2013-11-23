# -*- coding: utf-8 -*- 

import numpy as np

from intervalo import *
from difauto import *

# funciones

def g(x) :
    return (x**2 - 4)

def g_p(x) :
    return 2*x
    
def h(x) :
    # return x*x*x - 3*x*x + 2*x
    # return x*np.exp(x) - 1
    return x - 3.2*(3.2*(x - x**2) - 10.24*(x - x**2)**2)
    # return 0.5*np.sin(x)
    # return x*np.sin(1.0/x)
    # return x - 3.3*x*(1-x)

def f(x):
    return 3.2*x*(1-x)

def f_n(x) :
    n = 2
    if n > 1:
        return f(f(x))
    else :
        return f(x)

def f_real(x):
    return x - f_n(x)
    
def f_deriv(x) :
    return f_real(DifAuto(x,1)).deriv


def h_p(x) :
    
    def hh_p(x):
        # return 3*x*x - 6*x + 2
        # return np.exp(x)*x + np.exp(x)
        # return 12*x**2 - 2
        # return 0.5*np.cos(x)
        # return np.sin(1.0/x) - np.cos(1.0/x)/x
        # return h(DifAuto(x,1)).deriv
        return 1 - 3.2*(3.2*(1 - 2*x) - 20.48*(1 - 2*x)*(x - x**2))
    
    n = 1000
    epsilon = float(x.hi - x.lo)/n
    current_x = x.lo
    
    for i in range(1,n) :
        micro_x = Intervalo(current_x, current_x + epsilon)
        current_x += epsilon
        
        this_y = hh_p(micro_x)
        if i == 1 :
            y_final = this_y
        else:
            y_final = Intervalo.hull(y_final, this_y)
        
    return y_final

def met_newton(x, f, f_p, steps = 10000, epsilon = 1e-3) :
    # x       - intervalo
    # f       - función
    # f_p     - derivada de la función f
    # steps   - número máximo de iteraciones
    # epsilon - tolerancia para encontrar la raíz
    
    
    ceros = []
    intervalos = [x]
    index = 0
    terminar_ciclo = False
    
    while index < steps :
        
        cuenta_tolerancia = 0
        nuevos_intervalos = []
        
        for x in intervalos :
            if 0 in f_p(x) and (f_p(x).lo != 0 and f_p(x).hi != 0):
                # el reciproco de f_p(x) va a devolver 2 intervalos
                
                x_1 = x & (x.middle() - f(x.middle())*f_p(x).reciprocal()[0])
                x_2 = x & (x.middle() - f(x.middle())*f_p(x).reciprocal()[1])
                
                # print "hey corte ", x
                
                if not isinstance(x_1, Intervalo) and not isinstance(x_2, Intervalo):
                    nuevos_intervalos.append(x)
                else :
                    if x_1 in x :
                        # print "inclui x_1", x_1
                        nuevos_intervalos.append(x_1) 
                    if x_2 in x :
                        # print "inclui x_2", x_2
                        nuevos_intervalos.append(x_2)
            else :
                x_new = x & (x.middle() - f(x.middle())*f_p(x).reciprocal())
                if not isinstance(x_new, Intervalo) :
                    x_new = x
                if x_new in x:
                    # print "no corte", x, "e inclui x_new", x_new
                    nuevos_intervalos.append(x_new)
        
        nuevos_intervalos[:] = (value for value in nuevos_intervalos if isinstance(value, Intervalo))
        for x_new in nuevos_intervalos :
            if abs(x_new.width()) < epsilon :
                cuenta_tolerancia += 1
                
        if cuenta_tolerancia == len(nuevos_intervalos) :
            intervalos = nuevos_intervalos
            terminar_ciclo = True
        
        # print "antes:", intervalos
        intervalos = nuevos_intervalos
        # print "despues", intervalos
        # print "fin de vuelta"
        
        
        if terminar_ciclo == True :
            break
        index += 1
    
    intervalos[:] = (value for value in intervalos if value.width() < epsilon)
    ceros = intervalos
    return ceros

