
import sys
import os
import argparse
import numpy as np
import astropy
from astropy.io import fits
import matplotlib
from matplotlib import pyplot as plt
from astropy.coordinates import SkyCoord  # High-level coordinates
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude  # Angles
import astropy.units as u
from astropy import wcs

cube=sys.argv[1]
lat=sys.argv[2]
lon=sys.argv[3]

#open the fits file

datacube = fits.open(cube)
data = datacube[0].data
header = datacube[0].header

lat=float(lat)
lon=float(lon)


#set the naxis to 2 dimentions to get the pixel coordinates
w = wcs.WCS(datacube[0].header, naxis=2)

#put the coordinates into a skycoordinate array
c_icrs = SkyCoord(ra=lat*u.degree, dec=lon*u.degree,frame='icrs')


#convert the RA and Dec into pixel coordinates
xpix,ypix=c_icrs.to_pixel(w,origin=0,mode='wcs')

#set teh pixel values to integers from floats
xpix=int(xpix)
ypix=int(ypix)

#get the frequencies for the x-axis

rp = datacube[0].header['CRPIX3']
rf = datacube[0].header['CRVAL3']
df = datacube[0].header['CDELT3']
nf = datacube[0].header['NAXIS3']
xvals = rf + df*(np.arange(nf)-rp)
first=xvals[0]
first=str(first/10**6)

#build an array of the signal from the pixel coordinates
signal=[]
xpix2=xpix+25
ypix2=ypix+25
for x in range(0, 10):
    value = np.nanmean(data[x,xpix:xpix2,ypix:ypix2])
    signal.append(value)


#plot the spectrum
plt.plot(xvals/10**6,signal, "r-",ls="steps")
plt.title("Cube"+first+"- Carbon RRL")
plt.xlabel("Frequency (MHz)")
plt.ylabel("Flux density (Jy)")
plt.ylim(-1,1)
plt.savefig("Cube"+first+".png")






# Recombination_Lines
