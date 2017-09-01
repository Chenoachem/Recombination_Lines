import astropy
from astropy.io import fits
from astropy.modeling import models
import numpy as np
import matplotlib
#get_ipython().magic(u'matplotlib inline')
from matplotlib import pyplot

import sys

mycube=sys.argv[1]
blank=sys.argv[2]

#Open the data cube

cube = fits.open(mycube)
data = cube[0].data
header = cube[0].header
small_cube = data[:,:,:]
small_cube.shape

ave_cube = np.average(small_cube[0:10,:,:], axis=0)



#Open the blank cube

blank = fits.open(blank)
data = blank[0].data
header = blank[0].header
Blank = data[:,:]

tot_ave=(ave_cube + Blank)/2

subcube=small_cube - tot_ave

#Save data to a new cube

cube[0].data = np.float32(subcube)
cube.writeto('Sub_'+mycube, clobber=True)
