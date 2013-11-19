# -*- coding: utf-8 -*- 

import numpy as np
from intervalo import *
from matplotlib import pyplot as plt

# Función cuadrática
def f(x,r) :
    return r*x*(1-x)

def mapeo(r, x = 0.2, lista_r = None, lista_x = None, datos_a_guardar = 100, eps = 10e-8):
        if lista_r is None:
            lista_r = []
        if lista_x is None:
            lista_x = []

        primeras_iteraciones = 1000
        rango = primeras_iteraciones + datos_a_guardar
        for i in range(rango):
            if i > primeras_iteraciones:
                lista_x.append(x)
                lista_r.append(r)
            x = f(x,r)
        M = np.array([lista_r, lista_x] )    
        plt.plot( M[0], M[1], '.', markersize = .8, color = 'black' )
        return [r, M[1]]

def encontrar_puntos(r) :
    a = mapeo(r)[1];
    # borrar valores repetidos
    seen = set()
    seen_add = seen.add
    res = [ x for x in a if x not in seen and not seen_add(x)]
    res.sort()
    return res

def r_mapeo(R, n, x0 = 0.2, eps = 10e-8, lista_r = None, lista_x = None, M = None) :
    delta_r = float(R.hi - R.lo)/n

    r = R.lo
    while r <= R.hi :
        r += delta_r
        a = mapeo(r, x0, lista_r, lista_x)
    else :
        plt.show()
        
def cobweb(r, x0=0.2, steps=1000, eps=1e-7):
    x = np.linspace(0,1,1001)
    y = f(x, r)
    plt.plot(x, y, color="purple")
    plt.plot(x, x, color="blue")
    plt.axis([0, 1, 0, 1])
    i = 1

    while (i < steps) :
        xn = f(x0, r)
        if i == 1 :
            plt.plot([x0,x0],[0,f(x0,r)], color="red")

        plt.plot([xn,xn],[f(x0,r),f(xn,r)], color="red")     
        plt.plot([x0,xn],[f(x0,r),xn], color="red")

        if np.abs(xn - x0) < eps :
            break

        x0 = xn
        i += 1

    plt.grid()
    plt.show()

def prob_function(r, x0 = 0.2, steps=2000) :
    a = mapeo(r, x0, None, None, steps)[1]
    num_bins = 100
    plt.hist(a, num_bins, color='blue',alpha=0.9)
    lim_y = steps/10
    plt.axis([0,1,0, lim_y])
    plt.grid()
    plt.show()
