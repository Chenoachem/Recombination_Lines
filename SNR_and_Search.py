

import astropy
from astropy.io import fits
from astropy.modeling import models
import numpy as np
import matplotlib
#get_ipython().magic(u'matplotlib inline')
from matplotlib import pyplot


# now lets do a polynomial fit instead of the mean
import scipy
import scipy.stats
from scipy.stats import linregress

#open the continuum subtracted fits file
subcube = fits.open('median_Sub.fits')
data = subcube[0].data
header = subcube[0].header

# we can just delete the stokes axis
rm_cube = data[0:100,:,:]
rm_cube.shape

#replace all the zeros with nans before doing statistical calculations
rm_cube[rm_cube==0] = np.nan
rm_cube.shape

#Can be used to check noise if need to diagnose a problem
#slice = range(5,48) + range(49,90)
#slice=45
#for i in xrange(500,1500,200):
#    for j in xrange(500,1500,200):
#        print np.nanstd(rm_cube[slice,i:i+200,j:j+200])

#for i in xrange(10,80,10):
#    print np.nanstd(rm_cube[i:i+10,800:1000,800:1000])


#calculate the standard deviation but ignoring nans
rms_cube=np.nanstd(rm_cube, axis=1)
rms_cube.shape

#print np.nanstd(rm_cube[:,890:910,890:910])
#print rms_cube[900,900]


#make a signal to noise map
snr=rm_cube/rms_cube

#save the signal to noise cube to a fits file
subcube[0].data = np.float32(snr)
subcube.writeto('Median_snr.fits', clobber=True)
subcube[0].data=np.float32(rms_cube)
subcube.writeto('Median_rms.fits', clobber=True)

#open the SNR cube fits file
#snr_cube = fits.open('Median_snr.fits')
#data = snr_cube[0].data

#positions= np.where(abs(data[5:89,100:1900,100:1900]) > 5)
#np.savetxt("positions.csv", positions, delimiter=",")





