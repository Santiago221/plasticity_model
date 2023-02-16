## import
import numpy as np 
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

## Entrada
print('Propriedades - 316L:')
Sy = 183.95*1e6
print('Limite de escoamento [MPa] = {}'.format(Sy*1e-6))
ey = 0.2 # [%]
E = 72*1e9
print('Módulo de Elasticidade [GPa] = {}'.format(E*1e-6))
marker = [5,7,10,20,28]
print('')
## experimental
file = 'ensaio_longitudinal.txt'
df1 = pd.read_csv(file,'\t')
strain = (df1[['strain']].values.T[0])
stress = (df1[['stress']].values.T[0])
df1['stress_real']=df1['stress']*(1+(df1['strain']/100))

df1['strain_real']=np.log(1+(df1['strain']/100))
strainR = df1[['strain_real']].values.T[0]
stressR = df1[['stress_real']].values.T[0]
SE = E*ey 
Sut = df1['stress_real'].max()*1e6 
emax = df1['strain_real'].max()*1e2

## Bilinear 
Et_Sy = (Sut-Sy)/((emax -ey)*1e-2) # calcula modulo de elasticidade tangente
print('Modelo bilinear:')
print('Módulo de Tangente [MPa] = {}'.format(Et_Sy*1e-6))
x = np.zeros(3)
y = np.zeros(3)
y[1] = Sy
y[2] = Sut
x[1] = ey
x[2] = emax

## multilinear 
strain_multi = np.zeros(len(marker)+1)
stress_multi = np.zeros(len(marker)+1)
strain_multi[0] = ey*1e-2
stress_multi[0] = Sy
#E_multi[0] = E
for ii in range(len(marker)):
    stress_multi[ii+1] = stressR[marker[ii]-1]*1e6
    strain_multi[ii+1] = strainR[marker[ii]-1]
strain_multi = strain_multi*100

strain_multi=np.insert(strain_multi, [0],0)
stress_multi=np.insert(stress_multi, [0],0)

print('Modelo Multilinear')
for i in range(len(stress_multi)):
    print('Stress: {:02f} MPa Strain: {:3f} mm/mm'.format(stress_multi[i]*1e-6,strain_multi[i]*1e-2))

## usando modelos
A = 3.5*13
L0 = 50
df2 = pd.read_csv('bilinear.txt','\t')
F_bi = (df2[['F']].values.T[0])
d_bi = (df2[['D']].values.T[0])
S2 = (df2[['F']].values.T[0])/A
s2 = ((df2[['D']].values.T[0]))/L0
S2_r = S2*(1+s2)
s2_r = np.log(1+s2)

df3 = pd.read_csv('multilinear_real.txt','\t')
F_multi = (df3[['F']].values.T[0])
d_multi = (df3[['D']].values.T[0])
S3 = (df3[['F']].values.T[0])/A
s3 = ((df3[['D']].values.T[0]))/L0
S3_r = S3*(1+s3)
s3_r = np.log(1+s3)

df4 = pd.read_csv('multilinear_eng.txt','\t')
F_multi = (df4[['F']].values.T[0])
d_multi = (df4[['D']].values.T[0])
S4 = (df4[['F']].values.T[0])/A
s4 = ((df4[['D']].values.T[0]))/L0
S4_r = S3*(1+s4)
s4_r = np.log(1+s4)

## plot 
fig, ax = plt.subplots(facecolor='lightgray')
ax.plot(x,y*1e-6,'ks--', label = 'Modelo Bilinear')
ax.plot(strain_multi,stress_multi*1e-6,'r^--', label = 'Modelo Multilinear')
ax.plot(strain,stress,'c--',label = 'Experimental - Engenharia')
ax.plot(strainR*100,stressR,'b--',label = 'Experimental - Real')
plt.ylabel('Tensão [MPa]')
plt.xlabel('Deformação [%]')
##text1 = 'E =' + str(E*1e-9) + 'GPa' 
##text2 = 'Et =' + str(Et_Sy*1e-6) + 'MPa' 
##text3 = 'Sy =' + str(Sy*1e-6) + 'MPa'
##text4 = 'Sut =' + str(Sut*1e-6) + 'MPa'
##ax.text(0, 0, text1, ha='left')
###ax.text(emax*0.4 , (Sy*1.1)*1e-6, text2, ha='left')
##ax.text(ey*10, (Sy*0.9)*1e-6, text3, ha='left')
##ax.text(emax*0.8, Sut*1e-6, text4, ha='left')
ax.legend()
ax.grid(True)


fig2, ax2 = plt.subplots(facecolor='lightgray')
ax2.plot(strain,stress,'c--',label = 'Experimental - Engenharia')
ax2.plot(strainR*100,stressR,'r--',label = 'Experimental - Real')
ax2.plot(s2_r*100 ,S2_r,'k-',label = 'Numérico - Bilinear')
ax2.plot(s3_r*100 ,S3_r,'b-',label = 'Numérico - Mutilinear - Real ')
plt.ylabel('Tensão [MPa]')
plt.xlabel('Deformação [%]')
ax2.legend()
ax2.set_xlim(-1,21)
ax2.grid(True)
plt.show()


