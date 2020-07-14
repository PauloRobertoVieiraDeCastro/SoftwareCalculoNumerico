import numpy as np
import math
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit

def reglinear(x,y):
    def soma(x):
        s = 0
        cont = 0
        for i in x:
            s+=i
            cont+=1
        return s,cont

    def media(x):
        return soma(x)[0]/soma(x)[1]

    b = soma([i*(j - media(y)) for (i,j) in zip(x,y)])[0]/soma([i*(i - media(x)) for i in x])[0]
    a = media(y) - b*media(x)
    R2 = 1 - soma([(j - (b*i + a))**2 for (i,j) in zip(x,y)])[0]/soma([(i - media(y))**2 for i in y])[0]
    return b,a,R2

def regexp(td,z0):
    s1 = np.sum(td*np.log(z0))
    s2 = (np.sum(np.log(z0)))*(np.sum(td))/len(td)
    s3 = np.sum(np.dot(td,td))
    s4 = ((np.sum(td))**2)/len(td)
    A = (s1 - s2)/(s3 - s4)
    s5 = np.sum(np.log(z0))/len(td)
    s6 = np.sum(td)/len(td)
    B = math.exp(s5 - A*s6)

    r1 = len(td)*np.sum(td*np.log(z0))
    r2 = (np.sum(td)*np.sum(np.log(z0)))
    r3 = ((len(td))*(np.sum(np.dot(td,td)))) - (np.sum(td))**2
    r4 = ((len(td))*(np.sum(np.dot(np.log(z0),np.log(z0))))) - (np.sum(np.log(z0)))**2

    R2 = ((r1 - r2)**2)/(r3*r4)
    return A,B,R2

def regpol(x,y,n):
    poly = PolynomialFeatures(degree = n)
    X = np.array(x).reshape(-1,1)
    Y = np.array(y)
    X_poly = poly.fit_transform(X) 
  
    poly.fit(X_poly, y) 
    lin2 = LinearRegression() 
    lin2.fit(X_poly, y)
    b = lin2.coef_
    a = lin2.intercept_
    R2 = r2_score(lin2.predict(poly.fit_transform(X)),y)
    return b,a,R2,lin2.predict(poly.fit_transform(X))

def reglog(X,y):
    def sigmoid(X, Beta_1, Beta_2):
        y = 1 / (1 + np.exp(-Beta_1*(X-Beta_2)))
        return y
    X1 = np.array(X)/max(np.array(X))
    y1 = np.array(y)/max(np.array(y))
    popt, pcov = curve_fit(sigmoid, X1, y1)
    y_pred = sigmoid(X1,popt[0],popt[1])
    R2 = r2_score(y_pred,y1)
    return popt[0], popt[1], R2, y_pred

def regLN(x,y):
    def logar(x,a,b):
        y = a*np.log(x) + b
        return y
    x1 = np.array(x)
    y1 = np.array(y)
    popt1, pcov1 = curve_fit(logar, x1, y1)
    y_pred = logar(x1,popt1[0],popt1[1])
    R2 = r2_score(y_pred,y1)
    return popt1[0], popt1[1], R2, y_pred
