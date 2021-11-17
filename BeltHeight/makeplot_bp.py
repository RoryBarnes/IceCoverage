import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import vplanet
import vplot as vpl
import os
import matplotlib.patches as mpatches
import sys
import scipy.ndimage
from matplotlib.pyplot import figure
import matplotlib.lines as mlines
from bigplanet import bp_extract as bp
import pathlib
from itertools import chain


dest = ['/media/caitlyn/Data_Drive8/Projects/IceBelt/K_Cases/K_Monte_Carlo_large/',
        '/media/caitlyn/Data_Drive8/Projects/IceBelt/G_Cases/G_Monte_Carlo_Large_2/',
        '/media/caitlyn/Data_Drive8/Projects/IceBelt/F_Cases/F_Monte_Carlo_large/']
#dest = ['../DynamicCases/CaseA/KDwarf/','../DynamicCases/CaseA/GDwarf/','../DynamicCases/CaseA/FDwarf/']
star = ['K Dwarf','G Dwarf','F Dwarf']
num = 10000

fig, axs = plt.subplots(3,1,figsize=(9,7))
fig.subplots_adjust(top=0.851,bottom=0.098,left=0.085,right=0.98,hspace=0.839,wspace=0.2)

for x in range(len(dest)):

    #case = [f.path for f in os.scandir(dest[x]) if f.is_dir()][0]
    #case_name = [f.name for f in os.scandir(dest[x]) if f.is_dir()][0]

    #os.chdir(dest[x])
    num = int(num)
    data = np.zeros(151)
    avg_count = np.zeros(151)
    icecount = 0
    
    file = bp.BPLFile(path / "Test.bpf")


    snowballL = bp.Ext
    snowballS = float(line[2])
    northCapL = float(line[3])
    northCapS = float(line[4])
    southCapL = float(line[5])
    southCapS = float(line[6])
    icebeltL = float(line[7])
    icebeltS = float(line[8])
    iceFree = float(line[9])

    if (
        icebeltL == 1 and icebeltS == 0 and southCapS == 0 and
        southCapL == 0 and northCapS == 0 and northCapL == 0 and
        snowballL == 0 and snowballS == 0
    ):
        if icecount <= 70:
            out = vplanet.get_output(folders[number], units = False)
            body = out.bodies[1]

            lats = np.unique(body.Latitude)
            nlats = len(lats)
            ntimes = len(body.Time)

            ice = np.reshape(body.IceHeight,(ntimes,nlats))
            ice_last = ice[-1]

            data += ((ice_last.T)/1000)
            indi = axs[x].plot(lats,((ice_last.T)/1000), color = 'gray', alpha = 0.25)
            icecount += 1

    for z in range(data.size):
        avg_count[z] = data[z]/icecount

    avg_plot = axs[x].plot(lats,avg_count, color = 'black', linewidth = 4)
    axs[x].plot([-80,-90],[0,0], color = 'black', linewidth = 4)
    axs[x].plot([80,90],[0,0], color = 'black', linewidth = 4)

    indi_leg = mlines.Line2D([],[],color = 'gray',linewidth = 3 ,label = 'Individual Cases', alpha = 0.25)
    avg_leg = mlines.Line2D([],[],color = 'black',linewidth = 4,label = 'Average')

    axs[x].set_xlim(-90,90)
    axs[0].set_ylim(0.0,5.0)
    axs[1].set_ylim(0.0,5.0)
    axs[2].set_ylim(0.0,5.0)

    axs[0].set_yticks([0.0,2.5,5.0])
    axs[1].set_yticks([0.0,2.5,5.0])
    axs[2].set_yticks([0.0,2.5,5.0])

    axs[0].set_title("K Dwarf", fontsize = 16)
    axs[1].set_title("G Dwarf", fontsize = 16)
    axs[2].set_title("F Dwarf", fontsize = 16)

    axs[x].set_xlabel(r'Latitude [$^\circ$]', fontsize = 12)
    axs[x].set_ylabel("Ice Height [km]", fontsize = 12)

    axs[0].legend(handles = [indi_leg,avg_leg], fontsize=14, loc = 'upper left',
                bbox_to_anchor=(0, 1.75, 1, 0.102),ncol=2, mode="expand", borderaxespad=0,edgecolor='k')


plt.tight_layout()
os.chdir('/home/caitlyn/IceSheet/BeltHeight')
if (sys.argv[1] == 'pdf'):
    plt.savefig('BeltHeight' + '.pdf')
if (sys.argv[1] == 'png'):
    plt.savefig('BeltHeight' + '.png')

plt.show()
plt.close()
