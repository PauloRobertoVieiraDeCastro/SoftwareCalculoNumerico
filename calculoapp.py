from math import*
import numpy as np
import pandas as pd
from scipy.integrate import quad,dblquad,nquad
import datetime
from tkinter import*
from tkinter import ttk
from tkinter import tix
import xlrd
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from tkinter.filedialog import askopenfilename
import tkinter.ttk as ttk
from scipy import stats
from sympy import*
import raizes as roots
import integracao as integ
import eqdiff as eqd
import otimizacao as optim
import regressaolinear as reglin


class aplicacao():
    def __init__(self):
                
        #----------------------------------------------
        self.contaqtd = 0 #contagem de posição para gerar quadro de inserção de dados
        
        self.i = 0
        #----------Características básicas do objeto----------
        self.main = Tk()
        self.main['bg'] = 'seashell2'
        self.main.title("Metodologias de cálculo numérico",)
        self.main.geometry('500x400')
        self.main.resizable(False,False) #impeço ampliar a janela
        #self.menubar = Menu(self.root) #criando barra de menu
        Label(self.main,text="Seleção de metodologias",bg='seashell2',font = ("Arial",24,"bold")).place(x=50,y=10)
        

        Button(self.main,command = self.raizes,text = "Cálculo de raízes",width=17).place(x=60,y=120)
        Button(self.main,command = self.integral,text = "Cálculo de integrais",width=17).place(x=60,y=170)
        Button(self.main,command = self.edos,text = "Cálculo de EDO´s",width=17).place(x=60,y=220)
        Button(self.main,command = self.otimizacao,text = "Otimização",width=17).place(x=260,y=120)
        Button(self.main,command = self.estat,text = "Regressão",width=17).place(x=260,y=170)
        
    #-----------------------------------------------Cálculo de Raízes-----------------------------------------------------------------------------------------

    def raizes(self):
        #----------Características básicas do objeto----------
        self.root = Toplevel()#tix.Tk()
        self.root['bg'] = 'seashell2'
        self.root.title("Aplicação didática em cálculo numérico")
        self.root.geometry('800x600')
        self.frames_tela()
        self.lista()

        #---------------variáveis-------------------------------------------------------------------------------------------------------------------------------
        self.qtd = StringVar()
        self.x0 = StringVar()
        self.x1 = StringVar()
        self.rr = StringVar()
        self.it = IntVar()
        self.prec = StringVar()

        #-------------------------Spinbox---------------------------------------------------------------------------------------------------------------------
        self.met1 = ["Newton-Raphson","Bissecção","Regula-Falsi","Secante","Halley","Two-Step Method","FLM","Steffensen","Pégaso","Schroder","Raltz"]
        Label(self.frame_3,text = "Metodologia",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.1,rely=0.03)
        self.it_r = Spinbox(self.frame_3,values=self.met1,justify = "center",textvariable=self.rr,
                            command = self.event).place(relx = 0.1,rely = 0.15,relwidth= 0.58)
        
        #---------------------------Radiobutton----------------------------------------------------------------------------------------------------------------
        Label(self.frame_3,text = "Critério de parada",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.1,rely=0.33)
        self.rr1 = Radiobutton(self.frame_3, text="|f(x)| < Precisão",bg='#dfe3ee',font = ("Arial",9,"bold"),value=0,
                               variable = self.it).place(relx=0.1,rely=0.43)
        self.rr2 = Radiobutton(self.frame_3, text="|xn - xn-1| < Precisão",bg='#dfe3ee',font = ("Arial",9,"bold"),value=1,
                               variable = self.it).place(relx=0.1,rely=0.55)
        
        #--------------Entrada---------------------------------------------------------------------------------------------------------------------------------
        self.L1 = Label(self.frame_1,text='Insira sua função f(x)',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.03)
        self.e1 = Entry(self.frame_1,justify='center',font = ("Arial",11),width=35,textvariable=self.qtd).place(relx= 0.05, rely= 0.1, relwidth= 0.35)#função
        
        self.L1 = Label(self.frame_1,text='Insira a precisão',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.23)
        self.e3 = Entry(self.frame_1,justify='center',font = ("Arial",11),width=25,textvariable=self.prec).place(relx= 0.05, rely= 0.3, relwidth= 0.14)#função
        
        self.L1 = Label(self.frame_1,text='Insira seu chute inicial',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.43)
        self.e2 = Entry(self.frame_1,justify='center',font = ("Arial",11),width=25,textvariable=self.x0).place(relx= 0.05, rely= 0.5, relwidth= 0.14)#chute inicial

        #-------------------------Botões------------------------------------------------------------------------------------------------------------------------
        self.b1 = Button(self.frame_1, text = 'Calcular', width = 20, font = ('Verdana',10,'bold'),bg = '#107db2',fg = 'white',
               command = self.extract).place(relx= 0.05, rely= 0.85, relwidth= 0.20)
        self.b2 = Button(self.frame_1, text = 'Exportar resultados', width = 20, font = ('Verdana',10,'bold'),bg = '#107db2',fg = 'white',
               command = self.export).place(relx= 0.30, rely= 0.85, relwidth= 0.20)
        #----------------------------Explanação das entradas-------------------------------------------------------------------------------------------------
        #self.balao_buscar = tix.Balloon(self.frame_1)
        #text = "Exporta os valores de x por iteração e a evolução do erro"
        #self.balao_buscar.bind_widget(self.b2,balloonmsg="Some random text")
        
        self.root.resizable(False,False) #impeço ampliar a janela
        self.root.mainloop()

    #-------------------------------------Tabela para resultados por iteração------------------------------------------------------------------------------------------
    def lista(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,
                                     column=("Iteração","x", "f(x)", "Erro"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="x")
        self.listaCli.heading("#2", text="f(x)")
        self.listaCli.heading("#3", text="Erro")
        self.listaCli.heading("#4", text="Iteração")
        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=30)
        self.listaCli.column("#2", width=30)
        self.listaCli.column("#3", width=30)
        self.listaCli.column("#4", width=30)
        self.listaCli.place(relx=0.45, rely=0.05, relwidth=0.5, relheight=0.9)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical',command=self.listaCli.yview)
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.95, rely=0.05, relwidth=0.02, relheight=0.9)

    #---------------------------Extração da função-----------------------------------------------------------------------------------------------------------------
    def extract(self):
        x = symbols('x') #entrada de função símbolica
        cb = self.it.get() #para mudar o critério de parada
        
        try:
            expr = self.qtd.get().lower() #obtendo a função simbólica
            x01 = float(self.x0.get()) #obtendo o primeiro chute inicial
            preci = float(self.prec.get()) #obtendo a precisão desejada
            f = lambdify(x,expr,modules=['math']) #converti em função
        except ValueError:
            messagebox.showinfo('Cálculo de raízes','Erro - Nem todos os campos foram preenchidos')
        
        self.it_r2 = self.rr.get() #seleção do método

        if self.it_r2 == "Newton-Raphson":
            self.resultado = roots.NewtonRaphson(f,x01,cb,preci)
        if self.it_r2 == "Secante":
            try:
                x02 = float(self.x02.get())
                self.resultado = roots.secante(f,x01,x02,cb,preci)
            except ValueError:
                messagebox.showinfo('Cálculo de raízes','Erro - Nem todos os campos foram preenchidos')
        if self.it_r2 == "Bissecção":
            try:
                x02 = float(self.x02.get())
                self.resultado = roots.bisseccao(f,x01,x02,cb,preci)
            except ValueError:
                messagebox.showinfo('Cálculo de raízes','Erro - Nem todos os campos foram preenchidos')
        if self.it_r2 == "Regula-Falsi":
            try:
                x02 = float(self.x02.get())
                self.resultado = roots.regula_falsi(f,x01,x02,cb,preci)
            except ValueError:
                messagebox.showinfo('Cálculo de raízes','Erro - Nem todos os campos foram preenchidos')
        if self.it_r2 == "Pégaso":
            try:
                x02 = float(self.x02.get())
                self.resultado = roots.pegaso(f,x01,x02,cb,preci)
            except ValueError:
                messagebox.showinfo('Cálculo de raízes','Erro - Nem todos os campos foram preenchidos')
        if self.it_r2 == "Raltz":
            try:
                x02 = float(self.x02.get())
                self.resultado = roots.Raltz(f,x01,x02,cb,preci)
            except ValueError:
                messagebox.showinfo('Cálculo de raízes','Erro - Nem todos os campos foram preenchidos')
        if self.it_r2 == "Halley":
            self.resultado = roots.halley(f,x01,cb,preci)
        if self.it_r2 == "Two-Step Method":
            self.resultado = roots.TSM(f,x01,cb,preci)
        if self.it_r2 == "FLM":
            self.resultado = roots.FLM(f,x01,cb,preci)
        if self.it_r2 == "Steffensen":
            self.resultado = roots.Steffensen(f,x01,cb,preci)
        if self.it_r2 == "Schroder":
            self.resultado = roots.Schroder(f,x01,cb,preci)
            
        self.r1 = Label(self.frame_2,text="Resultado da raiz da função",bg='#dfe3ee',
                           font = ("Arial",10,'bold')).place(relx= 0.05, rely= 0.05, relwidth= 0.30)
        self.r2 = Label(self.frame_2,text="Número de iterações necessárias",bg='#dfe3ee',
                           font = ("Arial",10,'bold')).place(relx= 0.05, rely= 0.25, relwidth= 0.30)

        if type(self.resultado[0])==float or type(self.resultado[0])==int:
            self.resul1 = Label(self.frame_2,text="{:.4f}".format(self.resultado[0]),bg='#dfe3ee',
                           font = ("Arial",10,'bold')).place(relx= 0.05, rely= 0.15, relwidth= 0.30)
            self.resu2 = Label(self.frame_2,text="{:.0f}".format(self.resultado[1]),bg='#dfe3ee',
                           font = ("Arial",10,'bold')).place(relx= 0.05, rely= 0.35, relwidth= 0.30)
            df = self.resultado[3] #resultado de cada iteração
            self.listaCli.delete(*self.listaCli.get_children()) #apago os dados anteriores
            self.X = df['Valor de x'].values #valores de x
            self.E = df['Erro'].values #valores de erro
            self.Y = df['y'].values #valores de y
            cont = list(range(len(self.X))) #iterações
            for i,j,k,o in zip(self.X,self.E,cont,self.Y):
                self.listaCli.insert("","end",values = ("{:.5f}".format(i),"{:.5f}".format(o),"{:.5f}".format(j),k))
    
        else:
            self.resul1 = Label(self.frame_2,text=(self.resultado),bg='#dfe3ee',
                           font = ("Arial",10,'bold')).place(relx= 0.05, rely= 0.15, relwidth= 0.30)
            self.resu2 = Label(self.frame_2,text="Impossível calcular",bg='#dfe3ee',
                           font = ("Arial",10,'bold')).place(relx= 0.05, rely= 0.35, relwidth= 0.30)
    #-------------------------------Exportando para excel---------------------------------------------------------------------------------------------------   
    def export(self):
        try:
            if type(self.resultado[0])==float or type(self.resultado[0])==int:
                self.resultado[3].to_excel('Resultado.xlsx')
                messagebox.showinfo('Cálculo de raízes','Resultado exportado com sucesso')
            else:
                messagebox.showinfo('Cálculo de raízes','Erro - Impossível exportar')
        except AttributeError:
            messagebox.showinfo('Cálculo de raízes','Erro - Impossível exportar. Nenhum cálculo foi realizado.')
    #--------------------------------------Evento de mudança por método --------------------------------------------------------------------------------------
    def event(self):
        self.it_r2 = self.rr.get()
        self.x02 = StringVar()
        if self.it_r2 == "Bissecção" or self.it_r2 == "Regula-Falsi" or self.it_r2 == "Secante" or self.it_r2 == "Pégaso" or self.it_r2 == "Raltz":
            Label(self.frame_1,text='Insira seu segundo chute inicial',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.63)
            self.e3 = Entry(self.frame_1,justify='center',font = ("Arial",11),width=25,textvariable=self.x02).place(relx= 0.05, rely= 0.7, relwidth= 0.14)#chute inicial
        else:
            Label(self.frame_1,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.63, relwidth = 0.5)
            Label(self.frame_1,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.7, relwidth = 0.5)
            




    #----------------------------------------------------------Cálculo de integrais ---------------------------------------------------------------------------------------
            
    def integral(self):
        #----------Características básicas do objeto----------
        self.root2 = Toplevel()#tix.Tk()
        self.root2['bg'] = 'seashell2'
        self.root2.title("Aplicação didática em cálculo numérico")
        self.root2.geometry('600x600')
        self.frame2()
        #self.lista()

        #---------------variáveis-------------------------------------------------------------------------------------------------------------------------------
        self.func = StringVar() #funcao
        self.a0 = StringVar() #valor menor EM X
        self.a1 = StringVar() #valor maior EM X
        self.a2 = StringVar() #VALOR MENOR E Y
        self.a3 = StringVar() #valor maior em Y
        self.a4 = StringVar() #VALOR MENOR E z
        self.a5 = StringVar() #valor maior em z
        self.interv = StringVar() #intervalo
        self.zz2 = StringVar() #evento método
        self.zz3 = StringVar() #evento para integral dupla
        self.zz4 = StringVar() #evento para integral tripla
        
        self.it2 = StringVar()
        

        #-------------------------Spinbox---------------------------------------------------------------------------------------------------------------------
        self.met2 = ["Quadratura","Trapézios","Simpson 1/3","Simpson 3/8","Boole"]
        Label(self.frame_6,text = "Metodologia",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.1,rely=0.03)
        Spinbox(self.frame_6,values=self.met2,justify = "center",textvariable=self.zz2,command=self.event2).place(relx = 0.1,rely = 0.17,relwidth= 0.58)
        
        Label(self.frame_6,text = "Tipo de integral",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.1,rely=0.38)
        self.met3 = ["Simples","Dupla","Tripla"]
        Spinbox(self.frame_6,values=self.met3,justify = "center",textvariable=self.zz3,command = self.event3).place(relx = 0.1,rely = 0.52,relwidth= 0.58)
        
        #--------------Entrada---------------------------------------------------------------------------------------------------------------------------------
        Label(self.frame_4,text='Insira sua função f(x)',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.03)
        Entry(self.frame_4,justify='center',font = ("Arial",10),width=35,textvariable=self.func).place(relx= 0.05, rely= 0.1, relwidth= 0.35)#função
        
        Label(self.frame_4,text='X inicial',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.23)
        Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a0).place(relx= 0.05, rely= 0.3, relwidth= 0.08)#primeiro valor
        
        Label(self.frame_4,text='X final',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.43)
        Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a1).place(relx= 0.05, rely= 0.5, relwidth= 0.08)#segundo valor

        #-------------------------Botões------------------------------------------------------------------------------------------------------------------------
        self.b1 = Button(self.frame_4, text = 'Calcular', width = 20, font = ('Verdana',10,'bold'),bg = '#107db2',fg = 'white',
                         command = self.integr).place(relx= 0.05, rely= 0.85, relwidth= 0.20)
        
        self.root2.resizable(False,False) #impeço ampliar a janela
        self.root2.mainloop()
    

    #-----------------------------------------------Cálculo de integrais numérico----------------------------------------------------------------------------------------

    def integr(self):
        
        try:
            self.kz2 = self.zz3.get()
            if self.kz2 == "Simples":
                x = symbols('x') #entrada de função símbolica
                expr = self.func.get().lower() #obtendo a função simbólica
                a00 = float(self.a0.get()) #obtendo o primeiro chute inicial
                a01 = float(self.a1.get()) #obtendo a precisão desejada
                f = lambdify(x,expr,modules=['math']) #converti em função
            if self.kz2 == "Dupla":
                x,y = symbols('x y')
                expr = self.func.get().lower() #obtendo a função simbólica
                a00 = float(self.a0.get()) #obtendo o primeiro chute inicial
                a01 = float(self.a1.get()) #obtendo a precisão desejada
                a02 = float(self.a2.get()) #obtendo o primeiro chute inicial
                a03 = float(self.a3.get()) #obtendo a precisão desejada
                f = lambdify([x,y],expr,modules=['math']) #converti em função
            if self.kz2 == "Tripla":
                x,y,z = symbols('x y z')
                expr = self.func.get().lower() #obtendo a função simbólica
                a00 = float(self.a0.get()) #obtendo o primeiro chute inicial
                a01 = float(self.a1.get()) #obtendo a precisão desejada
                a02 = float(self.a2.get()) #obtendo o primeiro chute inicial
                a03 = float(self.a3.get()) #obtendo a precisão desejada
                a04 = float(self.a4.get()) #obtendo o primeiro chute inicial
                a05 = float(self.a5.get()) #obtendo a precisão desejada
                f = lambdify([x,y,z],expr,modules=['math']) #converti em função
        except ValueError:
            messagebox.showinfo('Cálculo de integrais','Erro - Nem todos os campos foram preenchidos')
        
        self.met1 = self.zz2.get() #seleção do método
        
        if self.met1 == "Trapézios":
            try:
                if self.kz2 == "Simples":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.trapezio(f,a00,a01,nn)
                if self.kz2 == "Dupla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.doubletrap(f,a00,a01,a02,a03,nn)
                if self.kz2 == "Tripla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.tripletrap(f,a00,a01,a02,a03,a04,a05,nn)
            except ValueError:
                messagebox.showinfo('Cálculo de integrais','Erro - Nem todos os campos foram preenchidos')
        if self.met1 == "Simpson 1/3":
            try:
                if self.kz2 == "Simples":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.simpson1(f,a00,a01,nn)
                if self.kz2 == "Dupla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.doublesimp1(f,a00,a01,a02,a03,nn)
                if self.kz2 == "Tripla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.triplesimp1(f,a00,a01,a02,a03,a04,a05,nn)
            except ValueError:
                messagebox.showinfo('Cálculo de integrais','Erro - Nem todos os campos foram preenchidos')
        if self.met1 == "Simpson 3/8":
            try:
                if self.kz2 == "Simples":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.simpson2(f,a00,a01,nn)
                if self.kz2 == "Dupla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.doublesimp2(f,a00,a01,a02,a03,nn)
                if self.kz2 == "Tripla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.triplesimp2(f,a00,a01,a02,a03,a04,a05,nn)
            except ValueError:
                messagebox.showinfo('Cálculo de integrais','Erro - Nem todos os campos foram preenchidos')
        if self.met1 == "Boole":
            try:
                if self.kz2 == "Simples":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.boole(f,a00,a01,nn)
                if self.kz2 == "Dupla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.doubleboole(f,a00,a01,a02,a03,nn)
                if self.kz2 == "Tripla":
                    nn = int(self.interv.get()) #número de divisoes
                    self.resultado2 = integ.tripleboole(f,a00,a01,a02,a03,a04,a05,nn)
            except ValueError:
                messagebox.showinfo('Cálculo de integrais','Erro - Nem todos os campos foram preenchidos')
        if self.met1 == "Quadratura":
            if self.kz2 == "Simples":
                self.resultado2 = integ.quad(f,a00,a01)
            if self.kz2 == "Dupla":
                self.resultado2 = nquad(f,[[a00,a01],[a02,a03]])[0]
            if self.kz2 == "Tripla":
                self.resultado2 = nquad(f,[[a00,a01],[a02,a03],[a04,a05]])[0]  
    #-------------------------------------------------------------------------Expressando os resultados------------------------------------------------
        
        Label(self.frame_4,text="Resultado da integral da função",bg='#dfe3ee',font = ("Arial",10,'bold')).place(relx = 0.6, rely= 0.63, relwidth= 0.4)
        Label(self.frame_4,text="{:.4f}".format(self.resultado2),bg='#dfe3ee',font = ("Arial",10,'bold')).place(relx = 0.6, rely= 0.7, relwidth= 0.4)
        try:
            nn = int(self.interv.get())
        except ValueError:
            nn = 100
        xa = np.linspace(a00,a01,nn)

        #-----------------------------------------------------------------Graficando as curvas----------------------------------------------------------------
        if self.kz2 == "Simples":
            plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=10)
            fig = Figure(figsize=(4.6,3.4),dpi=70)
            a = fig.add_subplot(111)
            a.grid(True)
            a.set_title('Curva da função solicitada',fontsize=12)
            fig.patch.set_color('#dfe3ee')
            #a.set_facecolor('#dfe3ee')
            yplot = [f(i) for i in xa]
            a.plot(xa,yplot,'b')
            canvas = FigureCanvasTkAgg(fig,master=self.frame_5)
            canvas.get_tk_widget().place(relx=0.22,rely=0.01)
            canvas.draw()
            
        if self.kz2 == "Dupla":
            jj = []
            ya = np.linspace(a02,a03,nn)
            plt.rc('xtick', labelsize=6)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=6)
            for i in xa:
                jjj = []
                for j in ya:
                    jjj.append(f(i,j))
                jj.append(jjj)
            zz=np.array(jj)
            fig = Figure(figsize=(3.8,2.4))
            a = fig.add_subplot(111,projection='3d')
            a.grid(True)
            a.set_title('Curva da função solicitada',fontsize=8)
            fig.patch.set_color('#dfe3ee')
            a.set_facecolor('#dfe3ee')
            X, Y = np.meshgrid(xa, ya)
            bb = a.plot_surface(X, Y, zz, rstride=1, cstride=1, cmap='jet')
            fig.colorbar(bb, shrink=0.7, aspect=10)
            canvas = FigureCanvasTkAgg(fig,master=self.frame_5)
            canvas.get_tk_widget().place(relx=0.16,rely=0.0)
            canvas.draw()

        if self.kz2 == "Tripla":
            jj = []
            ya = np.linspace(a02,a03,nn)
            plt.rc('xtick', labelsize=6)    # fontsize of the tick labels
            plt.rc('ytick', labelsize=6)
            for i in xa:
                jjj = []
                for j in ya:
                    jjj.append(f(i,j,a04))
                jj.append(jjj)
            zz=np.array(jj)
            fig = Figure(figsize=(3.8,2.4))
            a = fig.add_subplot(111,projection='3d')
            a.grid(True)
            a.set_title('Curva da função solicitada em z = {:.2f}'.format(a04),fontsize=8)
            fig.patch.set_color('#dfe3ee')
            a.set_facecolor('#dfe3ee')
            X, Y = np.meshgrid(xa, ya)
            bb = a.plot_surface(X, Y, zz, rstride=1, cstride=1, cmap='jet')
            fig.colorbar(bb, shrink=0.7, aspect=10)
            canvas = FigureCanvasTkAgg(fig,master=self.frame_5)
            canvas.get_tk_widget().place(relx=0.16,rely=0.0)
            canvas.draw()
            

    #-------------------------------------------------------------Expressando eventos de entrada----------------------------------------------------
    def event2(self):
        self.kz1 = self.zz2.get()
        if self.kz1 == "Trapézios" or self.kz1 == "Simpson 1/3" or self.kz1 == "Simpson 3/8" or self.kz1 == "Boole":
            Label(self.frame_4,text='Insira o número de intervalos',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.63)
            Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.interv).place(relx= 0.05, rely= 0.7, relwidth= 0.1)#Intervalos
        else:
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.63, relwidth = 0.5)
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.7, relwidth = 0.5)

    def event3(self):
        self.kz2 = self.zz3.get()
        if self.kz2 == "Dupla":
            Label(self.frame_4,text='Y inicial',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.23)
            Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a2).place(relx= 0.16, rely= 0.3, relwidth= 0.08)#primeiro valor
            Label(self.frame_4,text='Y final',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.43)
            Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a3).place(relx= 0.16, rely= 0.5, relwidth= 0.08)#segundo valor
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.27, rely=0.23, relwidth = 0.1)
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.27, rely=0.3, relwidth = 0.1)
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.27, rely=0.43, relwidth = 0.1)
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.27, rely=0.5, relwidth = 0.1)
        elif self.kz2 == "Tripla":
            Label(self.frame_4,text='Y inicial',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.23)
            Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a2).place(relx= 0.16, rely= 0.3, relwidth= 0.08)#primeiro valor
            Label(self.frame_4,text='Y final',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.43)
            Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a3).place(relx= 0.16, rely= 0.5, relwidth= 0.08)#segundo valor
            Label(self.frame_4,text='Z inicial',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.27, rely=0.23)
            Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a4).place(relx= 0.27, rely= 0.3, relwidth= 0.08)#primeiro valor
            Label(self.frame_4,text='Z final',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.27, rely=0.43)
            Entry(self.frame_4,justify='center',font = ("Arial",10),width=25,textvariable=self.a5).place(relx= 0.27, rely= 0.5, relwidth= 0.08)#segundo valor      
        else:
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.23, relwidth = 0.3)
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.3, relwidth = 0.3)
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.43, relwidth = 0.3)
            Label(self.frame_4,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.16, rely=0.5, relwidth = 0.3)


#----------------------------------------------------------Modelo de REGRESSÃO----------------------------------------------------------------------------------------

#-----------------------------------------------------------MODELO DE EQUAÇÕES DIFERENCIAIS---------------------------------------------------------------------------
   
    def edos(self):
        #----------Características básicas do objeto----------
        self.root3 = Toplevel()#tix.Tk()
        self.root3['bg'] = 'seashell2'
        self.root3.title("Aplicação didática em cálculo numérico")
        self.root3.geometry('600x600')
        self.fram_3()
        self.listam()
        self.func2 = StringVar() #funcao
        self.func3 = StringVar()
        self.b0 = StringVar() #valor inical EM X
        self.b1 = StringVar() #valor inicial EM Y
        self.b2 = StringVar() #passo
        self.b3 = StringVar() #numero de intervalos
        self.c0 = StringVar() #Valor inicial em X'
        self.zz5 = StringVar() #evento para a edo
        self.zz6 = StringVar() #evento para a ordem da edo
        
        self.it2 = StringVar()

         #-------------------------Spinbox---------------------------------------------------------------------------------------------------------------------
        self.met5 = ["Euler Explícito","Runge-Kutta","Euler Implícito","Adams-Moulton","Euler Aprimorado","RK Implícito"]
        Label(self.f_9,text = "Metodologia",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.1,rely=0.03)
        Spinbox(self.f_9,values=self.met5,justify = "center",textvariable=self.zz5).place(relx = 0.1,rely = 0.2,relwidth= 0.7)

        Label(self.f_9,text = "Ordem da EDO",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.1,rely=0.45)
        self.met6 = ["Primeira","Segunda"]
        Spinbox(self.f_9,values=self.met6,justify = "center",textvariable=self.zz6,command = self.event5).place(relx = 0.1,rely = 0.62,relwidth= 0.7)

        #--------------Entrada---------------------------------------------------------------------------------------------------------------------------------
        Label(self.f_7,text="Insira Y' = f(x,y)",bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.03)
        Entry(self.f_7,justify='center',font = ("Arial",10),width=38,textvariable=self.func2).place(relx= 0.05, rely= 0.1, relwidth= 0.38)#função
        
        Label(self.f_7,text='X inicial',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.23, rely=0.43)
        Entry(self.f_7,justify='center',font = ("Arial",10),width=25,textvariable=self.b0).place(relx= 0.23, rely= 0.5, relwidth= 0.08)#primeiro valor
        
        Label(self.f_7,text='Y inicial',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.23, rely=0.63)
        Entry(self.f_7,justify='center',font = ("Arial",10),width=25,textvariable=self.b1).place(relx= 0.23, rely= 0.7, relwidth= 0.08)#segundo valor

        Label(self.f_7,text='Passo',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.43)
        Entry(self.f_7,justify='center',font = ("Arial",10),width=25,textvariable=self.b2).place(relx= 0.05, rely= 0.5, relwidth= 0.08)#primeiro valor
        
        Label(self.f_7,text='Intervalos',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.63)
        Entry(self.f_7,justify='center',font = ("Arial",10),width=25,textvariable=self.b3).place(relx= 0.05, rely= 0.7, relwidth= 0.08)#segundo valor

        #-------------------------Botões------------------------------------------------------------------------------------------------------------------------
        Button(self.f_7, text = 'Calcular', width = 25, font = ('Verdana',10,'bold'),bg = '#107db2',fg = 'white',
               command=self.edocalc).place(relx= 0.05, rely= 0.85,relwidth=0.3)
        Button(self.f_7, text = 'Exportar resultados', width = 25, font = ('Verdana',10,'bold'),bg = '#107db2',fg = 'white',
               command = self.exportEDO).place(relx= 0.6, rely= 0.85,relwidth=0.3)
        
        self.root3.resizable(False,False) #impeço ampliar a janela
        self.root3.mainloop()

    def listam(self):
        self.Cli = ttk.Treeview(self.f_8, height=3,
                                     column=("x", "f(x,y)"))
        self.Cli.heading("#0", text="")
        self.Cli.heading("#1", text="x")
        self.Cli.heading("#2", text="f(x,y)")
        self.Cli.column("#0", width=1)
        self.Cli.column("#1", width=20)
        self.Cli.column("#2", width=20)
        self.Cli.place(relx=0.6, rely=0.05, relwidth=0.35, relheight=0.9)

        self.scr = Scrollbar(self.f_8, orient='vertical',command=self.Cli.yview)
        self.Cli.configure(yscroll=self.scr.set)
        self.scr.place(relx=0.95, rely=0.05, relwidth=0.02, relheight=0.9)


    def edocalc(self):
        try:
            self.kz5 = self.zz5.get()
            self.kzed = self.zz6.get()
            if self.kz5 == "Euler Explícito" and self.kzed == "Primeira":
                x,y = symbols('x y')
                expr = self.func2.get().lower() #obtendo a função simbólica
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                f = lambdify([x,y],expr,modules=['math']) #converti em função
                self.resedo = eqd.eulerexplicito(f,a00,a01,a02,a03)

            if self.kz5 == "Runge-Kutta" and self.kzed == "Primeira":
                x,y = symbols('x y')
                expr = self.func2.get().lower() #obtendo a função simbólica
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                f = lambdify([x,y],expr,modules=['math']) #converti em função
                self.resedo = eqd.rungekutta4(f,a00,a01,a02,a03)

            if self.kz5 == "Euler Implícito" and self.kzed == "Primeira":
                x,y = symbols('x y')
                expr = self.func2.get().lower() #obtendo a função simbólica
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                f = lambdify([x,y],expr,modules=['math']) #converti em função
                self.resedo = eqd.implicitoeuler(f,a00,a01,a02,a03)

            if self.kz5 == "Adams-Moulton" and self.kzed == "Primeira":
                x,y = symbols('x y')
                expr = self.func2.get().lower() #obtendo a função simbólica
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                f = lambdify([x,y],expr,modules=['math']) #converti em função
                self.resedo = eqd.adam(f,a00,a01,a02,a03)

            if self.kz5 == "Euler Aprimorado" and self.kzed == "Primeira":
                x,y = symbols('x y')
                expr = self.func2.get().lower() #obtendo a função simbólica
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                f = lambdify([x,y],expr,modules=['math']) #converti em função
                self.resedo = eqd.eulerapr(f,a00,a01,a02,a03)

            if self.kz5 == "RK Implícito" and self.kzed == "Primeira":
                x,y = symbols('x y')
                expr = self.func2.get().lower() #obtendo a função simbólica
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                f = lambdify([x,y],expr,modules=['math']) #converti em função
                self.resedo = eqd.implicitorunge(f,a00,a01,a02,a03)

            if self.kz5 == "Euler Explícito" and self.kzed == "Segunda":
                x,y,t = symbols('x y t')
                expr = self.func2.get().lower() #obtendo a função simbólica
                expr2 = self.func3.get().lower()
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                a04 = float(self.c0.get())
                f1 = lambdify([x,y,t],expr,modules=['math']) #converti em função
                f2 = lambdify([x,y,t],expr2,modules=['math']) #converti em função
                self.resedo = eqd.euler2(f2,f1,a00,a01,a04,a02,a03)

            if self.kz5 == "Euler Aprimorado" and self.kzed == "Segunda":
                x,y,t = symbols('x y t')
                expr = self.func2.get().lower() #obtendo a função simbólica
                expr2 = self.func3.get().lower()
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                a04 = float(self.c0.get())
                f1 = lambdify([x,y,t],expr,modules=['math']) #converti em função
                f2 = lambdify([x,y,t],expr2,modules=['math']) #converti em função
                self.resedo = eqd.euler2(f2,f1,a00,a01,a04,a02,a03)

            if self.kz5 == "Euler Implícito" and self.kzed == "Segunda":
                x,y,t = symbols('x y t')
                expr = self.func2.get().lower() #obtendo a função simbólica
                expr2 = self.func3.get().lower()
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                a04 = float(self.c0.get())
                f1 = lambdify([x,y,t],expr,modules=['math']) #converti em função
                f2 = lambdify([x,y,t],expr2,modules=['math']) #converti em função
                self.resedo = eqd.euler2(f2,f1,a00,a01,a04,a02,a03)

            if self.kz5 == "Adams-Moulton" and self.kzed == "Segunda":
                x,y,t = symbols('x y t')
                expr = self.func2.get().lower() #obtendo a função simbólica
                expr2 = self.func3.get().lower()
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                a04 = float(self.c0.get())
                f1 = lambdify([x,y,t],expr,modules=['math']) #converti em função
                f2 = lambdify([x,y,t],expr2,modules=['math']) #converti em função
                self.resedo = eqd.adam2(f2,f1,a00,a01,a04,a02,a03)

            if self.kz5 == "Runge-Kutta" and self.kzed == "Segunda":
                x,y,t = symbols('x y t')
                expr = self.func2.get().lower() #obtendo a função simbólica
                expr2 = self.func3.get().lower()
                a00 = float(self.b0.get()) 
                a01 = float(self.b1.get()) #obtendo a precisão desejada
                a02 = float(self.b2.get()) #obtendo o primeiro chute inicial
                a03 = int(self.b3.get()) #obtendo a precisão desejada
                a04 = float(self.c0.get())
                f1 = lambdify([x,y,t],expr,modules=['math']) #converti em função
                f2 = lambdify([x,y,t],expr2,modules=['math']) #converti em função
                self.resedo = eqd.runge2(f2,f1,a00,a01,a04,a02,a03)
           
        except ValueError:
            messagebox.showinfo('Cálculo de integrais','Erro - Nem todos os campos foram preenchidos')

        
        dff = self.resedo #resultado de cada iteração
        self.Cli.delete(*self.Cli.get_children()) #apago os dados anteriores
        self.T1 = dff['t'].values #valores de x
        self.Y1 = dff['y'].values #valores de y
        for i,j in zip(self.T1,self.Y1):
            self.Cli.insert("","end",values = ("{:.5f}".format(i),"{:.5f}".format(j)))

        plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=10)
        fig = Figure(figsize=(4.5,3.4),dpi=70)
        a = fig.add_subplot(111)
        a.grid(True)
        a.set_title('Curva solução da equação diferencial',fontsize=12)
        fig.patch.set_color('#dfe3ee')
            #a.set_facecolor('#dfe3ee')
        #yplot = [f(i) for i in xa]
        a.plot(self.T1,self.Y1,'b')
        canvas = FigureCanvasTkAgg(fig,master=self.f_8)
        canvas.get_tk_widget().place(relx=0.03,rely=0.01)
        canvas.draw()

    def exportEDO(self):
        try:
            self.resedo.to_excel('ResultadoEDO.xlsx')
            messagebox.showinfo('Cálculo de EDO','Resultado exportado com sucesso')
        except AttributeError:
            messagebox.showinfo('Cálculo de raízes','Erro - Impossível exportar. Nenhum cálculo foi realizado.')
        

    #------------------------------------------------------Procedimento para equações diferenciais de primeira ordem---------------------------------------------

    
        #-----------------------------Frame---------------------------------------------------------------------------------------------------------------------------
    def frames_tela(self):
        #-------------------------------------------Frame Raizes ---------------------------------------------------------------
        self.frame_1 = Frame(self.root, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.48)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=2)
        self.frame_2.place(relx=0.02, rely=0.54, relwidth=0.96, relheight=0.42)

        self.frame_3 = Frame(self.frame_1, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_3.place(relx=0.66, rely=0.02, relwidth=0.3, relheight=0.78)

    def frame2(self):
        #-------------------------------------------Frame Integral---------------------------------------------------------------
        self.frame_4 = Frame(self.root2, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_4.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.48)

        self.frame_5 = Frame(self.root2, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=2)
        self.frame_5.place(relx=0.02, rely=0.54, relwidth=0.96, relheight=0.42)

        self.frame_6 = Frame(self.frame_4, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.frame_6.place(relx=0.66, rely=0.02, relwidth=0.3, relheight=0.6)

    def fram_3(self):
        self.f_7 = Frame(self.root3, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.f_7.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.48)

        self.f_8 = Frame(self.root3, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=2)
        self.f_8.place(relx=0.02, rely=0.54, relwidth=0.96, relheight=0.42)

        self.f_9 = Frame(self.f_7, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.f_9.place(relx=0.6, rely=0.02, relwidth=0.3, relheight=0.6)

    def fram_4(self):
        self.f_10 = Frame(self.root4, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.f_10.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.5)

        self.f_11 = Frame(self.root4, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=2)
        self.f_11.place(relx=0.02, rely=0.54, relwidth=0.96, relheight=0.42)

        self.f_12 = Frame(self.f_10, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.f_12.place(relx=0.6, rely=0.02, relwidth=0.3, relheight=0.6)

    def fram_5(self):
        self.f_13 = Frame(self.root5, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.f_13.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        #self.f_14 = Frame(self.root5, bd=4, bg='#dfe3ee',
         #                    highlightbackground='#759fe6', highlightthickness=2)
        #self.f_14.place(relx=0.02, rely=0.54, relwidth=0.96, relheight=0.42)

        self.f_15 = Frame(self.f_13, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.f_15.place(relx=0.45, rely=0.1, relwidth=0.5, relheight=0.45)

        self.f_16 = Frame(self.f_13, bd=4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=2)
        self.f_16.place(relx=0.55, rely=0.6, relwidth=0.3, relheight=0.3)


#---------------------------------------------------------------evento mudança de ordem da EDO--------------------------------------------------------------------------

    def event5(self):
        self.kzed = self.zz6.get()
        if self.kzed == "Primeira":
            Label(self.f_7,text='                    ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.43, rely=0.43, relwidth = 0.15)
            Label(self.f_7,text='               ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.43, rely=0.5, relwidth = 0.1)
            Label(self.f_7,text='                    ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.23, relwidth = 0.23)
            Label(self.f_7,text='                    ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.3, relwidth = 0.38)
        else:
            Label(self.f_7,text='dY/dt inicial',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.43, rely=0.43)
            Entry(self.f_7,justify='center',font = ("Arial",10),width=25,textvariable=self.c0).place(relx= 0.43, rely= 0.5, relwidth= 0.08)#primeiro valor

            Label(self.f_7,text="Insira Y = f(x,y)",bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.23)
            Entry(self.f_7,justify='center',font = ("Arial",10),width=38,textvariable=self.func3).place(relx= 0.05, rely= 0.3, relwidth = 0.38)#função
            


    
#----------------------------------------------------------Modelo de PLANEJAMENTO DE EXPERIMENTOS----------------------------------------------------------------------------------------

    def otimizacao(self):
        #----------Características básicas do objeto----------
        self.root4 = Toplevel()#tix.Tk()
        self.root4['bg'] = 'seashell2'
        self.root4.title("Aplicação didática em cálculo numérico")
        self.root4.geometry('600x600')
        self.fram_4()
        self.lista_opt()

        #---------------variáveis-------------------------------------------------------------------------------------------------------------------------------
        self.funopt = StringVar() #FUNÇÃO
        self.qtdopt = StringVar()
        self.x0opt = StringVar() #CHUTE INICIAL
        self.rropt = StringVar() #metodo
        self.itopt = IntVar() #CRITERIO DE PARADA
        self.precopt = StringVar() #PRECISAO

        self.metopt = ["Newton-Raphson","Gradiente Descendente","Busca Aleatória","Seção Áurea"]
        Label(self.f_12,text = "Metodologia",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05,rely=0.03)
        Spinbox(self.f_12,values=self.metopt,justify = "center",textvariable=self.rropt,command=self.eventopt).place(relx = 0.05,rely = 0.17,relwidth= 0.85)
        
        #---------------------------Radiobutton----------------------------------------------------------------------------------------------------------------
        Label(self.f_12,text = "Critério de parada",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05,rely=0.4)
        self.opt1 = Radiobutton(self.f_12, text="|f(x) - f(x-1)| < Precisão",bg='#dfe3ee',font = ("Arial",8,"bold"),value=0,variable=self.itopt).place(relx=0.05,rely=0.54)
        self.opt2 = Radiobutton(self.f_12, text="|xn - xn-1| < Precisão",bg='#dfe3ee',font = ("Arial",8,"bold"),value=1,variable=self.itopt).place(relx=0.05,rely=0.7)
        
        #--------------Entrada---------------------------------------------------------------------------------------------------------------------------------
        Label(self.f_10,text='Insira sua função f(x)',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.02)
        Entry(self.f_10,justify='center',font = ("Arial",11),width=35,textvariable=self.funopt).place(relx= 0.05, rely= 0.1, relwidth= 0.35)#função
        
        Label(self.f_10,text='Insira a precisão',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.22)
        Entry(self.f_10,justify='center',font = ("Arial",11),width=25,textvariable=self.precopt).place(relx= 0.05, rely= 0.3, relwidth= 0.14)#função
        
        Label(self.f_10,text='Primeiro valor inicial',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.42)
        Entry(self.f_10,justify='center',font = ("Arial",11),width=25,textvariable=self.x0opt).place(relx= 0.05, rely= 0.5, relwidth= 0.14)#chute inicial

        #-------------------------Botões------------------------------------------------------------------------------------------------------------------------
        Button(self.f_10, text = 'Calcular', width = 20, font = ('Verdana',10,'bold'),bg = '#107db2',fg = 'white',command = self.otimization).place(relx= 0.05, rely= 0.85, relwidth= 0.20)
        self.root4.resizable(False,False) #impeço ampliar a janela
        self.root4.mainloop()

    def eventopt(self):
        self.it_r2opt = self.rropt.get()
        self.x01opt = StringVar()
        self.minmax = StringVar()
        if self.it_r2opt == "Busca Aleatória":
            self.mopt = ['Mínimo','Máximo']
            Label(self.f_10,text='Tipo de extremo',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.35, rely=0.22)
            Spinbox(self.f_10,values=self.mopt,justify = "center",textvariable=self.minmax).place(relx = 0.35,rely = 0.3,relwidth= 0.15)
            Label(self.f_10,text='Segundo valor inicial',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.62)
            Label(self.f_10,text='Primeiro valor inicial',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.05, rely=0.42)
            self.e3 = Entry(self.f_10,justify='center',font = ("Arial",11),width=25,textvariable=self.x01opt).place(relx= 0.05, rely= 0.7, relwidth= 0.14)#chute inicial
        else:
            Label(self.f_10,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.62, relwidth = 0.5)
            Label(self.f_10,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.05, rely=0.7, relwidth = 0.5)
            Label(self.f_10,text='                           ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.35, rely=0.22)
            Label(self.f_10,text='                           ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.35, rely=0.3)

    def otimization(self):
        x = symbols('x') #entrada de função símbolica
        cb = self.itopt.get() #para mudar o critério de parada
        
        try:
            expr = self.funopt.get().lower() #obtendo a função simbólica
            x00 = float(self.x0opt.get()) #obtendo o primeiro chute inicial
            preci = float(self.precopt.get()) #obtendo a precisão desejada
            f = lambdify(x,expr,modules=['math']) #converti em função
        except ValueError:
            messagebox.showinfo('Cálculo de otimização','Erro - Nem todos os campos foram preenchidos')
        
        self.it_r2opt = self.rropt.get() #seleção do método
        if self.it_r2opt == "Newton-Raphson":
            self.resultadopt = optim.NewtonRaphson2(f,x00,cb,preci)
        if self.it_r2opt == "Gradiente Descendente":
            self.resultadopt = optim.gradiente_descendente(f,x00,cb,preci)
        if self.it_r2opt == "Busca Aleatória":
            fopt = float(self.x01opt.get())
            minmax = self.minmax.get()
            self.resultadopt = optim.montecarlo(f,x00,fopt,minmax,cb,preci)
            
        self.r1opt = Label(self.f_10,text="Valor de x ótimo",bg='#dfe3ee',
                           font = ("Arial",9,'bold')).place(relx= 0.55, rely= 0.63, relwidth= 0.40)
        self.r2opt = Label(self.f_10,text="Valor f(x) ótimo",bg='#dfe3ee',
                           font = ("Arial",9,'bold')).place(relx= 0.55, rely= 0.77, relwidth= 0.40)

        if type(self.resultadopt[0])==float or type(self.resultadopt[0])==int:
            self.resul1opt = Label(self.f_10,text="{:.4f}".format(self.resultadopt[0]),bg='#dfe3ee',
                           font = ("Arial",9,'bold')).place(relx= 0.6, rely= 0.7, relwidth= 0.30)
            self.resu2opt = Label(self.f_10,text="{:.4f}".format(self.resultadopt[1]),bg='#dfe3ee',
                           font = ("Arial",9,'bold')).place(relx= 0.6, rely= 0.84, relwidth= 0.30)

        dff = self.resultadopt[3] #resultado de cada iteração
        self.listaOpt.delete(*self.listaOpt.get_children()) #apago os dados anteriores
        self.T1opt = dff['x'].values #valores de x
        self.Y1opt = dff['y'].values #valores de y
        self.eropt = dff['Erro'].values #valores de y
        for i,j,k in zip(self.T1opt,self.Y1opt,self.eropt):
            self.listaOpt.insert("","end",values = ("{:.3f}".format(i),"{:.3f}".format(j),"{:.3f}".format(k)))

        plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=10)
        fig = Figure(figsize=(4.5,3.4),dpi=70)
        a = fig.add_subplot(111)
        a.grid(True)
        xop = np.linspace(self.resultadopt[0]-5,self.resultadopt[0]+5,100)
        yop = [f(x) for x in xop]
        a.set_title('Curva solução da função f(x)',fontsize=12)
        fig.patch.set_color('#dfe3ee')
            #a.set_facecolor('#dfe3ee')
        #yplot = [f(i) for i in xa]
        a.plot(xop,yop,'b')
        canvas = FigureCanvasTkAgg(fig,master=self.f_11)
        canvas.get_tk_widget().place(relx=0.03,rely=0.01)
        canvas.draw()

    #-------------------------------------Tabela para resultados por iteração------------------------------------------------------------------------------------------
    def lista_opt(self):
        self.listaOpt = ttk.Treeview(self.f_11, height=3,
                                     column=("x", "f(x)", "Erro"))
        self.listaOpt.heading("#0", text="")
        self.listaOpt.heading("#1", text="x")
        self.listaOpt.heading("#2", text="f(x)")
        self.listaOpt.heading("#3", text="Erro")
        self.listaOpt.column("#0", width=1)
        self.listaOpt.column("#1", width=20)
        self.listaOpt.column("#2", width=20)
        self.listaOpt.column("#3", width=20)
        self.listaOpt.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.9)

        self.scroolLista_opt = Scrollbar(self.f_11, orient='vertical',command=self.listaOpt.yview)
        self.listaOpt.configure(yscroll=self.scroolLista_opt.set)
        self.scroolLista_opt.place(relx=0.95, rely=0.05, relwidth=0.02, relheight=0.9)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def estat(self):
        #----------Características básicas do objeto----------
        def _on_frame_configure(self, event=None):
            canvas.configure(scrollregion=canvas.bbox("all"),background="seashell2",width=264,highlightbackground= '#759fe6', highlightthickness=2,height=300)
            
        self.root5 = Toplevel()#tix.Tk()
        self.root5['bg'] = 'seashell2'
        self.root5.title("Aplicação didática em cálculo numérico")
        self.root5.geometry('900x600')
        self.fram_5()
        #self.lista()
        frame = Frame(self.f_13, borderwidth=0.3, background="seashell2",height=300)
        frame.place(relx=0.03,rely=0.10)


        yscrollbar = Scrollbar(frame,background='gray')
        yscrollbar.grid(column=1, row=0)

        canvas = Canvas(frame, bd=0, relief=SUNKEN, yscrollcommand=yscrollbar.set,height=300)
        canvas.grid(column=0, row=0)

        yscrollbar.config(command=canvas.yview)

        frame = Frame(canvas, borderwidth=1, background='seashell2',height=300) #refere-se a caixa toda, com exceção da barra d rolagem
        canvas.create_window(1, 2, window=frame, anchor='nw')
        frame.bind("<Configure>", _on_frame_configure)

        self.rrest = StringVar() #metodo
        
        a,a1,a2,a3=StringVar(),StringVar(),StringVar(),StringVar()
        b,b1,b2,b3=StringVar(),StringVar(),StringVar(),StringVar()
        c,c1,c2,c3=StringVar(),StringVar(),StringVar(),StringVar()
        d,d1,d2,d3=StringVar(),StringVar(),StringVar(),StringVar()
        e,e1,e2,e3=StringVar(),StringVar(),StringVar(),StringVar()
        f,f1,f2,f3=StringVar(),StringVar(),StringVar(),StringVar()
        g,g1,g2,g3=StringVar(),StringVar(),StringVar(),StringVar()
        h,h1,h2,h3=StringVar(),StringVar(),StringVar(),StringVar()
        i,i1,i2,i3=StringVar(),StringVar(),StringVar(),StringVar()
        j,j1,j2,j3=StringVar(),StringVar(),StringVar(),StringVar()
        k,k1,k2,k3=StringVar(),StringVar(),StringVar(),StringVar()
        l,l1,l2,l3=StringVar(),StringVar(),StringVar(),StringVar()
        m,m1,m2,m3=StringVar(),StringVar(),StringVar(),StringVar()
        n,n1,n2,n3=StringVar(),StringVar(),StringVar(),StringVar()
        o,o1,o2,o3=StringVar(),StringVar(),StringVar(),StringVar()
        p,p1,p2,p3=StringVar(),StringVar(),StringVar(),StringVar()
        q,q1,q2,q3=StringVar(),StringVar(),StringVar(),StringVar()
        r,r1,r2,r3=StringVar(),StringVar(),StringVar(),StringVar()
        s,s1,s2,s3=StringVar(),StringVar(),StringVar(),StringVar()
        t,t1,t2,t3=StringVar(),StringVar(),StringVar(),StringVar()
        u,u1,u2,u3=StringVar(),StringVar(),StringVar(),StringVar()
        v,v1,v2,v3=StringVar(),StringVar(),StringVar(),StringVar()
        w,w1,w2,w3=StringVar(),StringVar(),StringVar(),StringVar()
        x,x1,x2,x3=StringVar(),StringVar(),StringVar(),StringVar()
        y,y1,y2,y3=StringVar(),StringVar(),StringVar(),StringVar()
        z,z1,z2,z3=StringVar(),StringVar(),StringVar(),StringVar()
        self.omegax = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1,v1,w1,x1,y1,z1]
        self.omegay = [a2,b2,c2,d2,e2,f2,g2,h2,i2,j2,k2,l2,m2,n2,o2,p2,q2,r2,s2,t2,u2,v2,w2,x2,y2,z2,
                       a3,b3,c3,d3,e3,f3,g3,h3,i3,j3,k3,l3,m3,n3,o3,p3,q3,r3,s3,t3,u3,v3,w3,x3,y3,z3]

            
        for i in range(52):
            if i==0:
                label = ttk.Label(frame, text="Valor de x",background='seashell2')
                label.grid(column=1, row=i)
                label = ttk.Label(frame, text="Valor de y",background='seashell2')
                label.grid(column=2, row=i)
            else:
                label = ttk.Label(frame,background='seashell2')
                label.grid(column=0, row=i)
                
                self.text = ttk.Entry(frame,justify='center',textvariable=self.omegax[i])
                self.text.grid(column=1, row=i)

                self.text1 = ttk.Entry(frame,justify='center',textvariable=self.omegay[i])
                self.text1.grid(column=2, row=i)
                
        self.metreg = ["Regressão Linear","Regressão Exponencial","Regressão Logística","Regressão Polinomial","Regressão Logaritmica"]
        Label(self.f_13,text = "Metodologia de regressão",bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.1,rely=0.65)
        Spinbox(self.f_13,values=self.metreg,justify = "center",textvariable=self.rrest,command = self.eventreg).place(relx = 0.13,rely = 0.69,relwidth= 0.15)

        Button(self.f_13, text = 'Calcular', width = 20, font = ('Verdana',10,'bold'),
               bg = '#107db2',fg = 'white',command=self.regre).place(relx= 0.1, rely= 0.85, relwidth= 0.20)
        Label(self.f_16,text='Equação da curva',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.26, rely=0.02)
        Label(self.f_16,text='Coeficiente b',bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.02, rely=0.36)
        Label(self.f_16,text='Coeficiente a',bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.02, rely=0.49)
        Label(self.f_16,text='Coeficiente de Determinação',bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.02, rely=0.62)
        
        self.root5.resizable(False,False) #impeço ampliar a janela
        self.root5.mainloop()
    #---------------------------------------------------------------Evento spinbox ordem polinomial-------------------------------------------------------------

    def eventreg(self):
        self.it_r2est2 = self.rrest.get()
        self.ordreg = IntVar()
        if self.it_r2est2 == "Regressão Polinomial":
            self.mopt2 = [2,3,4,5,6,7,8]
            Label(self.f_13,text='Ordem',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.17, rely=0.74)
            Spinbox(self.f_13,values=self.mopt2,justify = "center",textvariable=self.ordreg).place(relx = 0.175,rely = 0.78,relwidth= 0.05)
        else:
            Label(self.f_13,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.17, rely=0.74, relwidth = 0.15)
            Label(self.f_13,text='                           ',bg='#dfe3ee',font = ("Arial",9,"bold")).place(relx=0.17, rely=0.78, relwidth = 0.15)

    #--------------------------------------------------------------Regressao algoritmo-------------------------------------------------------------------------------
    def regre(self):
        self.x1reg=[]
        self.y1reg=[]
        self.it_r2est = self.rrest.get() #seleção do método
        for conti,contj in zip(self.omegax,self.omegay):
            try:
                self.x1reg.append(float(conti.get()))
                self.y1reg.append(float(contj.get()))
            except ValueError:
                pass
        if self.it_r2est == 'Regressão Linear':
            self.resultadolin = reglin.reglinear(self.x1reg,self.y1reg)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16, relwidth = 0.52)
            Label(self.f_16,text='y = bx + a',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.66, rely=0.36, relwidth = 0.3)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[0]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.36)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.76, rely=0.49, relwidth = 0.1)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[1]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.49)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[2]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.62)
            yop = [self.resultadolin[0]*x + self.resultadolin[1] for x in self.x1reg]
        if self.it_r2est == 'Regressão Exponencial':
            self.resultadolin = reglin.regexp(self.x1reg,self.y1reg)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16, relwidth = 0.52)
            Label(self.f_16,text='y = b*exp(a*x)',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.66, rely=0.36, relwidth = 0.3)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[1]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.36)
            Label(self.f_16,text='             ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.76, rely=0.49, relwidth = 0.1)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[0]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.49)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[2]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.62)
            yop = [self.resultadolin[1]*exp(x*self.resultadolin[0]) for x in self.x1reg]
        if self.it_r2est == 'Regressão Polinomial':
            n_pol = self.ordreg.get()
            self.resultadolin = reglin.regpol(self.x1reg,self.y1reg,n_pol)
            Label(self.f_16,text='      ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16, relwidth = 0.48)
            Label(self.f_16,text='      ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.72, rely=0.36, relwidth = 0.22)
            Spinbox(self.f_16,values=list(self.resultadolin[0]),justify = "center").place(relx = 0.72,rely = 0.36,relwidth= 0.23)
            #Label(self.f_16,text='{:.4f}'.format(self.resultadolin[1]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.36)
            Label(self.f_16,text='      ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.76, rely=0.49, relwidth = 0.1)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[1]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.49)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[2]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.62)
            yop = self.resultadolin[3]
        if self.it_r2est == 'Regressão Logística':
            self.resultadolin = reglin.reglog(self.x1reg,self.y1reg)
            Label(self.f_16,text='             ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16, relwidth = 0.38)
            Label(self.f_16,text='y = 1/1+exp(-a*(x - b))',bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.33, rely=0.16)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.66, rely=0.36, relwidth = 0.3)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[1]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.36)
            Label(self.f_16,text='             ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.76, rely=0.49, relwidth = 0.1)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[0]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.49)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[2]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.62)
            yop = self.resultadolin[3]
            self.x1reg = np.array(self.x1reg)/max(self.x1reg)
            self.y1reg = np.array(self.y1reg)/max(self.y1reg)
        if self.it_r2est == 'Regressão Logaritmica':
            self.resultadolin = reglin.regLN(self.x1reg,self.y1reg)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16, relwidth = 0.52)
            Label(self.f_16,text='y = b*Ln(x) + a',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.36, rely=0.16)
            Label(self.f_16,text='          ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.66, rely=0.36, relwidth = 0.3)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[0]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.36)
            Label(self.f_16,text='             ',bg='#dfe3ee',font = ("Arial",10,"bold")).place(relx=0.76, rely=0.49, relwidth = 0.1)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[1]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.49)
            Label(self.f_16,text='{:.4f}'.format(self.resultadolin[2]),bg='#dfe3ee',font = ("Arial",8,"bold")).place(relx=0.76, rely=0.62)
            yop = self.resultadolin[3]

        plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=10)
        fig = Figure(figsize=(5.7,3.4),dpi=70)
        a = fig.add_subplot(111)
        a.grid(True)
        #xop = np.linspace(self.resultadopt[0]-5,self.resultadopt[0]+5,100)
        
        a.set_title('Curva obtida por regressão',fontsize=12)
        fig.patch.set_color('#dfe3ee')
        a.scatter(self.x1reg,self.y1reg,color='blue')
        a.plot(self.x1reg,yop,'b')
        canvas = FigureCanvasTkAgg(fig,master=self.f_15)
        canvas.get_tk_widget().place(relx=0.01,rely=0.01)
        canvas.draw()

    
aplicacao()
