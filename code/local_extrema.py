# Author: Toma OC

import numpy as np
from scipy.signal import argrelextrema

def local_extrema(t1, t2, fsc, fsxe, tc, fcur, fbds, txes, fxrs, fefs, div):
    # define indices
    it1=np.argmin(np.abs(tc-t1)) # starting index (tower)
    it2=np.argmin(np.abs(tc-t2)) # ending index (tower)
    ir1=np.argmin(np.abs(txes-t1)) # starting index (radome)
    ir2=np.argmin(np.abs(txes-t2)) # ending index (radome)
    # determine sample size
    twst = fsc*(t2-t1)*(1e-3) # number of samples in time window (tower)
    twsr = fsxe*(t2-t1)*(1e-3) # number of samples in time window (radome)
    #print('Sample sizes:', twst, twsr)
    # Current
    #cni = argrelextrema(fcur[it1:it2], np.less, order=int(twst/div)) # I min
    #cnt = [] # minima times
    #cnv = [] # minima values
    #for id in cni:
    #    cnt.append(tc[it1+id])
    #    cnv.append(fcur[it1+id])
    #print('Current minima times:', cnt)
    #print('Current minima value:', cnv)
    cxi = argrelextrema(np.abs(fcur[it1:it2]), np.greater,
                        order=int(twst/div)) # absolute value max
    cxt = [] # maxima times
    cxv = [] # maxima values
    for id in cxi:
        cxt.append(tc[it1+id])
        cxv.append(fcur[it1+id])
    print('Current peak times:', cxt)
    print('Current peak value:', cxv)
    # B-dot (dI/dt)
    bni = argrelextrema(fbds[it1:it2], np.less, order=int(twst/div)) # min
    bnt = [] # minima times
    bnv = [] # minima values
    for id in bni:
        bnt.append(tc[it1+id])
        bnv.append(fbds[it1+id])
    print('B-dot minima times:', bnt)
    print('B-dot minima value:', bnv)
    bxi = argrelextrema(fbds[it1:it2], np.greater, order=int(twst/div)) # max
    bxt = [] # maxima times
    bxv = [] # maxima values
    for id in bxi:
        bxt.append(tc[it1+id])
        bxv.append(fbds[it1+id])
    print('B-dot maxima times:', bxt)
    print('B-dot maxima value:', bxv)
    # E-field
    efni = argrelextrema(fefs[ir1:ir2], np.less, order=int(twsr/div)) # Ef min
    efnt = [] # minima times
    efnv = [] # minima values
    for id in efni:
        efnt.append(txes[ir1+id])
        efnv.append(fefs[ir1+id])
    print('E-field minima times:', efnt)
    print('E-field minima value:', efnv)
    efxi = argrelextrema(fefs[ir1:ir2], np.greater, order=int(twsr/div)) # max
    efxt = [] # maxima times
    efxv = [] # maxima values
    for id in efxi:
        efxt.append(txes[ir1+id])
        efxv.append(fefs[ir1+id])
    print('E-field maxima times:', efxt)
    print('E-field maxima value:', efxv)
    # X-rays
    xrei = argrelextrema(fxrs[ir1:ir2], np.greater, order=int(twsr/div)) # Xr min
    xret = [] # x-ray event times
    xree = [] # x-ray event energies
    for id in xrei:
        xret.append(txes[ir1+id])
        xree.append(fxrs[ir1+id])
    print('XR event times:', xret)
    print('XR event energ:', xree)
    

# TO DO:
#  1. overplot x-rays and current. DONE.
#  2. overplot e-field and current. DONE.
#  3. Zoom on events. DONE.
#  4. Update summary sheet and/or paper appendix
#  5. ID events using > np.abs(mean+2*sigma) and/or max. DONE.
#  6. Apply low-pass filter for frequencies > 5e6 Hz. DONE.
#     (1 MHz for temporal correlation OK, raw for max)
#  7. Align current and Ef based on 10% rise time.
#  8. Scatter plot of rise-times, peaks, etc. (current, x-ray)
#  9. Check B-dot data (greater frequency sensitivity). DONE.
# 10. Add B-dot to subplots for comparison. (1x4 or 2x2 ?)
