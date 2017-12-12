#-----------------------------------------------------------------------------#
#verticalillum_angle.py
#
#NPS Night Skies Program
#
#Last updated: 2017/12/12
#
#This script finds the azimuth angle associated with the maximum vertical 
#illuminance
#
#Note: This script is written for Python3
#	
#Input: 
#   (1) illumall.xls in Calibdata folder for each data night 
#   (2) Data set information (modify the first three lines here)
#
#Output:
#   (1) Prints out the table on the python screen
#
#History:
#	Li-Wei Hung -- Created
#
#-----------------------------------------------------------------------------#

import numpy as n
import os
import pandas as pd


#-----------------------------------------------------------------------------#

#Modify the following three lines to specify the data sets 
fpath = 'c:/Users/lhung/Documents/Peer Review/NRR_Chaco/CHCU_data/Calibdata/'
set = [1,1,1,1,1,2,3,1,3] # data set number used
dnt = ['CHCU011014','CHCU030129','CHCU030131','CHCU050311','CHCU080530','CHCU080531','CHCU130601','CHCU140509','CHCU160924']

S = pd.Series(data=set, index=dnt, name='set')
A = pd.Series(name='azimuth')
V = pd.Series(name='max_vertical_illuminance')

i = 0
for dnight in os.listdir(fpath):
    if not os.path.isdir(fpath+dnight):
        continue
    
    #read in azimuth angle in degrees and vertical illuminance in mlx
    F = pd.read_excel(fpath+dnight+'/illumall.xls',
                      sheetname='Sheet 1',
                      skiprows=2,
                      skip_footer=12,
                      header=None,
                      names=['azimuth','vert'],
                      usecols=[0,S[i]*2-1])

    max_index = F['vert'].idxmax()
    A[dnight] = F['azimuth'][max_index]
    V[dnight] = round(F['vert'][max_index],2)
    i+=1

D = pd.DataFrame([S,A,V]).transpose()
print(D)
















