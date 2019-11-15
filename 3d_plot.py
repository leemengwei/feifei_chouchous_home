import numpy as np
import matplotlib
from IPython import embed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_filttered_position_and_speed(raw_data, sample_ratio):
    #sample_index = np.random.choice(range(len(raw_data)), sample_num)
    sample_index = np.where(raw_data[:,3:].sum(axis=1)!=0)[0][::sample_ratio]
    sampled_data = raw_data[sample_index]
    shaped_data = raw_data.reshape(391,391,160,6)

    x = sampled_data[:,0]
    y = sampled_data[:,1]
    z = sampled_data[:,2]
    #s
    u = sampled_data[:,3]
    #w
    v = sampled_data[:,4]
    #sh
    w = sampled_data[:,5]
    return x,y,z,u,v,w

def NormalizeData(data):
    return 10*(data - np.min(data)) / (np.max(data) - np.min(data) + 1e-100)

if __name__ == "__main__":
    
    #Get data:
    print("Reading...")
    raw_data = np.loadtxt("out01_gre")

    #Re-arrange data:
    print("Preprocessing...")
    sample_ratio = 100
    x, y, z, u, v, w = get_filttered_position_and_speed(raw_data, sample_ratio)

    #Plot:
    plt.figure(figsize=(18,6))
    ax_1 = plt.subplot(131, projection='3d')
    ax_2 = plt.subplot(132, projection='3d')
    ax_3 = plt.subplot(133, projection='3d')

    ax_1.scatter(x, y, z, c=NormalizeData(np.abs(u))+1, cmap='viridis', s=NormalizeData(np.abs(u))+1)
    ax_2.scatter(x, y, z, c=NormalizeData(np.abs(v))+1, cmap='viridis', s=NormalizeData(np.abs(v))+1)
    ax_3.scatter(x, y, z, c=NormalizeData(np.abs(w))+1, cmap='viridis', s=NormalizeData(np.abs(w))+1)

    ax_1.set_title("U")
    ax_2.set_title("V")
    ax_3.set_title("W")

    ax_1.set_xlabel("X")
    ax_1.set_ylabel("Y")
    ax_1.set_zlabel("Z")
    ax_2.set_xlabel("X")
    ax_2.set_ylabel("Y")
    ax_2.set_zlabel("Z")
    ax_3.set_xlabel("X")
    ax_3.set_ylabel("Y")
    ax_3.set_zlabel("Z")

    plt.show()


