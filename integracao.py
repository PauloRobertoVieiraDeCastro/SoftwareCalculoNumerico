import pandas as pd
import numpy as np
import math as mat

def trapezio(v,a,b,n=100):
    h = (b - a)/n
    y0 = v(a)
    y = []
    for i in range(n-1):
        a += h
        y.append(v(a))
    I = h*(y0 + 2*np.sum(y) + v(b))/2.0
    return I

def simpson1(v,a,b,n=100):
    h = (b - a)/n
    y0 = v(a)
    yf = v(b)
    x = np.linspace(a,b,n+1)
    S1 = ([v(x[i]) for i in range(1,n,2)])
    S2 = ([v(x[i]) for i in range(2,n-1,2)])
    I = h*(y0 + yf + 4*sum(S1) + 2*sum(S2))/3
    return I

def simpson2(v,a,b,n=100):
    h = (b - a)/n
    x = np.linspace(a,b,n+1)
    S1 = []
    for j,i in enumerate(x):
        if j == 0:
            S1.append(v(i))
        elif j == n:
            S1.append(v(i))
        elif j%3 == 0:
            S1.append(2*v(i))
        else:
            S1.append(3*v(i))
    return 3*h*(sum(S1))/8

def quad(v,a,b):
    I = ((b - a)/2)*( v(((a + b)/2) - ((b - a)/(2*mat.sqrt(3)))) + v(((a + b)/2) + ((b - a)/(2*mat.sqrt(3)))) )
    return I

def boole(v,a,b,n=100):
    h = (b - a)/n
    x = np.linspace(a,b,n+1)
    S1 = []
    for j,i in enumerate(x):
        if j == 0 or j == n:
            S1.append(7*v(i))
        elif j%2 == 1:
            S1.append(32*v(i))
        else:
            if j%4 == 0:
                S1.append(14*v(i))
            else:
                S1.append(12*v(i))
    return 2*h*(sum(S1))/45

def doubletrap(f,a,b,c,d,n=100): #integral dupla por trapézios
    dx,dy = (b - a)/n,(d - c)/n
    somadois = 0
    x,y = np.linspace(a,b,n),np.linspace(c,d,n)
    integralxx = 0
    for i in range(0,n):
        soma = 0
        integralxx = 0
        for j in range(0,n):
            soma += f(x[j],y[i])
        integralxx += (f(a,y[i]) + f(b,y[i]) + 2*soma)*dx/2
        if i==0 or i==n:
            somadois += dy*integralxx/2
        else:
            somadois += dy*integralxx
    return somadois

def tripletrap(ff,a,b,c,d,e,g,n=100):
    dx,dy,dz = (b - a)/n,(d - c)/n,(g - e)/n
    x,y,z = np.linspace(a,b,n),np.linspace(c,d,n),np.linspace(e,g,n)
    somatres = 0
    for i in range(0,n):
        somadois = 0
        for j in range(0,n):
            soma = 0
            integralx = 0
            for k in range(0,n):
                soma += ff(x[k],y[j],z[i])
            integralx += (ff(a,y[j],z[i]) + ff(b,y[j],z[i]) + 2*soma)*dx/2
            if j == 0 or j == n:
                somadois += dy*integralx/2
            else:
                somadois += dy*integralx
                                    
        if i == 0 or i == n:
            somatres += dz*somadois/2
        else:
            somatres += dz*somadois
    return somatres

def doublesimp1(f,a,b,c,d,n=100): #integral dupla por trapézios
    dx,dy = (b - a)/n,(d - c)/n
    somadois = 0
    x,y = np.linspace(a,b,n),np.linspace(c,d,n)
    integralxx = 0
    for i in range(0,n):
        soma = 0
        integralxx = 0
        for j in range(0,n):
            if j%2 == 1:
                soma += 4*f(x[j],y[i])
            elif j%2 == 0 and j>0: 
                soma += 2*f(x[j],y[i])
        integralxx += (f(a,y[i]) + f(b,y[i]) + soma)*dx/3
        if i==0 or i==n:
            somadois += dy*integralxx/3
        elif i%2 == 1:
            somadois += 4*dy*integralxx/3
        elif i%2 == 0:
            somadois += 2*dy*integralxx/3
    return somadois

def triplesimp1(f,a,b,c,d,e,g,n=100):
    dx,dy,dz = (b - a)/n,(d - c)/n,(g - e)/n
    x,y,z = np.linspace(a,b,n),np.linspace(c,d,n),np.linspace(e,g,n)
    somatres = 0
    for i in range(0,n):
        somadois = 0
        for j in range(0,n):
            soma = 0
            integralx = 0
            for k in range(0,n):
                if k%2 == 1:
                    soma += 4*f(x[k],y[j],z[i])
                elif k%2 == 0 and k>0: 
                    soma += 2*f(x[k],y[j],z[i])
                    
            integralx += (f(a,y[j],z[i]) + f(b,y[j],z[i]) + soma)*dx/3
            if j==0 or j==n:
                somadois += dy*integralx/3
            elif j%2 == 1:
                somadois += 4*dy*integralx/3
            elif j%2 == 0:
                somadois += 2*dy*integralx/3
                                    
        if i==0 or i==n:
            somatres += dz*somadois/3
        elif i%2 == 1:
            somatres += 4*dz*somadois/3
        elif i%2 == 0:
            somatres += 2*dz*somadois/3
    return somatres

def doublesimp2(f,a,b,c,d,n=100): #integral dupla por simpson 3/8
    dx,dy = (b - a)/n,(d - c)/n
    somadois = 0
    x,y = np.linspace(a,b,n+1),np.linspace(c,d,n+1)
    integralxx = 0
    for i in range(0,n+1):
        soma = 0
        integralxx = 0
        for j in range(0,n+1):
            if j == 0 or j == n:
                soma += f(x[j],y[i])
            elif j%3 == 0: 
                soma += 2*f(x[j],y[i])
            else:
                soma += 3*f(x[j],y[i])
        integralxx += 3*(soma)*dx/8
        if i==0 or i==n:
            somadois += 3*dy*integralxx/8
        elif i%3 == 0:
            somadois += 3*4*dy*integralxx/8
        else:
            somadois += 3*2*dy*integralxx/8
    return somadois

def triplesimp2(f,a,b,c,d,e,g,n=100):
    dx,dy,dz = (b - a)/n,(d - c)/n,(g - e)/n
    x,y,z = np.linspace(a,b,n+1),np.linspace(c,d,n+1),np.linspace(e,g,n+1)
    somatres = 0
    for i in range(0,n+1):
        somadois = 0
        for j in range(0,n+1):
            soma = 0
            integralx = 0
            for k in range(0,n+1):
                if k == 0  or k == n:
                    soma += f(x[k],y[j],z[i])
                elif k%3 == 0:
                    soma += 2*f(x[k],y[j],z[i])
                else: 
                    soma += 3*f(x[k],y[j],z[i])
                    
            integralx += 3*(soma)*dx/8
            if j==0 or j==n:
                somadois += 3*dy*integralx/8
            elif j%3 == 0:
                somadois += 3*4*dy*integralx/8
            else:
                somadois += 3*2*dy*integralx/8
                                    
        if i==0 or i==n:
            somatres += 3*dz*somadois/8
        elif i%3 == 0:
            somatres += 3*4*dz*somadois/8
        else:
            somatres += 3*2*dz*somadois/8
    return somatres

def doubleboole(f,a,b,c,d,n=100): #integral dupla por simpson 3/8
    dx,dy = (b - a)/n,(d - c)/n
    somadois = 0
    x,y = np.linspace(a,b,n+1),np.linspace(c,d,n+1)
    integralxx = 0
    for i in range(0,n+1):
        soma = 0
        integralxx = 0
        for j in range(0,n+1):
            if j == 0 or j == n:
                soma += 7*f(x[j],y[i])
            elif j%2 == 1: 
                soma += 32*f(x[j],y[i])
            else:
                if j%4 == 0:
                    soma += 14*f(x[j],y[i])
                else:
                    soma += 12*f(x[j],y[i])
        integralxx += 2*(soma)*dx/45
        if i==0 or i==n:
            somadois += 7*2*dy*integralxx/45
        elif i%2 == 1:
            somadois += 32*2*dy*integralxx/45
        else:
            if i%4 == 0:
                somadois += 14*2*dy*integralxx/45
            else:
                somadois += 12*2*dy*integralxx/45
    return somadois

def tripleboole(f,a,b,c,d,e,g,n=100):
    dx,dy,dz = (b - a)/n,(d - c)/n,(g - e)/n
    x,y,z = np.linspace(a,b,n+1),np.linspace(c,d,n+1),np.linspace(e,g,n+1)
    somatres = 0
    for i in range(0,n+1):
        somadois = 0
        for j in range(0,n+1):
            soma = 0
            integralx = 0
            for k in range(0,n+1):
                if j == 0 or j == n:
                    soma += 7*f(x[k],y[j],z[i])
                elif j%2 == 1: 
                    soma += 32*f(x[k],y[j],z[i])
                else:
                    if j%4 == 0:
                        soma += 14*f(x[k],y[j],z[i])
                    else:
                        soma += 12*f(x[k],y[j],z[i])
            integralx += 2*(soma)*dx/45
            if j==0 or j==n:
                somadois += 7*2*dy*integralx/45
            elif j%2 == 1:
                somadois += 32*2*dy*integralx/45
            else:
                if j%4 == 0:
                    somadois += 14*2*dy*integralx/45
                else:
                    somadois += 12*2*dy*integralx/45
                                    
        if i==0 or i==n:
            somatres += 7*2*dz*somadois/45
        elif i%2 == 1:
            somatres += 32*2*dz*somadois/45
        else:
            if i%4 == 0:
                somatres += 14*2*dz*somadois/45
            else:
                somatres += 12*2*dz*somadois/45
                                    
    return somatres
