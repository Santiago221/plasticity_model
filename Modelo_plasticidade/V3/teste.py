import numpy as np
import pandas as pd
from matplotlib import pyplot as plt 

df = pd.read_csv('316L.txt', '\t')
strain_real = df[['s']].values.T[0]
stress_real = df[['S']].values.T[0]
print(df)
df['s_eng'] = (np.exp((df['s'])/100) - 1)*100
df['S_eng'] = df['S']/(1 + df['s_eng']/100) 
strain_eng = df[['s_eng']].values.T[0]
stress_eng = df[['S_eng']].values.T[0]

x = np.array([0,0.5])
E = 100000
y = E*x/100 + 0.02

fig, ax = plt.subplots()

ax.plot(strain_real,stress_real,'k--',label = 'Real')
ax.plot(strain_eng,stress_eng,'r--',label = 'Engenharia')
ax.plot(x,y,'b-',label = 'Linear')
plt.ylabel('Tensão [MPa]')
plt.xlabel('Deformação [%]')
plt.ylim([0,175])
plt.legend()
ax.grid()
plt.show()
