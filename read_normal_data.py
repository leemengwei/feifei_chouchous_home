



import matplotlib.pyplot as plt
import numpy as np




def get_data(filename):
    data = np.loadtxt(filename)
    return data


if __name__ == "__main__":
    #Configs:
    filename = "./ricker.xyz"

    #Get data:
    data = get_data(filename)

    #Plot:
    plt.plot(data[:,0], data[:,1])  #画线
    plt.scatter(data[:,0], data[:,1], color='red', alpha=0.5, s=10)   #画点(颜色，透明度，点的大小)
    
    plt.xlabel("Time")
    plt.ylabel("Amptitude")
    plt.title("Source point")
    plt.show()
    
