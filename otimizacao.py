import pandas as pd
import numpy as np

def error(it,x0,x1,f):
    if it == 0:
        erro = abs(f(x1) - f(x0))
    if it == 1:
        erro = abs(x0 - x1)
    return erro

def NewtonRaphson2(f,x0,j,tol=1e-6,max_iter=40000):
    res = []
    er = []
    yexp = []
    h = tol/100.0
    def df(f,x,h):
        y = (f(x+h)-f(x))/h
        return y

    def df2(f,x,h):
        yy = (f(x+h) - 2*f(x) + f(x-h))/h**2
        return yy

    
    for i in range(max_iter):
        x = x0 - df(f,x0,h)/df2(f,x0,h)
        res.append(x)
        erro = error(1,x,x0,f)#abs(x - x0)
        er.append(erro)
        yexp.append(f(x))
        if erro<tol:
            break
        x0 = x
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['x','Erro','y']
    return x,f(x),erro,df


def gradiente_descendente(f,x0,j,tol):
    def derivada(f,x):
        h = 0.0001
        dff = (f(x+h) - f(x-h))/(2*h)
        return dff
    # função unidimensional
    alfa = 0.01 #taxa de aprendizagem
    max_iter = 50000 #máximo número de iterações
    res = []
    er = []
    yexp = []
    for i in range(max_iter):
        try:
            x = x0 - alfa*derivada(f,x0)
            res.append(x)
        except ZeroDivisionError:
            return "Divisão por zero"
        erro = error(j,x,x0,f)#abs(x - x0)
        er.append(erro)
        yexp.append(f(x))
        if erro<tol:
            break
        x0 = x
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['x','Erro','y']
    return x,f(x),erro,df

def montecarlo(ff,x0,x1,p,j,tol=1e-6):
    res = []
    er = []
    yexp = []
    if p == 'Mínimo':
        minf = 1e9
        mx = 0
        for i in range(500000):
            x = x0 + (x1 - x0)*np.random.rand(1)[0]
            fv = ff(x)
            if fv<minf:
                erro = error(1,x,x0,fv)
                er.append(erro)
                minf =fv
                yexp.append(minf)
                mx = x
                res.append(mx)
                if erro<tol:
                    break
        df = pd.DataFrame([res,er,yexp]).T
        df.columns = ['x','Erro','y']
        return float(mx),float(minf),float(erro),df
    
    if p == 'Máximo':
        maxf = -1e9
        mx = 0
        for i in range(500000):
            x = x0 + (x1 - x0)*np.random.rand(1)[0]
            fv = ff(x)
            if fv>maxf:
                erro = error(1,x,x0,fv)
                er.append(erro)
                maxf =fv
                yexp.append(maxf)
                mx = x
                res.append(mx)
                if erro<tol:
                    break
        df = pd.DataFrame([res,er,yexp]).T
        df.columns = ['x','Erro','y']
        return float(mx),float(maxf),float(erro),df

