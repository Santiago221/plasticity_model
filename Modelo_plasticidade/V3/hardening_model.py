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
        plt.savefig(nome + formato)

    def Imagem(self):
        plt.show()

    def DataFrame(self):
        print('Data Frame - Experimental')
        print(self.df,'\n')

# ################ Exemplos e utilizaçãp
# # Exemplo 1 - Titanio 
# # Entrada
# M       = 'Titânio Gr1'
# E       = 72000                                     #{MPa] Módulo de Elasticidade
# Sy      = 183                                       #[MPa] Limite de Escoamento
# Sut     = 287                                       #[MPa] Tensão máxima a tração
# emax    = 40                                        #[%]   Deformação onde ocorre o Sut
# pontos_multi = [4,5,7,10,20,28]                     #Pontos para o modelo multilinear
# Nome_imagem, formato = ['Modelos','.png']
# h       = Hardening(M,E,Sy,Sut,emax)                  # define as constantes do material 
# exp     = h.Experimental('ensaio_longitudinal_titanio.txt') # puxa os dados do experimental Stress vs Strain, pode usar o método Abrir_Arquivos 
# #exp     = h.Experimental(h.Abrir_Arquivos())
# h.DataFrame()                                       # Data frame com a curva de engenharia e a real 
# #bili    = h.Bilinear()                              # Modelo Bilinear 
# multi   = h.Multilinear(pontos_multi)               # Modelo Multilinear
# model   = h.Modelos(Nome_imagem,formato)            # Prepara a imagem
# img     = h.Imagem()                                # Mostra a imagem


# Exemplo 2 - 316L
M2 = '316L'
E2 = 200000
Sy2 = 290
Sut2 = 560
emax2 = 40
h2       = Hardening(M2,E2,Sy2,Sut2,emax2)
exp2     = h2.Experimental('ensaio_longitudinal_316L.txt') # puxa os dados do experimental Stress vs Strain, pode usar o método Abrir_Arquivos 
h2.DataFrame()
#bili2    = h2.Bilinear()
pontos_multi2 = [5,10,13,20,40] 
multi2 = h2.Multilinear(pontos_multi2)
Nome_imagem2, formato2 = ['Modelos2','.png']
model2 = h2.Modelos(Nome_imagem2,formato2)
img2     = h2.Imagem() 

