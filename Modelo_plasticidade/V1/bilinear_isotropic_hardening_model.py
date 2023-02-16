## 

import numpy as np 
from matplotlib import pyplot as plt
#Sy = float(input('Sy [MPa]:'))*1e6
Sy = 183.95*1e6
ey = 0.002 # [mm/mm]
#E = float(input('E [GPa]:'))*1e9
E = 72*1e9
SE = E*ey 
#Sut = float(input('Sut [MPa]:'))*1e6
Sut = 287.5*1e6 
#emax = float(input('def_sut [%]:'))
emax = 40
#Et_SE = (Sut-SE)/(emax/100 -ey)
Et_Sy = (Sut-Sy)/(emax/100 -ey)
print('SE [MPa] = {}'.format(SE*1e-6))
print('Módulo de Tangente [MPa] = {}'.format(Et_Sy*1e-6))
x = np.zeros(3)
y = np.zeros(3)
y[1] = Sy
y[2] = Sut
x[1] = ey
x[2] = emax

print(x)
print(y)
fig, ax = plt.subplots(facecolor='lightgray')
ax.plot(x,y*1e-6,'k--')
plt.ylabel('Tensão [MPa]')
plt.xlabel('Deformação [%]')
text1 = 'E =' + str(E*1e-9) + 'GPa' 
text2 = 'Et =' + str(Et_Sy*1e-6) + 'MPa' 
text3 = 'Sy =' + str(Sy*1e-6) + 'MPa'
ax.text(0, 0, text1, ha='left')
ax.text(emax*0.4 , (Sy*1.1)*1e-6, text2, ha='left')
ax.text(ey*10 , (Sy*0.9)*1e-6, text3, ha='left')

ax.grid(True)
plt.show()   
