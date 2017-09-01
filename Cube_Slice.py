import astropy
from astropy.io import fits
from astropy.modeling import models
import numpy as np
import matplotlib

from matplotlib import pyplot
import sys


#open cube file

cube=sys.argv[1]

mycube = fits.open(cube+'.fits')
data = mycube[0].data
header = mycube[0].header

#reshape the cube to remove the stokes parameter
rm_cube = data[0,:,:,:].reshape((99,2000,2000))


#Choose the centre channel and slice the cube

num=sys.argv[2]
num=int(num)
centre=num
start=centre-5
end=centre+5
cube_slice = rm_cube[start:end,:,:]

#Correct the header information in the cube
freq=mycube[0].header['CRVAL3']
mycube[0].header['CRVAL3']=freq+(start*10000)


#Save the sliced cube
num=str(num)
mycube[0].data = np.float32(cube_slice)
mycube.writeto(cube+'_Slice'+num+'.fits', clobber=True)

#Make a blank channel cube and average the channel data
num=int(num)
if num > 20:
	centre=num-20
	start=centre-5
	end=centre+5
	cube_blank = np.average(rm_cube[start:end,:,:], axis=0)
else:
	centre=num+20
	start=centre-5
	end=centre+5
	cube_blank = np.average(rm_cube[start:end,:,:], axis=0)

#Save blank cube
num=str(num)
mycube[0].data = np.float32(cube_blank)
mycube.writeto(cube+'_Blankave'+num+'.fits', clobber=True)
