import numpy as np
import os
import matplotlib
from IPython import embed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob

def filtter_and_reshape_data(raw_data, CONFIG):
    if CONFIG.ONLY_MOVES:
        sample_index = np.where(raw_data[:,3:].sum(axis=1)!=0)[0][::CONFIG.SAMPLE_RATIO]
    else:
        sample_index = np.where(raw_data[:,3:].sum(axis=1)!=np.nan)[0][::CONFIG.SAMPLE_RATIO]
    sampled_data = raw_data[sample_index]
    shaped_data = raw_data.reshape(CONFIG.MODEL_SHAPE[0], CONFIG.MODEL_SHAPE[1], CONFIG.MODEL_SHAPE[2], 6)
    #Through axis:
    x = sampled_data[:,0]
    y = sampled_data[:,1]
    z = sampled_data[:,2]
    u = sampled_data[:,3]
    v = sampled_data[:,4]
    w = sampled_data[:,5]
    return x,y,z,u,v,w

def NormalizeData(data):
    return np.exp(4*(data - np.min(data)) / (np.max(data) - np.min(data) + 1e-20))

def get_max_min_over_all_files(all_files):
    print("Getting min and max...")
    min_value_u=1e9
    max_value_u=-1e9
    min_value_v=1e9
    max_value_v=-1e9
    min_value_w=1e9
    max_value_w=-1e9
    for one_file in all_files:
        raw_data = np.loadtxt("%s"%one_file)
        min_value_u = min(min_value_u, raw_data[:,3].min())
        max_value_u = max(max_value_u, raw_data[:,3].max())
        min_value_v = min(min_value_w, raw_data[:,4].min())
        max_value_v = max(max_value_w, raw_data[:,4].max())
        min_value_w = min(min_value_v, raw_data[:,5].min())
        max_value_w = max(max_value_v, raw_data[:,5].max())
    return min_value_u, max_value_u, min_value_v, max_value_v, min_value_w, max_value_w

if __name__ == "__main__":
    #Configurations:
    import config as CONFIG

    #Get data:
    all_files = glob.glob("./result_out/*")
    all_files.sort()
    #Search min and max:
    min_u, max_u, min_v, max_v, min_w, max_w = get_max_min_over_all_files(all_files)
    print("MinMaxValue over files of u,v,w:", min_u, max_u, min_v, max_v, min_w, max_w)  
    min_all = min(min_u, min_v, min_w)
    max_all = min(max_u, max_v, max_w)
    _ = (max_all-min_all)*0.2

    #Plot:
    for t,one_file in enumerate(all_files):
        print("Reading...%s"%one_file)
        raw_data = np.loadtxt("%s"%one_file)
        #Re-arrange data:
        print("Preprocessing...")
        x, y, z, u, v, w = filtter_and_reshape_data(raw_data, CONFIG)
        
        #Plot:
        fig = plt.figure(figsize=(18,6))
        fig.suptitle("On time %s with zoomer %s"%(t,CONFIG.ZOOMER))
        ax_1 = plt.subplot(131, projection='3d')
        ax_2 = plt.subplot(132, projection='3d')
        ax_3 = plt.subplot(133, projection='3d')

        #CONFIG.COLOR_STYLE = plt.cm.jet(np.linspace(0, 1, len(x)))
        norm_u = CONFIG.ZOOMER*u/max(abs(min_u),abs(max_u))
        norm_v = CONFIG.ZOOMER*v/max(abs(min_v),abs(max_v))
        norm_w = CONFIG.ZOOMER*w/max(abs(min_w),abs(max_w))
        ax_1.scatter(x, y, z, c=norm_u, cmap=CONFIG.COLOR_STYLE, s=NormalizeData(np.abs(u))+1, vmin=-1, vmax=1)
        ax_2.scatter(x, y, z, c=norm_v, cmap=CONFIG.COLOR_STYLE, s=NormalizeData(np.abs(v))+1, vmin=-1, vmax=1)
        ax_3.scatter(x, y, z, c=norm_w, cmap=CONFIG.COLOR_STYLE, s=NormalizeData(np.abs(w))+1, vmin=-1, vmax=1)
        #Colorbars:
        m1 = matplotlib.cm.ScalarMappable(cmap=eval("matplotlib.cm.%s"%CONFIG.COLOR_STYLE))
        m2 = matplotlib.cm.ScalarMappable(cmap=eval("matplotlib.cm.%s"%CONFIG.COLOR_STYLE))
        m3 = matplotlib.cm.ScalarMappable(cmap=eval("matplotlib.cm.%s"%CONFIG.COLOR_STYLE))
        m1.set_array(np.linspace(min_u, max_u, 100))
        m2.set_array(np.linspace(min_v, max_v, 100))
        m3.set_array(np.linspace(min_w, max_w, 100))
        plt.colorbar(m1, ax=ax_1, orientation='horizontal')
        plt.colorbar(m2, ax=ax_2, orientation='horizontal')
        plt.colorbar(m3, ax=ax_3, orientation='horizontal')
        
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

        plt.savefig("./pngs/%s_ZOOM%s"%(one_file.split('/')[-1], CONFIG.ZOOMER))
        #plt.show()
        plt.close() 
        fig.clf()

    #Use GPU render:
    #position = np.vstack((x,y,z)).T
    #colors = plt.cm.jet(np.linspace(1,0,len(position)))
    #try:
    #    import vispy
    #    import plot_utils
    #    from vispy import app, visuals, scene
    #    plot_utils.GPU_3d_scatter_plot(pos, colors)
    #    app.run()
    #except Exception as e:
    #    print("Perhaps vispy not installed, pass.", e)

    #Run a bash command to generate gif and show it
    if CONFIG.GIF_GENERATION:
        print("Generating gif under ./pngs/")
        os.system("convert -delay 0 pngs/*_ZOOM%s.png -loop 0 pngs/output_ZOOM%s.gif"%(CONFIG.ZOOMER, CONFIG.ZOOMER))
        os.system("eog pngs/output_ZOOM%s.gif"%CONFIG.ZOOMER)

    print("Thank you feifei")

