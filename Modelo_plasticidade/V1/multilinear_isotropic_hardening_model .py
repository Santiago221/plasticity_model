### imports
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
### experimental

df1 = pd.read_csv('ensaio_longitudinal.txt','\t')
strain = (df1[['strain']].values.T)
stress = (df1[['stress']].values.T)

### bilinear
Sy = 183.95*1e6 #[Pa]          
ey = 0.2 # [mm/mm]
E = 72*1e9 #[Pa]
Sut = 287.5*1e6 #[Pa]
emax = 40 #[%]
Et_Sy = (Sut-Sy)/(emax/100 -ey/100) #[Pa]
strain_bi = np.zeros(3)
stress_bi = np.zeros(3)
stress_bi[1] = Sy
stress_bi[2] = Sut
strain_bi[1] = ey
strain_bi[2] = emax

print('Modelo Bilinear:')
print('Sy: {:.2f} MPa'.format(Sy*1e-6))
print('Et: {:.2f} Pa \n'.format(Et_Sy*1e-6))

### multilinear
stn = [5.8,24,41.4]
strain_multi = []
stress_multi = []
erro = 3
size = len(strain[0])
for ii in range(len(stn)):
    for i in range(size):
        erro2 = abs((stn[ii] - strain[0,i])/stn[ii])
        if erro2*100<erro:
            strain_multi.append(strain[0,i])
            stress_multi.append(stress[0,i])
            
E_multi = []
for i in range(len(strain_multi)):
    if i == 0:
        E_multi.append((stress_multi[i]*1e6-Sy)/(strain_multi[i]/100 -ey/100))
    else:
        E_multi.append((stress_multi[i]*1e6-stress_multi[i-1]*1e6)/(strain_multi[i]/100 - strain_multi[i-1]/100))
strain_m = [0,ey]
for i in range(len(strain_multi)):
    strain_m.append(strain_multi[i])

stress_m = [0,Sy*1e-6]
for i in range(len(stress_multi)):
    stress_m.append(stress_multi[i])

print('Modelo Multilinear:')
for i in range(len(E_multi)):
    print('E{}: {:.2f} Pa -- Deformação {:.2f}%'.format(i,E_multi[i]*1e-6,strain_m[i+2]))
print('\n')


### Plot
fig, ax = plt.subplots(facecolor='lightgray')
ax.plot(strain_bi,stress_bi*1e-6,'k--', label = 'Modelo Bilinear')
ax.plot(strain_m,stress_m,'b.--', label = 'Modelo Multilinear')
ax.plot(strain.T,stress.T,'ro', label = 'Experimental')

plt.ylabel('Tensão [MPa]')
plt.xlabel('Deformação [%]')
text1 = 'E =' + str(E*1e-9) + 'GPa' 
text2 = 'Et =' + str(Et_Sy*1e-6) + 'MPa' 
text3 = 'Sy =' + str(Sy*1e-6) + 'MPa'
#ax.text(0, 0, text1, ha='left')
#ax.text(emax*0.4 , (Sy*1.1)*1e-6, text2, ha='left')
#ax.text(ey*10 , (Sy*0.9)*1e-6, text3, ha='left')
ax.legend()
ax.grid(True)
plt.show()   

input('')
