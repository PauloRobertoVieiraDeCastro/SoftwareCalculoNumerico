import pandas as pd
import numpy as np

def error(it,x0,x1,f):
    if it == 0:
        erro = abs(f(x1))
    if it == 1:
        erro = abs(x0 - x1)
    return erro

def bisseccao(f,x0,x1,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    if (f(x0)>0 and f(x1)>0) or (f(x0)<0 and f(x1)<0):
        return "Chutes incorretos"
    else:
    
        for i in range(it):
            b = ((x0 + x1)/2.0)
            res.append(b)
            if (f(b)>0 and f(x0)>0) or (f(b)<0 and f(x0)<0):
                erro = error(j,b,x0,f)#abs(b - x0)
                x0 = b
            else:
                erro = error(j,b,x0,f)#abs(b - x1)
                x1 = b
            er.append(erro)
            yexp.append(f(b))
            if erro<tol:
                break
        df = pd.DataFrame([res,er,yexp]).T
        df.columns = ['Valor de x','Erro','y']
        return b,i,erro,df

def regula_falsi(f,x0,x1,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    if (f(x0)>0 and f(x1)>0) or (f(x0)<0 and f(x1)<0):
        return "Chutes incorretos"
    else:
    
        for i in range(it):
            b = (x0*f(x1) - x1*f(x0))/(f(x1) - f(x0))
            res.append(b)
            if (f(b)>0 and f(x0)>0) or (f(b)<0 and f(x0)<0):
                erro = error(j,b,x0,f)#abs(b - x0)
                x0 = b
            else:
                erro = error(j,b,x0,f)#abs(b - x1)
                x1 = b
            yexp.append(f(b))
            er.append(erro)
            if erro<tol:
                break
        df = pd.DataFrame([res,er,yexp]).T
        df.columns = ['Valor de x','Erro','y']
        return b,i,erro,df

def NewtonRaphson(f,x0,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    def df(f,x0,tol):
        return (f(x0+0.01*tol) - f(x0))/(0.01*tol)
    
    for i in range(it):
        x = x0 - f(x0)/df(f,x0,tol)
        res.append(x)
        erro = error(j,x,x0,f)#abs(x - x0)
        er.append(erro)
        yexp.append(f(x))
        x0 = x
        if erro<tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x,i,erro,df

def secante(f,x0,x1,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    for i in range(it):
        m = (f(x1) - f(x0))/(x1 - x0)
        x2 = x1 - f(x1)/m
        res.append(x2)
        erro = error(j,x1,x2,f)#abs(x2 - x1)
        er.append(erro)
        yexp.append(f(x2))
        x0 = x1
        x1 = x2
        if erro<tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x1,i,erro,df
   

def halley(f,x0,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    def df(f,x0,tol):
        return (f(x0+0.01*tol) - f(x0))/(0.01*tol)
    def df2(f,x0,tol):
        return (f(x0+0.01*tol) - 2*f(x0) + f(x0-0.01*tol))/(0.01*tol)**2
    
    for i in range(it):
        x = x0 - 2*f(x0)*df(f,x0,tol)/(2*(df(f,x0,tol)**2) - f(x0)*df2(f,x0,tol))
        res.append(x)
        erro = error(j,x,x0,f)#abs(x - x0)
        er.append(erro)
        yexp.append(f(x))
        x0 = x
        if erro<tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x,i,erro,df

def TSM(f,x0,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    def df(f,x0,tol):
        return (f(x0+0.01*tol) - f(x0))/(0.01*tol)
    
    for i in range(it):
        yn = x0 - f(x0)/df(f,x0,tol)
        x = yn - f(yn)/(df(f,yn,tol))
        res.append(x)
        erro = error(j,x,x0,f)#abs(x - x0)
        er.append(erro)
        yexp.append(f(x))
        x0 = x
        if erro<tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x,i,erro,df

def FLM(f,x0,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    def df(f,x0,tol):
        return (f(x0+0.01*tol) - f(x0))/(0.01*tol)
    
    for i in range(it):
        yn = x0 - f(x0)/df(f,x0,tol)
        x = yn - ((5*df(f,x0,tol)**2 + 3*df(f,yn,tol))/(df(f,x0,tol)**2 + 7*df(f,yn,tol)**2))*(f(yn)/df(f,x0,tol))
        res.append(x)
        erro = error(j,x,x0,f)#abs(x - x0)
        er.append(erro)
        yexp.append(f(x))
        x0 = x
        if erro<tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x,i,erro,df

def Steffensen(f,x0,j,tol=1e-6,it=40000):
    res = []
    er = []
    yexp = []
    for i in range(it):
        try:
            x = x0 - (f(x0)**2)/(f(x0 + f(x0)) - f(x0))
            res.append(x)
            erro = error(j,x,x0,f)
            er.append(erro)
            yexp.append(f(x))
            x0 = x
            if erro<tol:
                break
        except ZeroDivisionError:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x,i,erro,df

def pegaso(f,x0,x1,j,tol=1e-6,it=40000):
    res = []
    er = []
    yexp = []
    for i in range(it):
        b = x1 - (f(x1)/(f(x1) - f(x0)))*(x1 - x0)
        res.append(b)
        if (f(b)>0 and f(x0)>0) or (f(b)<0 and f(x0)<0):
            erro = error(j,b,x0,f)
            x0 = b
        else:
            erro = error(j,b,x0,f)
            x1 = b
        yexp.append(f(b))
        er.append(erro)
        if erro<=tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return b,i,erro,df

def Schroder(f,x0,j,tol=1e-6,it=400):
    res = []
    er = []
    yexp = []
    def df(f,x0,tol):
        return (f(x0+0.01*tol) - f(x0))/(0.01*tol)
    def df2(f,x0,tol):
        return (f(x0+0.01*tol) - 2*f(x0) + f(x0-0.01*tol))/(0.01*tol)**2
    
    for i in range(it):
        x = x0 - (f(x0)*df(f,x0,tol))/((df(f,x0,tol)**2) - f(x0)*df2(f,x0,tol))
        res.append(x)
        erro = error(j,x,x0,f)#abs(x - x0)
        er.append(erro)
        yexp.append(f(x))
        x0 = x
        if erro<tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x,i,erro,df
    
def Raltz(f,x0,x1,j,tol=1e-6,it=400):
    def df(f,x0,tol):
        return (f(x0+0.01*tol) - f(x0))/(0.01*tol)
    res = []
    er = []
    yexp = []
    for i in range(it):
        u0 = f(x0)/df(f,x0,tol)
        u1 = f(x1)/df(f,x1,tol)
        x2 = x1 - u1*(x0 - x1)/(u0 - u1)
        res.append(x2)
        erro = error(j,x1,x2,f)#abs(x2 - x1)
        er.append(erro)
        yexp.append(f(x2))
        x0 = x1
        x1 = x2
        if erro<tol:
            break
    df = pd.DataFrame([res,er,yexp]).T
    df.columns = ['Valor de x','Erro','y']
    return x1,i,erro,df
