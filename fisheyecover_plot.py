#-----------------------------------------------------------------------------#
#fisheyecover_plot.py
#
#NPS Night Skies Program
#
#Last updated: 2018/01/24
#
#This script takes the fish-eye jpg image from Dan's pipeline output and re-plot
#it for the night skies NRRs cover image with readable labels, axises, and 
#color-bar.
#
#Note: This script is written for Python3
#	
#Input: 
#   (1)Dan's fisheye image from his pipeline output
#   (2)colorbar.jpg
#
#Output:
#   (1)jpg image for the night skies NRR cover
#
#History:
#	Li-Wei Hung -- Created
#
#
#-----------------------------------------------------------------------------#
import matplotlib.pyplot as plt
import numpy as n

#-----------------------------------------------------------------------------#
#Park specific information
#Read in image
Pin = 'C:/Users/lhung/Documents/Peer Review/NRR_Chaco/Images/'
Pout = Pin
im = plt.imread(Pin+'CHCU_fisheyecover.jpg').copy()    #fisheye image
cbar = plt.imread('colorbar.jpg').copy()               #colorbar

#Mask out the original image labels by turning those pixels black
k = 0                              #0=black; 255=white
im[:500,:,:] = k                   #top
im[:730,:2650,:] = k               #top-left corner
im[:730,6400:,:] = k               #top-right corner
im[7150:,:,:] = k                  #bottom

#Create figure
fig = plt.figure(0, figsize=(8,8), frameon=False)
plt.clf()
ax = plt.axes([0,0,1,1]) #use these two lines for the final figure production
plt.axis('off')
#ax = fig.add_subplot(111) #use these two lines when tuning
#plt.tight_layout()
ax.set_xlim(0,im.shape[0])
ax.set_ylim(0,im.shape[1])

#label positions
x0 = 4000
x1 = 200
x2 = 5000
x3 = 1150

y0 = 7080
y1 = 6800
y2 = 250
y3 = 6700

s0 = 0.65
s1 = 272.5*s0

#Plot images    
ax.imshow(n.flip(im,axis=0),origin='bottom')
ax.imshow(n.flip(cbar,axis=0),origin='top',
          extent=[x1,x1+s0*cbar.shape[1],y3,y3+1*cbar.shape[0]])

#Color bar tick mark labels 
for mag in range(14,25,2):                                          
    ax.text(x1+s1*(mag-14),y3-30,mag,color='w',fontsize=7,ha='center',va='top')

#Text labels
ax.text(x0,y0,'Chaco Culture National Historical Park',color='w',
        fontsize=16,ha='center',va='bottom')
ax.text(x3,y3+80,r'V mags arcsec$^{-2}$',color='w',
        fontsize=8,ha='center',va='bottom')
ax.text(im.shape[1]-x1,y1,'May 31, 2008\n23.3 hr LMT\nWater Tank',color='w',
        fontsize=10,ha='right',va='top')
ax.text(x1,y2,'Night Skies Program\nUS National Park Service',color='w',
        fontsize=10,ha='left',va='bottom')
ax.text(im.shape[1]-x1,y2,'Observed Sky in False Color'+
        '\nFisheye Equal Area Projection',color='w',
        fontsize=10,ha='right',va='bottom')

#Cardinal direction labels
ax.text(3733,6775,'N',color='r',fontsize=11,ha='center',va='bottom')
ax.text(3733, 500,'S',color='r',fontsize=11,ha='center',va='top')
ax.text( 570,3648,'E',color='r',fontsize=11,ha='right',va='center')
ax.text(6865,3648,'W',color='r',fontsize=11,ha='left',va='center')

#show and save        
plt.draw()
plt.show(block=False)
#plt.savefig('test.jpg', dpi=300)
#plt.savefig(Pout+'fig01-cover.jpg', dpi=150)

