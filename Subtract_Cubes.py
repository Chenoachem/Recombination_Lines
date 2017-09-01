import astropy
from astropy.io import fits
from astropy.modeling import models
import numpy as np
import sys

mycube=sys.argv[1]
blank=sys.argv[2]

#Open the data cube

cube = fits.open(mycube)
data = cube[0].data
header = cube[0].header
small_cube = data[:,:,:]
small_cube.shape


#Open the blank cube

blank = fits.open(blank)
data = blank[0].data
header = blank[0].header
Blank = data[:,:]


subcube=small_cube - Blank


#Save data to a new cube

cube[0].data = np.float32(subcube)
cube.writeto('Sub_'+mycube+'.fits', clobber=True)
