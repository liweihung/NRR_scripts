#-----------------------------------------------------------------------------#
#sunspot_plot.py
#
#NPS Night Skies Program
#
#Last updated: 2017/12/11
#
#This script plots the number of sunspots verse time. The input data was 
#downloaded from http://www.sidc.be/silso/datafiles#total website. Must include 
#the credit: SILSO data/image, Royal Observatory of Belgium, Brussels 
#
#Input: 
#   (1) sunspot.txt
#
#Output:
#   (1) sunspot.jpg
#
#History:
#	Li-Wei Hung -- created
#
#-----------------------------------------------------------------------------#

import matplotlib.pyplot as plt
import numpy as n

#-----------------------------------------------------------------------------#
Y, S = n.loadtxt('sunspot.txt', usecols=(2,3)).T
w = n.where(Y>1980)

plt.figure(0, figsize=(12,4.5))
plt.clf()
plt.plot(Y[w], S[w],'k.-')
plt.xlabel('Years', fontsize=18)
plt.ylabel('Number of Sunspots', fontsize=18)
plt.minorticks_on()
plt.tick_params(axis='y',which='minor',left='off',right='off')
plt.tick_params(labelsize=16, which='both', pad=8)
plt.tight_layout()
plt.draw()
plt.show(block=False)

plt.savefig('sunspots.jpg', dpi=200)

#plt.savefig(r'C:\Users\lhung\Documents\Peer Review\NRR_Chaco\Images' + 
#            r'\fig15-sunspots.jpg', dpi=200)