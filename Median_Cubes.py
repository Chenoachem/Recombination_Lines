import astropy
from astropy.io import fits
from astropy.modeling import models
import numpy as np
import matplotlib
#get_ipython().magic(u'matplotlib inline')
from matplotlib import pyplot
from glob import glob


#Pull all the blank files into a list

files=glob('Sub*.fits')
#Sub_SgrA_I_1160_Continuum_Slice20.fits.fits

#Determine the shape of each files in order to crate a blank.

shape=len(files),10,2000,2000

#Make a blank datacube to stack all the data into it.

data=np.empty(shape=shape, dtype=np.float32)

#Stack all the data into a single cube

for i,f in enumerate(files):
    data[i,:,:,:] = fits.getdata(f)

#Take the median of the data files
median=np.nanmedian(data, axis=0)

#Save the new cube
cube=fits.open(files[0])
cube[0].data=median
cube.writeto('median_nosignal.fits')
