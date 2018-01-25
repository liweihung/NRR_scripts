#-----------------------------------------------------------------------------#
#panoramic_plot.py
#
#NPS Night Skies Program
#
#Last updated: 2017/12/20
#
#This script takes the jpg images from Dan's pipeline output to re-plot the 
#panoramic images for the night skies NRRs with readable labels, axises, 
#and color-bar.
#
#Note: This script is written for Python3
#	
#Input: 
#   (1)park specific information section
#   (2)*_fullres_*.jpg  ----------observed sky
#   (2)*_artificial_*.jpg  -------light from artificial sources
#   (3)colorbar.jpg  -------------color bar
#   (4)AH_large_shaded_4C.jpg ----NPS arrowhead logo
#
#Output:
#   (1)jpg images for night skies NRRs
#
#History:
#	Li-Wei Hung -- Created
#
#-----------------------------------------------------------------------------#
import matplotlib.pyplot as plt
import numpy as n
import pandas as pd

#-----------------------------------------------------------------------------#
def cover(image):
    '''
    Mask out the original image labels by turning those pixels black
    '''
    B = image.copy()[340:340+h0,:,:]  #cut out top and bottom
    k = 0                             #0=black; 255=white
    B[:250,6000:,:] = k               #top right-hand corner
    B[200:240,1820:1870,:] = k        #60 degree altitude label
    B[850:890,525:575,:] = k          #30 degree altitude label
    B[1740:1780,70:120,:] = k         # 0 degree altitude label
    return n.flip(B,axis=0)

#-----------------------------------------------------------------------------#
#----------- Park specific information -------------------------------------#
#Input and output image location
Pin = 'C:/Users/lhung/Data_pipeline_Dan/graphics/'
Ptable = 'C:/Users/lhung/Data_pipeline_Dan/tables/'
Pout = 'C:/Users/lhung/Documents/Peer Review/NRR_Chaco/Images/'

#data night and data set used
D = {'CHCU011014':1,
     'CHCU030129':1,
     'CHCU030131':1,
     'CHCU050311':1,
     'CHCU080530':1,
     'CHCU080531':2,
     'CHCU130601':3,
     'CHCU140509':1,
     'CHCU160924':3
     }

#cities to be labeled
C = ['Albuquerque','Farmington','Rio Rancho','Gallup','Crownpoint','Santa Fe',
     'Bloomfield','Grants']
                  

#----------- Read in common images and set the common parameters -----------#
cbar = plt.imread('colorbar.jpg')                      #colorbar
logo = plt.imread('AH_large_shaded_4C.jpg').copy()     #arrowhead
logo[n.where(logo[:,:]==[8,6,7])] = 0                  #set background to black

#label positions
h0 = 1780
h1 = 240
h2 = 2330
h3 = 170
h4 = 4500
h5 = 0.4
h6 = 1750
h7 = 30
h8 = 1.2
h9 = 3600-h8*cbar.shape[1]/2.2
h10 = 4440
h11 = 0.8

#azimuth and cardinal labels
A = [236, 710, 1250, 1820, 2430, 3060, 3700, 4340, 4970, 5580, 6150, 6680, 7164]
P = {0:'N',90:'E',180:'S',270:'W',360:'N'}

#master plot array
master = n.zeros([5000,7400,3],dtype='uint8')

#plot
fig = plt.figure(0, figsize=(12,8.108),frameon=False)

#----------- Loop through images -------------------------------------------#
for k in D.keys():
    #Read in the panoramic images
    obs = plt.imread(Pin+k+'_fullres_{}_HA180.jpg'.format(D[k]))   
    art = plt.imread(Pin+k+'_artificial_{}_HA180.jpg'.format(D[k]))
    
    #Place the panoramic images in the master array
    master[h1:h1+h0,100:-100,:] = cover(art)
    master[h2:h2+h0,100:-100,:] = cover(obs)
    
    #Read in observation information
    Tn = pd.read_excel(Ptable+k+'.xlsx',sheetname='NIGHT METADATA',
                       skiprows=3,header=0)
    Ts = pd.read_excel(Ptable+k+'.xlsx',sheetname='SET METADATA',
                       skiprows=3,header=0)
    date = Ts['MID_DATE_LMT'][D[k]-1]
    LMT = Ts['MID_TIME_LMT'][D[k]-1]
    site = Tn['SITE_NAME'][0]
    
    #Plot images
    plt.clf()
    ax = plt.axes([0,0,1,1]) #use these two lines for the final figure production
    plt.axis('off')
    #ax = fig.add_subplot(111) #use these two lines to show axises
    #plt.tight_layout()
    ax.set_xlim(0,7400)
    ax.set_ylim(0,5000)
    ax.imshow(master)
    ax.imshow(logo,extent=[h3,h3+h5*logo.shape[1],h4,h4+h5*logo.shape[0]])
    ax.imshow(cbar,extent=[h9,h9+h8*cbar.shape[1],h10,h10+h11*cbar.shape[0]])

    #Text labels
    ax.text(h3+970,h4+0.85*h5*len(logo)/2,                            #NPS
            'U.S. National Park Service\nNight Skies Program',
            color='w',fontsize=11,ha='center',va='center')
    ax.text(3600,4820,'Chaco Culture NHP',                            #Park
            color='w',fontsize=24,ha='center',va='top')
    ax.text(7220,4800,
            '{:%B %d, %Y}\n{:.1f} hr LMT\n{}'.format(date,LMT,site),  #Date
            color='w',fontsize=14,ha='right',va='top')
    ax.text(3700,h10-100,r'V mags arcsec$^{-2}$',                     #Unit
            color='w',fontsize=10,ha='center',va='top')
    ax.text(180,h2+h6,'(a) Observed Sky',                             #(a)
            color='w',fontsize=14,ha='left',va='top')
    ax.text(180,h1+h6,'(b) Light from Artificial Sources',            #(b)
            color='w',fontsize=14,ha='left',va='top')  
    
    #City labels
    Tc = pd.read_excel(Ptable+k+'.xlsx',sheetname='CITIES',
                       skiprows=3,skip_footer=80,header=0)
    for city in C:                                                    #Cities
        b = [city in i for i in Tc['PLACE']].index(1)
        j = n.interp(Tc['BEARING'][b],n.arange(0,390,30),A)
        ax.text(j,550,city,color='wheat',fontsize=12,
                ha='center',va='bottom',rotation=90)

    #Tick mark labels -- color bar
    for mag in range(14,25):                                          #Color bar
        ax.text(h9+20+268*h8*(mag-14),h10-10,mag,color='w',
                fontsize=10,ha='center',va='top')

    #Tick mark labels -- direction
    for i in range(13):
        a = 30*i
        if a in P.keys():                                             #Cardinal
            ax.text(A[i],h1-h7,P[a],color='r',fontsize=14,
                    ha='center',va='top')
            ax.text(A[i],h2-h7,P[a],color='r',fontsize=14,
                    ha='center',va='top')
        else:                                                         #Azimuth
            ax.text(A[i],h1-h7,a,color='lightgray',fontsize=10,
                    ha='center',va='top')
            ax.text(A[i],h2-h7,a,color='lightgray',fontsize=10,
                    ha='center',va='top')
            
    plt.draw()
    #plt.show(block=False)
    #plt.savefig('test.jpg', dpi=300)
    plt.savefig(Pout+k+'_mosaic.jpg', dpi=150)

