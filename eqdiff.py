import numpy as np
import math as mat
import matplotlib.pyplot as plt
import pandas as pd

def eulerexplicito(f, t0, x0, dt, nsteps):
    tf = t0 + nsteps*dt
    xs = []
    t = np.linspace(t0,tf,nsteps+1)
    for i in t:
        x = x0 + dt*f(i,x0)
        xs.append(x)
        x0 = x
    df = pd.DataFrame([t,xs]).T
    df.columns = ['t','y']
    return df

def rungekutta4(f, t0, x0, dt, nsteps):
    tf = t0 + nsteps*dt
    xs = []
    t = np.linspace(t0,tf,nsteps+1)
    for i in t:
        k1 = dt*f(i,x0)
        k2 = dt*f(i+dt/2,x0+k1/2)
        k3 = dt*f(i+dt/2,x0+k2/2)
        k4 = dt*f(i+dt,x0+k3)
        x = x0 + (k1/6 + k2/3 + k3/3 + k4/6)
        xs.append(x)
        x0 = x
    df = pd.DataFrame([t,xs]).T
    df.columns = ['t','y']
    return df

def implicitoeuler(f, t0, x0, dt, nsteps):
    def NewtonRaphson(g,x00,tol=1e-7,it=500):
        def df(g,x00,tol=1e-7):
            return (g(x00+0.01*tol) - g(x00))/(0.01*tol)
    
        for i in range(it):
            xi = x00 - g(x00)/df(g,x00,tol)
            erro = abs(xi - x00)
            x00 = xi
            if erro<tol:
                break
        return xi
    
    tf = t0 + nsteps*dt
    xs = []
    t = np.linspace(t0,tf,nsteps+1)
    for i in t:
        gh = lambda x: x0 + dt*f(i,x) - x #função para obter no caso implícito
        yn_1 = NewtonRaphson(gh,x0)
        xs.append(yn_1)
        x0 = yn_1
    df = pd.DataFrame([t,xs]).T
    df.columns = ['t','y']
    return df

def adam(f, t0, x0, dt, nsteps): #metodo de 6a ordem e implícito
    def NewtonRaphson(g,x00,tol=1e-7,it=500):
        def df(g,x00,tol=1e-7):
            return (g(x00+0.01*tol) - g(x00))/(0.01*tol)
    
        for i in range(it):
            xi = x00 - g(x00)/df(g,x00,tol)
            erro = abs(xi - x00)
            x00 = xi
            if erro<tol:
                break
        return xi
    
    tf = t0 + nsteps*dt
    xs = []
    t = np.linspace(t0,tf,nsteps+1)
    for j,i in enumerate(t):
        if j<=4:
            gh = lambda x: x0 + dt*f(i,x) - x #função para obter no caso implícito
            yn_1 = NewtonRaphson(gh,x0)
            xs.append(yn_1)
            x0 = yn_1
        else:
            fy0 = xs[j-4]
            fy1 = xs[j-3]
            fy2 = xs[j-2]
            fy3 = xs[j-1]
            gh = lambda x: x0 + dt*(475*f(i,x) + 1427*f(i,x0) - 798*f(i,fy3) + 482*f(i,fy2) - 173*f(i,fy1) + 27*f(i,fy0))/1440 - x #função para obter a raiz no caso implícito
            yn_1 = NewtonRaphson(gh,x0)
            xs.append(yn_1)
            x0 = yn_1
    df = pd.DataFrame([t,xs]).T
    df.columns = ['t','y']
    return df

def eulerapr(f, t0, x0, dt, nsteps):
    def NewtonRaphson(g,x00,tol=1e-7,it=500):
        def df(g,x00,tol=1e-7):
            return (g(x00+0.01*tol) - g(x00))/(0.01*tol)
    
        for i in range(it):
            xi = x00 - g(x00)/df(g,x00,tol)
            erro = abs(xi - x00)
            x00 = xi
            if erro<tol:
                break
        return xi
    
    tf = t0 + nsteps*dt
    xs = []
    t = np.linspace(t0,tf,nsteps+1)
    for i in t:
        gh = lambda x: x0 + 0.5*dt*(f(i,x)+f(i,x0)) - x #função para obter no caso implícito
        yn_1 = NewtonRaphson(gh,x0)
        xs.append(yn_1)
        x0 = yn_1

    df = pd.DataFrame([t,xs]).T
    df.columns = ['t','y']
    return df

def implicitorunge(f, t0, x0, dt, nsteps): #runge kutta implicito de 3 ordem
    def NewtonRaphson(g,x00,tol=1e-7,it=500):
        def df(g,x00,tol=1e-7):
            return (g(x00+0.01*tol) - g(x00))/(0.01*tol)
    
        for i in range(it):
            xi = x00 - g(x00)/df(g,x00,tol)
            erro = abs(xi - x00)
            x00 = xi
            if erro<tol:
                break
        return xi
    
    tf = t0 + nsteps*dt
    xs = []
    t = np.linspace(t0,tf,nsteps+1)
    for i in t:
        gh = lambda x: x0 + 0.25*dt*(f(i,x0) +3*f(i+2*dt/3,x0 + 2*(x - x0)/3)) - x                                  #função para obter no caso implícito
        yn_1 = NewtonRaphson(gh,x0)
        xs.append(yn_1)
        x0 = yn_1
    df = pd.DataFrame([t,xs]).T
    df.columns = ['t','y']
    return df

#-------------------------------------------------EQUAÇÕES DIFERENCIAIS DE SEGUNDA ORDEM--------------------------------------------------------------------------------------------------

def euler2(dxdt ,dydt ,t0 ,x0, y0, dt, nsteps):
    tf = t0 + nsteps*dt
    t = np.linspace(t0,tf,nsteps+1)
    a = []
    b = []
    for i in t:
        #x = x0 + dt*w0#(f(t[j]+0.000001,x0)-f(t[j],x0))/0.000001
        x = x0 + dt*dxdt(i,x0,y0)
        y = y0 + dt*dydt(i,x0,y0)
        x0 = x
        a.append(x0)
        y0 = y
        b.append(y0)
    df = pd.DataFrame([t,b]).T
    df.columns = ['t','y']
    return df

def runge2(dxdt ,dydt ,t0 ,x0, y0, dt, nsteps):
    tf = t0 + nsteps*dt
    t = np.linspace(t0,tf,nsteps+1)
    a = []
    b = []
    for i in t:
        k1x = dt*dxdt(i,x0,y0)
        k2x = dt*dxdt(i+dt/2,x0+k1x/2,y0)
        k3x = dt*dxdt(i+dt/2,x0+k2x/2,y0)
        k4x = dt*dxdt(i+dt,x0+k3x,y0)
        x = x0 + (k1x/6 + k2x/3 + k3x/3 + k4x/6)
        k1y = dt*dydt(i,x0,y0)
        k2y = dt*dydt(i+dt/2,x0,y0+k1y/2)
        k3y = dt*dydt(i+dt/2,x0,y0+k2y/2)
        k4y = dt*dydt(i+dt,x0,y0+k3y)
        y = y0 + (k1y/6 + k2y/3 + k3y/3 + k4y/6)
        x0 = x
        a.append(x0)
        y0 = y
        b.append(y0)
    df = pd.DataFrame([t,b]).T
    df.columns = ['t','y']
    return df

def implicitoeuler2(dxdt ,dydt ,t0, x0, y0, dt, nsteps):
    def NewtonRaphson(g,x00,tol=1e-7,it=500):
        def df(g,x00,tol=1e-7):
            return (g(x00+0.01*tol) - g(x00))/(0.01*tol)
    
        for i in range(it):
            xi = x00 - g(x00)/df(g,x00,tol)
            erro = abs(xi - x00)
            x00 = xi
            if erro<tol:
                break
        return xi
    
    tf = t0 + nsteps*dt
    xs = []
    ys = []
    t = np.linspace(t0,tf,nsteps+1)
    for i in t:
        ghx = lambda x: x0 + dt*dxdt(i,x,y0) - x #função para obter no caso implícito
        ghy = lambda y: y0 + dt*dydt(i,x0,y) - y #função para obter no caso implícito
        yn_1 = NewtonRaphson(ghx,x0)
        yn_2 = NewtonRaphson(ghy,y0)
        xs.append(yn_1)
        ys.append(yn_2)
        x0 = yn_1
        y0 = yn_2
    df = pd.DataFrame([t,ys]).T
    df.columns = ['t','y']
    return df

def eulerapr2(dxdt ,dydt ,t0, x0, y0, dt, nsteps):
    def NewtonRaphson(g,x00,tol=1e-7,it=500):
        def df(g,x00,tol=1e-7):
            return (g(x00+0.01*tol) - g(x00))/(0.01*tol)
    
        for i in range(it):
            xi = x00 - g(x00)/df(g,x00,tol)
            erro = abs(xi - x00)
            x00 = xi
            if erro<tol:
                break
        return xi
    
    tf = t0 + nsteps*dt
    xs = []
    ys = []
    t = np.linspace(t0,tf,nsteps+1)
    for i in t:
        ghx = lambda x: x0 + 0.5*dt*(dxdt(i,x,y0) + dxdt(i,x0,y0)) - x #função para obter no caso implícito
        ghy = lambda y: y0 + 0.5*dt*(dydt(i,x0,y) + dydt(i,x0,y0)) - y #função para obter no caso implícito
        yn_1 = NewtonRaphson(ghx,x0)
        yn_2 = NewtonRaphson(ghy,y0)
        xs.append(yn_1)
        ys.append(yn_2)
        x0 = yn_1
        y0 = yn_2
    df = pd.DataFrame([t,ys]).T
    df.columns = ['t','y']
    return df

def adam2(dxdt ,dydt ,t0, x0, y0, dt, nsteps): #metodo de 6a ordem e implícito
    def NewtonRaphson(g,x00,tol=1e-7,it=500):
        def df(g,x00,tol=1e-7):
            return (g(x00+0.01*tol) - g(x00))/(0.01*tol)
    
        for i in range(it):
            xi = x00 - g(x00)/df(g,x00,tol)
            erro = abs(xi - x00)
            x00 = xi
            if erro<tol:
                break
        return xi
    
    tf = t0 + nsteps*dt
    xs = []
    ys = []
    t = np.linspace(t0,tf,nsteps+1)
    for j,i in enumerate(t):
        if j<=4:
            ghx = lambda x: x0 + dt*dxdt(i,x,y0) - x #função para obter no caso implícito
            ghy = lambda y: y0 + dt*dydt(i,x0,y) - y #função para obter no caso implícito
            yn_1 = NewtonRaphson(ghx,x0)
            yn_2 = NewtonRaphson(ghy,y0)
            xs.append(yn_1)
            ys.append(yn_2)
            x0 = yn_1
            y0 = yn_2
        else:
            fx0 = xs[j-4]
            fx1 = xs[j-3]
            fx2 = xs[j-2]
            fx3 = xs[j-1]
            fy0 = ys[j-4]
            fy1 = ys[j-3]
            fy2 = ys[j-2]
            fy3 = ys[j-1]
            ghx = lambda x: x0 + dt*(475*dxdt(i,x,y0) + 1427*dxdt(i,x0,y0) - 798*dxdt(i,fx3,y0) + 482*dxdt(i,fx2,y0) - 173*dxdt(i,fx1,y0) + 27*dxdt(i,fx0,y0))/1440 - x #função para obter a raiz no caso implícito
            ghy = lambda y: y0 + dt*(475*dydt(i,x0,y) + 1427*dydt(i,x0,y0) - 798*dydt(i,x0,fy3) + 482*dydt(i,x0,fy2) - 173*dydt(i,x0,fy1) + 27*dydt(i,x0,fy0))/1440 - y
            yn_1 = NewtonRaphson(ghx,x0)
            yn_2 = NewtonRaphson(ghy,y0)
            xs.append(yn_1)
            ys.append(yn_2)
            x0 = yn_1
            y0 = yn_2
    df = pd.DataFrame([t,ys]).T
    df.columns = ['t','y']
    return df
