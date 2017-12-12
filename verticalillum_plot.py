#-----------------------------------------------------------------------------#
#verticalillum_plot.py
#
#NPS Night Skies Program
#
#Last updated: 2017/12/11
#
#This script plots (1) the vertical illuminance from anthropogenic light as a 
#function of azimuth angle and (2) the panoramic image showing only the 
#artificial light in the background.
#
#Note: This script is written for Python3
#	
#Input: 
#   (1) illum.xls in Calibdata folder of the datanight 
#   (2) panoramic image showing only artificial-light 
#
#Output:
#   (1) verticalillum.jpg
#
#History:
#	Li-Wei Hung -- Created
#
#-----------------------------------------------------------------------------#

import pandas as pd
import matplotlib.pyplot as plt
import numpy as n

#-----------------------------------------------------------------------------#

#----------- Read in data -----------#
#Read in azimuth angle in degrees and vertical illuminance from artificial 
#sources in mlx 
fpath = 'c:/Users/lhung/Documents/Peer Review/NRR_Chaco/CHCU_data'+\
        '/Calibdata/CHCU080531/'

A = pd.read_excel(fpath + 'illum.xls',
                  sheetname='Sheet 1',
                  skiprows=2,
                  skip_footer=47,
                  header=None,
                  names=['azimuth','vert'],
                  usecols=[0,3]
                  )

#Copy the row with azimuth of 0 degree to azimuth of 360 degrees
A.loc[len(A)] = [360,A.vert[0]]                  
   
#Read in the artificial panoramic image in the background (facing south)
imgpath = 'C:/Users/lhung/Documents/Peer Review/NRR_Chaco/Images/'
img_north = plt.imread(imgpath+'CHCU_testimage.jpg')[196:500,57:1203] 
h = int(img_north.shape[1]/2)
img_south = n.concatenate([img_north[:,h:-1,:],img_north[:,1:h,:]],axis=1)


#-----------     Plot     -----------#
fig = plt.figure(0, figsize=(12,4.2))
plt.clf()
ax = fig.add_subplot(111)

#Plot the background
ax.imshow(img_south, alpha=0.5, extent=[0,360,0,1.1*A['vert'].max()], aspect="auto")

#Plot the vertical illuminance
ax.plot(A['azimuth'], A['vert'],'y-',lw=3)
ax.plot(A['azimuth'], A['vert'],'k--',lw=2)
line1 = plt.Line2D([], [], linewidth=2.5, linestyle="-", color='yellow')
line2 = plt.Line2D([], [], linewidth=2, linestyle="-", dashes=(4, 2), color='black')

#Plot settings
ax.set_xlabel('Azimuth Angle (degree)', fontsize=16)
ax.set_ylabel('Vertical Illuminance (mlx) \n from artificial sources   ', fontsize=16)
ax.minorticks_on()
ax.set_xticks(n.arange(0,450,45))
ax.set_xlim(0,360)
ax.tick_params(labelsize=14, which='both', pad=8)
ax.yaxis.set_ticks_position('both')
fig.tight_layout()
plt.draw()
plt.show(block=False)
plt.savefig('verticalillum.jpg', dpi=150)
#plt.savefig(imgpath+'fig20-verticalillum.jpg', dpi=150)

