# This python script is to extract data along Cifalps2 profile from Stefeno's 3D Vp model(<30km)
# Start: Mao, 20200203, Grenoble, ISTerre, 214
# Last Run: 
#!/usr/bin/python3
import numpy as np
import pandas as pd
from IPython import embed
# Input file: Stefeno's model, profile lon-lat
# output1: dep lon lat vp
# output2: dep x(km,to fisrt station) vp
# plot1: profile(blacki line),staions(black circle),Stefeno model point(red point)
# plot2: cifalps2 model section from Stefeno

print ("Hello, python!")
# 1.get profile coordinates from Anne [longitude,latitude]

A = [4.46361,46.608372]
B = [6.994917,45.806924]
C = [7.9,45.417731]
D = [8.640197,44.378364]

slope_AB = (B[1]-A[1])/(B[0]-A[0])
slope_BC = (C[1]-B[1])/(C[0]-B[0])
slope_CD = (D[1]-C[1])/(D[0]-C[0])
print (slope_AB,slope_BC,slope_CD)

# 2.search for every depth, extract all the parameter along profile

homedir = "/home/zhl/work/rf/model"
Stefeno_model = homedir + "/LET-Stefano-Vp-3D"

for ite in range(0,30):
    dep_nu = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
    name = Stefeno_model + "/plane00" + dep_nu[ite] + ".0.xyz"
    embed()
    data = pd.read_csv(name)
    print (data) 
    
    fo.close()
    break
    



# 3.interpolate the vp cross profile
# 4.output1, output2

