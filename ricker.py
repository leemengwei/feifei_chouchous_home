import matplotlib.pyplot as plt
import numpy as np


#matrix = np.loadtxt(open("ricker.xz","r"),delimiter="\n")
#t=matrix[:,1]
#ricker=matrix[:,2]

f = open('ricker.xz','r')
matrix = f.readlines()
for line in matrix:
   row = line.split('\n')
   temp = row.split('\t')
   dateset.append(temp)
for i in range
   print(ma_float)
f.close()


plt.figure()
#plt.plot(t,ricker)
plt.show()

