# Author: Toma OC
#
# Generates subplots comparing HSC luminosity, current, dI/dt,
# and E-field waveforms as functions of time.

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import general as g
from scipy.signal import butter, filtfilt # argrelextrema,
from read_channel_saentis import rcs
#from local_extrema import local_extrema
# latex fonts:
from matplotlib import rcParams
rcParams['text.usetex'] = True

# colors
colors = ['#000075', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
          '#bcbd22', '#17becf', '#B8B8B8', '#eeeeee']

# filter functions
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a
    
def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# select flash:
#     ['UPa','UP0','UP1','UP2','UN1','UN2','UN3','UN4','UP3','UP4','UN5','UN6',
#      'UN7','UN8']
f=3 # [' 0 ',' 1 ',' 2 ',' 3 ',' 4 ',' 5 ',' 6 ',' 7 ',' 8 ',' 9 ','10 ','11 ',
    #  '12 ','13 ']
flash = g.names[f]

# open the video file
vc = cv2.VideoCapture('../../hsc/kronberg/UP2/2021-07-24_18.24.25.963149.avi')

# Get the video frame width and height
wdth = int(vc.get(3))
hght = int(vc.get(4))
print('Frame dimensions: %i x %i' % (wdth, hght))

# Get the total number of frames in the video
tf = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
print("Total frames:", tf)

# loop through video and sum pixel values of each frame
pvs = []
for fr in range(tf):
    ret, frame = vc.read()
    pvs.append(cv2.sumElems(frame)[0])

pvmin = np.min(pvs) # for later

frms=np.arange(1,tf+1) # frame array (1->tf)
tfrm=frms/24 # frames to ms

# go to current data
os.chdir(g.crdir+g.cds[f])

fsc = 50e6 # current sampling rate (Hz)
End_time = 2.4
data_size_nS = End_time * fsc

# pick current sensor
cs = ['Bdtt','PEMt','ROCb','PEMb']
# 1: B-dot top (dI/dt)
# 2: PEM top (I)
# 3: ROCOIL bottom (I)
# 4: PEM bottom (I)
chp = 4
cha = 3
chb = 1
# read from channel
cur,tc = rcs('./',chp,data_size_nS,fsc) # current data
#dia,ta = rcs('./',cha,data_size_nS,fsc) # ROCb data (for alignment)
bds,tb = rcs('./',chb,data_size_nS,fsc) # B-dot data

# go to ef data
os.chdir(g.cfadir+g.rds[f])

XX = 4e7 # number of samples set on digitizer
fsxe = 20e6 # digitiser sampling rate (Hz)

# set up time array
Txe = np.arange(1,XX+1)/fsxe
txe = Txe*1e3 # convert to ms

## CHANNEL 2    E-field Melope
# Amplifier was set to 10 kV/m before 30.7.2021 and 1 kV/m after 30.7.
# Volts to kV/m conversion cofficient:
KK_ef = (10 * 1 / 0.4) if f<10 else (1 * 1 / 0.4)

fIDe = open('adlink_ch1.bin', 'rb')
Ych1_r = np.fromfile(fIDe, dtype='>d')
Ych1e = KK_ef * Ych1_r

## CHANNEL 3    E-field Flat plate, mostly not working
#fIDf = open('adlink_ch2.bin', 'rb')
#Ych2_r = np.fromfile(fIDf, dtype='>d') #,XX,'double','ieee-be')
#K_flat_plate to calculate

# align data

# find peak values
ilm = np.argmax(pvs)
icm = np.argmax(np.abs(cur))
lcos = tfrm[ilm]-tc[icm] # lumin.-current time offset
print('HSC - Tower time offset:', lcos, 'ms')
tlum = tfrm - lcos # shift time array

# use B-dot signal to align EF signal
if f in [2,3,7,10,11,9]: # UP1, UP2, UN4, UN5
    idc = np.argmax(np.abs(bds))
    #print(f'B-dot max: {max(bds)} kA/us at {tc[idc]} us')
    idc = np.argmin(bds)
    #print(f'B-dot min: {min(bds)} kA/us at {tc[idc]} us')
# same for EF
if f in [0,1,2,3,8,9]: # UPa, UP0, UP1, UP2, UP3
    Emargin = np.abs(np.mean(Ych1e)) + np.std(Ych1e)*8 # 20,12,9
    ide,vae = next((ide,vae) for ide,vae in enumerate(Ych1e)
                    if np.abs(vae) > Emargin)
    print(f'First E-field step: {vae} kV/m at {txe[ide]} us')
if f in [7,11]: # UN4, UN6
    ide = np.argmax(np.abs(Ych1e))
#else:
#    print('INVALID FLASH NUMBER')

tos = txe[ide]-tc[idc] # time offset
print('Radome - Tower time offset:', tos, 'ms')

# shift time array accordingly
txes = txe-tos #txe[(ide-i0):(ide+ie)]
Yefs = Ych1e

## RAW DATA and adjust units
fpvs = pvs
fcur = cur # in kA
fbds = bds # in kA/us
fefs = Yefs*1e3 # to V/m

## FILTER DATA and adjust units
cutoff = 1e5 # Hz ## also removes EF system oscillations?
#fpvs = butter_lowpass_filter(, cutoff, fsxe)
fcur = butter_lowpass_filter(cur, cutoff, fsc) # in kA
fbds = butter_lowpass_filter(bds, cutoff, fsc) # in kA/us
#fefs = butter_lowpass_filter(Yefs, cutoff, fsxe)*1e3 # to V/m

print('Lumin. avg.: %.7g +/- %.7g' % (np.mean(fpvs), np.std(fpvs)))
print('Lumin. range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (pvmin, tlum[np.argmin(fpvs)],
         np.max(fpvs), tlum[np.argmax(fpvs)]))
print('%s avg.: %.7g +/- %.7g' % (cs[chp-1], np.mean(fcur), np.std(fcur)))
print('%s range: %.7g (at %.9g us) to %.7g (at %.9g us)' % (cs[chp-1],
      np.min(fcur), tc[np.argmin(fcur)], np.max(fcur), tc[np.argmax(fcur)]))
print('%s avg.: %.7g +/- %.7g' % (cs[chb-1], np.mean(fbds), np.std(fbds)))
print('%s range: %.7g (at %.9g us) to %.7g (at %.9g us)' % (cs[chb-1],
      np.min(fbds), tc[np.argmin(fbds)], np.max(fbds), tc[np.argmax(fbds)]))
print('E-field avg.: %.7g +/- %.7g' % (np.mean(fefs), np.std(fefs)))
print('E-field range: %.7g (at %.9g us) to %.7g (at %.9g us)'
      % (np.min(fefs), txes[np.argmin(fefs)],
         np.max(fefs), txes[np.argmax(fefs)]))

# write data to file
os.chdir(g.ppd+flash)

#with open(flash+'_%s_%s_data_filt.bin'%(cs[chp-1],cs[chb-1]), # raw/filt
#          "wb") as file:
#    np.save(file, [tc, fcur, fbds])

#with open(flash+'_EF_data_raw.bin', "wb") as file: # raw/filt
#    np.save(file, [txes, fefs, fpvs])

#exit()

# leader start time (1st step)
#tsl = 959.010 # UP2

# zoom times
t1 = 940.
t2 = 1100.

# find corresponding indices
#ic1=np.argmin(np.abs(tc-t1)) # starting index (hsc)
#ic2=np.argmin(np.abs(tc-t2)) # ending index (hsc)
it1=np.argmin(np.abs(tc-t1)) # starting index (tower)
it2=np.argmin(np.abs(tc-t2)) # ending index (tower)
ir1=np.argmin(np.abs(txes-t1)) # starting index (radome)
ir2=np.argmin(np.abs(txes-t2)) # ending index (radome)

# ID peaks and troughs in time range:
#Lmin=np.min(fpvs[ir1:ir2])
#Lmax=np.max(fpvs[ir1:ir2])
Imin=np.min(fcur[it1:it2])
Imax=np.max(fcur[it1:it2])
Bmin=np.min(fbds[it1:it2])
Bmax=np.max(fbds[it1:it2])
Emin=np.min(fefs[ir1:ir2])
Emax=np.max(fefs[ir1:ir2])
print('For the specified time interval (%.7g to %.7g ms):' % (t1,t2))
#print('Lumin. avg.: %.5g +/- %.5g' %
#      (np.mean(fpvs[ir1:ir2]),np.std(fpvs[ir1:ir2])))
#print('Lumin. range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
#      % (Lmin, txes[ir1+np.argmin(fpvs[ir1:ir2])],
#         Lmax, txes[ir1+np.argmax(fpvs[ir1:ir2])]))
print('Current avg.: %.5g +/- %.5g' %
      (np.mean(fcur[it1:it2]),np.std(fcur[it1:it2])))
print('Current range: %.7g (at %.9g us) to %.7g (at %.9g ms)'
      % (Imin, tc[it1+np.argmin(fcur[it1:it2])],
         Imax, tc[it1+np.argmax(fcur[it1:it2])]))
print('dI/dt avg.: %.5g +/- %.5g' %
      (np.mean(fbds[it1:it2]),np.std(fbds[it1:it2])))
print('dI/dt range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (Bmin, tc[it1+np.argmin(fbds[it1:it2])],
         Bmax, tc[it1+np.argmax(fbds[it1:it2])]))
print('E-field avg.: %.5g +/- %.5g' %
      (np.mean(fefs[ir1:ir2]),np.std(fefs[ir1:ir2])))
print('E-field range: %.7g (at %.9g ms) to %.7g (at %.9g ms)'
      % (Emin, txes[ir1+np.argmin(fefs[ir1:ir2])],
         Emax, txes[ir1+np.argmax(fefs[ir1:ir2])]))
      #'deltaE =',(Emax-Emin))

# Find and print local extrema
div=16 # division
#local_extrema(t1, t2, fsc, fsxe, tc, fcur, fbds, txes, fpvs, fefs, div)

#exit()

# set yaxis offsets to zero
#Lmax,Lmin = (Lmax,Lmin) -= pvmin
Imax,Imin = (Imax,Imin)-np.mean(fcur)
Bmax,Bmin = (Bmax,Bmin)-np.mean(fbds)
Emax,Emin = (Emax,Emin)-np.mean(fefs)

fpvs -= pvmin
for y in (fcur, fbds, fefs): y -= np.mean(y) #

#dL = Lmax-Lmin
dI = Imax-Imin
dB = Bmax-Bmin
dE = Emax-Emin

# setup PLOTS
fig, (ax1, ax0, ax3, ax2) = plt.subplots(4, 1) #

ax1.set_title('Luminosity')
ax0.set_title('Current (%s)' % cs[chp-1])
ax3.set_title('Current derivative (%s)' % cs[chb-1])
ax2.set_title('E-field')

# whole flash
#st = -tos if tos<0 else 0 # start time
#et = 2e3-tos if (2e3-tos)<2400 else 2400 # end time
#for ax in (ax1, ax0, ax3, ax2): ax.set_xlim(st, et)

# zoom
for ax in (ax1, ax0, ax2, ax3): ax.set_xlim(t1, t2) #
ax1.set_ylim(0, 4e7)
ax0.set_ylim(Imin-.05*dI, Imax+.05*dI)
ax3.set_ylim(Bmin-.05*dB, Bmax+.05*dB)
ax2.set_ylim(Emin-.05*dE, Emax+.05*dE)

ax1.set_ylabel('Pixel sum')
ax0.set_ylabel('$I$ (kA)')
ax3.set_ylabel('$dI/dt$ (kA/$\mu s$)')
ax2.set_ylabel('$E_z$ (V/m)')

plt.xlabel('Time (ms)')

ax1.plot(tlum, fpvs, linewidth=0.8, color=colors[1])
ax0.plot(tc, fcur, linewidth=0.8, color=colors[0])
ax3.plot(tc, fbds, linewidth=0.8, color=colors[3])
ax2.plot(txes, fefs, linewidth=0.8, color=colors[2])

# add space between plots
fig.subplots_adjust(hspace=3/4)#, wspace=1/3)

# add lines
for ax in (ax0, ax3, ax2): # ax1, 
    ax.axhline(y=0, linestyle=':', lw=0.6, color='black')
    #ax.axvline(x=959010., linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.0209, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.0898, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.1558, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.2036, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.2123, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=1041.521, linestyle=':', lw=0.5, color=colors[4])
    #ax.axvline(x=959.6411, linestyle=':', lw=0.5, color=colors[4])


#plt.show()

#fig.savefig(flash+'_Libe_whole_raw.pdf', bbox_inches='tight')
#fig.savefig(flash+'_Libe_whole_100khzIB.pdf', bbox_inches='tight')
#fig.savefig(flash+'_ibe_zoomMP-1_raw.pdf', bbox_inches='tight')
fig.savefig(flash+'_Libe_Izoom_100khzIB_test.pdf', bbox_inches='tight')

# TO DO:
#  4. Update summary sheet and/or paper appendix.
#  5. ID events using > np.abs(mean+2*sigma) and/or max. DONE.
#  6. Apply low-pass filter for frequencies > 5e6 Hz. DONE.
#     (1 MHz for temporal correlation OK, raw for max)
#  7. Align current and Ef based on 10% rise time.
#  9. Check B-dot data (greater frequency sensitivity). DONE.


# Flash (Activity in 1-5s prior?)
# Close field timestamp
# Control room timestamp
# Herisau timestamp

# UP0 (Yes at EUCLID 2021-06-28 23:26:52. Confirm location)
# 2021-06-29_01.27.06,860815048
# 2021-06-29_01.27.30.430286026
# 2021-06-29_01.26.53.611041545

# UP1 (None. EUCLID 2021-07-24 16:06:06 where?)
# 2021-07-24_18.06.15,656520843
# 2021-07-24_18.06.44.769081436
# 2021-07-24_18.06.08.092065811

# UP2 (None. EUCLID 2021-07-24 16:24:00 where?)
# 2021-07-24_18.24.11,515220642
# 2021-07-24_18.24.40.678498596
# 2021-07-24_18.24.03.949035167

# UN4 (None. Flash itself at EUCLID 2021-07-30 15:38:10? If so why not below?)
# 2021-07-30_17.38.21,666766166
# 2021-07-30_17.38.47.073173566
# 2021-07-30_17.38.10.279182434

# UP3 (YES at EUCLID 2021-07-30 18:00:10)
# 2021-07-30_20.00.22,734939098
# 2021-07-30_20.00.47.477396746
# 2021-07-30_20.00.11.270195007

# UP4 (YES at EUCLID 2021-07-30 18:04:53)
# 2021-07-30_20.05.05,753443241
# 2021-07-30_20.05.30.176073566
# 2021-07-30_20.04.54.327002525
