###import
from tkinter import filedialog
from tkinter import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

### Classes
class Hardening:
    """
    [1] Todas as tensões devem ser passadas em MPa
    [2] Todas as deformações devem ser passadas em %
    """
    def __init__(self,material,E,Sy,Sut,emax):
        self.material = material
        self.E      = E
        self.Sy     = Sy
        self.Sut    = Sut
        self.emax   = emax/100
        self.ey     = 0.002
        self.exp    = False
        self.bi     = False
        self.multi  = False
        print('Material - ' + material)

    def Abrir_Arquivos(self):
        root = Tk()
        root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Selecione arquivo",filetypes = (("Arquivo de Texto","*.txt"),("Todos os Arquivos","*.*")))
        return root.filename
    
    def Experimental(self,arquivo):
        self.exp = True
        self.arquivo_exp    = arquivo    
        self.df         = pd.read_csv(self.arquivo_exp, '\t')
        self.strain_exp     = self.df[['strain']].values.T[0]
        self.stress_exp     = self.df[['stress']].values.T[0]
        self.df['strain_real'] = np.log(1+(self.df['strain']/100))
        self.df['stress_real'] = self.df['stress']*(1+(self.df['strain']/100))
        self.strainR = self.df[['strain_real']].values.T[0]*1e2 
        self.stressR = self.df[['stress_real']].values.T[0] 

    def Bilinear(self):
        self.bi = True
        self.Et = (self.Sut - self.Sy)/(self.emax - self.ey)
        print('Modelo Bilinear:')
        print('Módulo Tangente (Et) = {:8.3f} MPa'.format((self.Et)))
        print('')
        self.stress_bi = np.array([0,self.Sy,self.Sut])
        self.strain_bi = np.array([0,self.ey,self.emax])*1e2

    def Multilinear(self,pontos_multi):
        self.multi = True
        self.pontos_multi = pontos_multi
        self.strain_multi = np.zeros(len(self.pontos_multi) + 1)
        self.stress_multi = np.zeros(len(self.pontos_multi) + 1)
        self.stress_multi[0] = (self.Sy*1e-6)
        self.strain_multi[0] = (self.ey*1e2)
        for i in range(len(self.pontos_multi)):
            self.stress_multi[i + 1] = self.stressR[self.pontos_multi[i] - 1]
            self.strain_multi[i + 1] = self.strainR[self.pontos_multi[i] - 1]
        print('Modelo Multilinear:')
        for ii in range(len(self.stress_multi)):
            print('Tensão: {:8.3f} MPa - Deformação: {:4.3f} mm/mm'.format(self.stress_multi[ii],self.strain_multi[ii]*1e-2))
        print()
        
    def Modelos(self,nome,formato):
        fig, ax = plt.subplots()
        if self.exp:
            ax.plot(self.strain_exp,self.stress_exp,color= 'black',label = 'Texte Experimental - Engenharia')
            ax.plot(self.strainR,self.stressR,color= 'steelblue',label = 'Teste Experimental - Real')
        if self.bi:
            ax.plot(self.strain_bi,self.stress_bi,color= 'indigo',marker = 's',linestyle = '--',label = 'Modelo Bilinear')
        if self.multi:
            ax.plot(self.strain_multi,self.stress_multi,color= 'darkred',marker = '^',linestyle = '--',label = 'Modelo Multilinear')
        plt.ylabel('Tensão [MPa]')
        plt.xlabel('Deformação [%]')
        plt.title('Modelos de Plasticidade - ' + str(self.material))
        ax.legend()
        ax.grid(True)
        #plt.savefig(nome + formato)

    def Imagem(self):
        plt.show()

    def DataFrame(self):
        print('Data Frame - Experimental')
        print(self.df,'\n')